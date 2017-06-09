import urllib
params = urllib.urlencode({'Hello World': 1})
f = urllib.urlopen("http://127.0.0.1:8080", params)
print f.read()