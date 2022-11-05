import urllib.parse
from urllib.parse import unquote

def toUrl(string):
    return urllib.parse.quote_plus(string)

def toString(url):
    return unquote(url).replace("+", " ")

# references: https://stackoverflow.com/questions/11768070/transform-url-string-into-normal-string-in-python-20-to-space-etc