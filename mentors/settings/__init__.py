from .common import *
try:
    from .prod import *
except ImportError:
    print
    print "!! WARNING !!"
    print "Please create a settings/prod.py file with your custom settings"
    print "See the settings/prod_sample.py file and README.md"
    print
