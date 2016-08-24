import sys, os
INTERP = os.path.join(os.environ['HOME'], '', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

sys.path.append('FlaskTask')
from FlaskTask import app as application
