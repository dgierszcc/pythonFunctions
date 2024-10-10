import requests

pyURL = "https://github.com/dgierszcc/pythonFunctions/<filename>"
pyFile = <filename>
request = request.get(pyURL)
with open(pyFile, "wb") as f:
  f.write(request.content)

from <file minus extention> import <function>

"""Example
import requests

pyURL = "https://github.com/dgierszcc/pythonFunctions/getGitFunctions.py"
pyFile = "getGitFunctions.py"
request = request.get(pyURL)
with open(pyFile, "wb") as f:
  f.write(request.content)

from getGitFunctions import nameOfFunction
"""
