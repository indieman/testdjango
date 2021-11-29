__author__ = 'indieman'

from fabric.contrib import files
import sys, os, fabtools, fabric, fileinput, random, string
from fabric.api import *
from fabtools import require
from fabtools.python import virtualenv, install_pip55555
from fabtools.files import watch, upload_template
from fabtools.service import restart
from fabric.contrib.files import comment, uncomment
from fabtools.utils import run_as_root

env.project_name = 'testdjango'
env.db_name = env.project_name
env.db_pass = ''
env.db_user = env.project_name
env.project_user = env.project_name

env.shell = '/bin/bash -c'

env.hosts = ['%(project_user)s@192.168.12.2' % env]
env.repository_url = 'https://github.com/indieman/testdjango.git'

env.virtualenv_path = '/usr/local/virtualenvs/%(project_name)s' % env
env.path = '/srv/sites/%(project_name)s' % env
env.manage_path = '/srv/sites/%(project_name)s/%(project_name)s' % env
env.settings_path = '/srv/sites/%(project_name)s/%(project_name)s/%(project_name)s' % env


def create_password(length = 13):
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    passwd = ''.join(random.choice(chars) for i in range(length))
    return passwd


@task
def host(host_name):
    env.hosts = [host_name]


@task
def setup():
    """
    Setup project.
    """
    require.deb.packages([
        'curl',
        'python',
        'mercurial',
        'subversion',
        'git',
        'vim',
        'sudo',
        'libpq-dev',
        'libxml2-dev',
        'libxslt1-dev',
    ], update=True)

    # Creating project paths.
    sudo('mkdir %s -p' % env.path)
    sudo('chown %(project_user)s %(path)s' % env)
    sudo('mkdir %s -p' % env.virtualenv_path)
    sudo('chown %(project_user)s %(virtualenv_path)s' % env)

    fabtools.git.clone(env.repository_url, path=env.path, use_sudo=False, user=env.project_user)

    require.python.virtualenv(env.virtualenv_path, use_sudo=False)

    require.python.virtualenv(env.virtualenv_path, use_sudo=False)
    with virtualenv(env.virtualenv_path):
        require.python.requirements(os.path.join(env.path, 'reqs', 'server.txt'))

    env.db_pass = create_password()
    upload_template('%(project_name)s/server_settings.py' % env, '%(settings_path)s/server_settings.py' % env,
                          context={'DB_PASSWORD': env.db_pass}, use_jinja=True)

    print env.db_pass
    # Require a PostgreSQL server
    require.postgres.server()
    require.postgres.user(env.db_user, password=env.db_pass, createdb=False, createrole=True)
    require.postgres.database(env.db_name, env.db_user)

    with cd(env.manage_path):
        run('chmod ogu+x manage.py')

    manage('collectstatic')

    # Require a supervisor process for our app
    require.supervisor.process(env.project_name,
                               command='%(virtualenv_path)s/bin/gunicorn -c %(path)s/_deploy/gunicorn.conf.py \
                               -u %(project_user)s testdjango.wsgi:application' % env,
                               directory=env.manage_path,
                               user=env.project_user,
                               stdout_logfile='%(path)s/log/testdjango.log' % env)

    # Require an nginx server proxying to our app
    require.nginx.proxied_site(env.project_name,
                               port=80,
                               docroot='%(path)s/static' % env,
                               proxy_url='http://127.0.0.1:8888')

    remove_default_nginx()

    manage('syncdb')
    manage('migrate')


@task
def remove_default_nginx():
    sudo('rm /etc/nginx/sites-enabled/default')
    restart('nginx')


@task
def update():
    """
    Update project.
    """
    with cd(env.path):
        run('git pull')

    with virtualenv(env.virtualenv_path):
        require.python.requirements(os.path.join(env.path, 'reqs', 'server.txt'))

    sudo('chmod ogu+x %(manage_path)s/manage.py' % env)

    # manage('syncdb')
    manage('migrate')
    manage('collectstatic')
    fabtools.supervisor.restart_process('all')


@task
def manage(command, noinput=True):
    """
    Run manage command.
    """
    with virtualenv(env.virtualenv_path):
        if noinput:
            run('%(manage_path)s/manage.py ' % env + command + ' --noinput')
        else:
            run('%(manage_path)s/manage.py ' % env + command)


@task
def create_project_user(pub_key_file, username=None):
    """
    Creates linux account, setups ssh access.

    Example::

        fab create_project_user:"/home/indieman/.ssh/id_rsa.pub"

    """
    require.deb.packages(['sudo'])
    with open(os.path.normpath(pub_key_file), 'rt') as f:
        ssh_key = f.read()

    username = username or env.project_user

    with (settings(warn_only=True)):
        sudo('adduser %s --disabled-password --gecos ""' % username)

    if username == 'root':
        home_dir = '/root/'
    else:
        home_dir = '/home/%s/' % username

    with cd(home_dir):
        sudo('mkdir -p .ssh')
        files.append('.ssh/authorized_keys', ssh_key, use_sudo=True)
        sudo('chown -R %s:%s .ssh' % (username, username))

    line = '%s ALL=(ALL) NOPASSWD: ALL' % username
    files.append('/etc/sudoers', line)
