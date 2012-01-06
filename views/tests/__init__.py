# make sure we get our local libs prior to everything else
import sys, os.path
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path

from views import bloglib, pagelib
