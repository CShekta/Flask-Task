from fabric.api import *

# the user to use for the remote commands
env.user = 'rubyFlaskTasknet'
# the servers where the commands are executed
env.hosts = ['FlaskTask.ninja']
SERVERS = ['FlaskTask.me', 'FlaskTask.pro', 'FlaskTask.mobi', 'FlaskTask.ninja']


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    run('mkdir -p /tmp/FlaskTask')
    put('dist/%s.tar.gz' % dist, '/tmp/FlaskTask.tar.gz')
    for server in SERVERS:
        put('passenger_wsgi.py', '/home/rubyFlaskTasknet/%s' % server)
    with cd('/tmp/FlaskTask'):
        run('tar xzf /tmp/FlaskTask.tar.gz')
        with cd('FlaskTask-1.0/'):
            for server in SERVERS:
                run('/home/rubyFlaskTasknet/%s/bin/python setup.py install' % server)
                run('mkdir -p /home/rubyFlaskTasknet/%s/tmp' % server)
                run('touch /home/rubyFlaskTasknet/%s/tmp/restart.txt' % server)
    run('rm -rf /tmp/FlaskTask.tar.gz /tmp/FlaskTask')
    local('rm -rf FlaskTask.egg-info dist')
