__author__ = 'indieman'

bind = "127.0.0.1:8888"
workers = 1
user = "testdjango"
group = "testdjango"
logfile = "/srv/sites/testdjango/log/gunicorn.log"
loglevel = "info"
proc_name = "testdjango"
pidfile = '/srv/sites/testdjango/pid/gunicorn_testdjango.pid'