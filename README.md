
## Purpose

The app taught me how to use Flask and Fabric, and gave me an opportunity to practice python in a web
environment. Each page contains a different error that could be in a website.

## Development

Development will done using [_flask_](http://flask.pocoo.org/), a lightweight
python web framework. For a consistent development environment, we use a
Vagrant virtual machine.  Once Vagrant is installed, do `vagrant up` to bring
up the Vagrant virtual machine and then `vagrant ssh` to login to the VM.

To run FlaskTask app in the virtual machine,

```
cd /vagrant
source venv/bin/activate
./run.py FlaskTask -d
```

which will be available on <http://localhost:5000> from the host machine.

## Deployment

Deploying FlaskTask to its domains on dreamhost is done via fabric.
First, the virtual environments on the domains must be set up. Ssh into each domain and run

```
virtualenv .
```

Next, in a clone of the FlaskTask repo run:

```
fab pack deploy
```
This will update all the domains in the fabfile SERVERS array simultaneously.

## Test

```
nosetests test/test_FlaskTask.py -s -v
```
