activate_this = '/var/www/postmash/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from postmash import app as application
