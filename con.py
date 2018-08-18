
import imp
f = open('configfile')
global data
data = imp.load_source('data', '', f)

print data.robotimage
