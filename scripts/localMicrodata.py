#!/usr/bin/env python
"""
Run the microdata extraction package locally
"""

import sys

sys.path.insert(0,"/Users/ivan/Source/PythonModules/MyModules/pyMicrodata-1.0")
sys.path.insert(0,"/Users/ivan/W3C/dev/2004/PythonLib-IH/rdfa-1.1")

# You may want to adapt this to your environment...
import sys, getopt, platform

from pyMicrodata import pyMicrodata
		
###########################################	


usageText="""Usage: %s -[xtjnpb:] [filename[s]]
where:
  -x: output format RDF/XML
  -t: output format Turtle (default)
  -j: output format JSON-LD
  -n: output format N Triples
  -p: output format pretty RDF/XML
  -b: give the base URI; if a file name is given, this can be left empty and the file name is used

'Filename' can be a local file name or a URI. In case there is no filename, stdin is used.

"""

def usage() :
	print usageText % sys.argv[0]

format = "turtle"
base   = ""

try :
	opts, value = getopt.getopt(sys.argv[1:],"xtjnpb:")
	for o,a in opts:
		if o == "-t" :
			format = "turtle"
		elif o == "-j" :
			format = "json-ld"
		elif o == "-n" :
			format = "nt"
		elif o == "-p" or o == "-x":
			format = "pretty-xml"
		elif o == "-b" :
			base = a
		else :
			usage()
			sys.exit(1)
except :
	usage()
	sys.exit(1)

processor = pyMicrodata(base)
if len(value) >= 1 :
	print processor.rdf_from_sources(value, outputFormat = format)
else :
	print processor.rdf_from_source(sys.stdin, outputFormat = format)
	
	

	
