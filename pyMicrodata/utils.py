# -*- coding: utf-8 -*-
"""
Various utilities for pyMicrodata

@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
@license: This software is available for use under the
U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231">}
"""

"""
$Id: utils.py,v 1.5 2012/04/02 16:16:27 ivan Exp $
$Date: 2012/04/02 16:16:27 $
"""
import os, os.path, sys
import urllib, urlparse, urllib2
import re
from datetime import datetime

from rdflib	import BNode
import rdflib
if rdflib.__version__ >= "3.0.0" :
	from rdflib	import RDF as ns_rdf
else :
	from rdflib.RDF	import RDFNS  as ns_rdf

#################################################################################
def is_absolute_URI( uri ) :
	return urlparse.urlparse(uri)[0] != ""

#################################################################################

def fragment_escape( name ) :
	return urllib.quote(name, '/~:-.')
		
#################################################################################

def generate_URI(base, val) :
	"""
	Generate an (absolute) URI; if val is a fragment, then using it with base,
	otherwise just return the value
	@param base: Absolute URI for base
	@param val: relative or absolute URI
	"""
	if is_absolute_URI( val ) :
		return val
	else :
		if urlparse.urlparse(base)[0] == "" :
			# Simple file name...
			return base + '#' + val.strip()
		else :
			# Trust the python library...
			# Well, not quite:-) there is what is, in my view, a bug in the urljoin; in some cases it
			# swallows the '#' or '?' character at the end. This is clearly a problem with
			# Semantic Web URI-s
			val = fragment_escape(val.strip())
			parsed = urlparse.urlsplit(base)
			return urlparse.urlunsplit( (parsed.scheme,parsed.netloc,parsed.path,parsed.query,val) )

#################################################################################
def generate_RDF_collection( graph, vals ) :
	"""
	Generate an RDF List from vals, returns the head of the list
	@param graph: RDF graph
	@type graph: RDFLib Graph
	@param vals: array of RDF Resources
	@return: head of the List (an RDF Resource)
	"""
	# generate an RDF List, returns the head
	# list has all the elements in RDF format already
	heads = [ BNode() for r in vals ] + [ ns_rdf["nil"] ]
	for i in xrange(0, len(vals)) :
		graph.add( (heads[i], ns_rdf["first"], vals[i]) )
		graph.add( (heads[i], ns_rdf["rest"],  heads[i+1]) )
	return heads[0]

#################################################################################
def get_Literal(Pnode):
	"""
	Get (recursively) the full text from a DOM Node.

	@param Pnode: DOM Node
	@return: string
	"""
	rc = ""
	for node in Pnode.childNodes:
		if node.nodeType == node.TEXT_NODE:
			rc = rc + node.data
		elif node.nodeType == node.ELEMENT_NODE :
			rc = rc + get_Literal(node)
			
	# This presupposes that all spaces and such should be stripped. I am not sure it is true in the spec,
	# but this is what the examples show
	return re.sub(r'(\r| |\n|\t)+'," ",rc).strip()

#################################################################################
def get_lang(node) :
	# we may have lang and xml:lang
	retval  = None
	if node.hasAttribute("lang") :
		retval = node.getAttribute("lang")
	if retval and node.hasAttribute("xml:lang") :
		xmllang = node.getAttribute("xml:lang").lower()
		if not( xmllang != None and xmllang == retval.lower() ) :
			# This is an error, in which case retval must be invalidated...
			retval = None
	return retval

def get_lang_from_hierarchy(document, node) :
	lang = get_lang(node)
	if lang == None :
		parent = node.parentNode
		if parent != None and parent != document :
			return get_lang_from_hierarchy(document, parent)
		else :
			return get_lang(document)
	else :
		return lang
	
#################################################################################
datetime_type 	= "http://www.w3.org/2001/XMLSchema#dateTime"
time_type 	 	= "http://www.w3.org/2001/XMLSchema#time"
date_type 	 	= "http://www.w3.org/2001/XMLSchema#date"
date_gYear		= "http://www.w3.org/2001/XMLSchema#gYear"
date_gYearMonth	= "http://www.w3.org/2001/XMLSchema#gYearMonth"
date_gMonthDay	= "http://www.w3.org/2001/XMLSchema#gMonthDay"
duration_type	= "http://www.w3.org/2001/XMLSchema#duration"

_formats = {
	date_gMonthDay	  : [ "%m-%d" ],
	date_gYearMonth	  : [ "%Y-%m"],
	date_gYear     	  : [ "%Y" ],
	date_type      	  : [ "%Y-%m-%d", "%Y-%m-%dZ" ],
	time_type      	  : [ "%H:%M",
					      "%H:%M:%S",
					      "%H:%M:%SZ",						
					      "%H:%M:%S.%f" ],
	datetime_type  	  : [ "%Y-%m-%dT%H:%M",
					      "%Y-%m-%dT%H:%M:%S",
					      "%Y-%m-%dT%H:%M:%S.%f",
					      "%Y-%m-%dT%H:%MZ",
					      "%Y-%m-%dT%H:%M:%SZ",
					      "%Y-%m-%dT%H:%M:%S.%fZ" ],
	duration_type     : [ "P%dD",
						  "P%YY%mM%dD",
						  "P%YY%mM",
						  "P%YY%dD",
						  "P%YY",
						  "P%mM",
						  "P%mM%dD",
						 ],
}

_dur_times = [ "%HH%MM%SS", "%HH", "%MM", "%SS", "%HH%MM", "%HH%SS", "%MM%SS" ]

def get_time_type(string) :
	"""
	Check whether the string abides to one of the accepted time related datatypes, and returns that one if yes
	@param string: the attribute value to be checked
	@return : a datatype URI or None
	"""
	for key in _formats :
		for format in _formats[key] :
			try :
				# try to check if the syntax is fine
				d = datetime.strptime(string, format)
				# bingo!
				return key
			except ValueError :
				pass

	# Now come the special cases:-(
	# Check first for the duration stuff, that is the nastiest.
	if len(string) > 2 and string[0] == 'P' or (string [0] == '-' and string[1] == 'P') :
		# this is meant to be a duration type
		# first of all, get rid of the leading '-' and check again
		if string[0] == '-' :
			for format in _formats[duration_type] :
				try :
					# try to check if the syntax is fine
					d = datetime.strptime(string, format)
					# bingo!
					return duration_type
				except ValueError :
					pass
		# Let us see if the value contains a separate time portion, and cut that one
		durs = string.split('T')
		if len(durs) == 2 :
			# yep, so we should check again
			dur = durs[0]
			tm  = durs[1]
			# Check the duration part
			td = False
			for format in _formats[duration_type] :
				try :
					# try to check if the syntax is fine
					d = datetime.strptime(dur, format)
					# bingo!
					td = True
					break
				except ValueError :
					pass
			if td == True :
				# Getting there...
				for format in _dur_times :
					try :
						# try to check if the syntax is fine
						d = datetime.strptime(tm, format)
						# bingo!
						return duration_type
					except ValueError :
						pass
			# something went wrong...
			return None			
		else :
			# Well, no more tricks, this is a plain type
			return None

	# If we got here, we should check the time zone
	# there is a discrepancy betwen the python and the HTML5/XSD lexical string,
	# which means that this has to handled separately for the date and the timezone portion
	try :
		# The time-zone-less portion of the string
		str = string[0:-6]
		# The time-zone portion
		tz = string[-5:]
		try :
			t = datetime.strptime(tz,"%H:%M")
		except ValueError :
			# Bummer, this is not a correct time
			return None
		# The time-zone is fine, the datetime portion has to be checked
		for format in _formats[datetime_type] :
			try :
				# try to check if it is fine
				d = datetime.strptime(str, format)
				# Bingo!
				return datetime_type
			except ValueError :
				pass
	except :
		pass
	return None


#########################################################################################################
# Handling URIs
class URIOpener :
	"""A wrapper around the urllib2 method to open a resource. Beyond accessing the data itself, the class
	sets the content location.
	The class also adds an accept header to the outgoing request, namely
	text/html and application/xhtml+xml (unless set explicitly by the caller).
	
	@ivar data: the real data, ie, a file-like object
	@ivar headers: the return headers as sent back by the server
	@ivar location: the real location of the data (ie, after possible redirection and content negotiation)
	"""
	CONTENT_LOCATION	= 'Content-Location'
	def __init__(self, name) :
		"""
		@param name: URL to be opened
		@keyword additional_headers: additional HTTP request headers to be added to the call
		"""		
		try :
			# Note the removal of the fragment ID. This is necessary, per the HTTP spec
			req = urllib2.Request(url=name.split('#')[0])

			req.add_header('Accept', 'text/html, application/xhtml+xml')
				
			self.data		= urllib2.urlopen(req)
			self.headers	= self.data.info()

			if URIOpener.CONTENT_LOCATION in self.headers :
				self.location = urlparse.urljoin(self.data.geturl(),self.headers[URIOpener.CONTENT_LOCATION])
			else :
				self.location = name
				
		except urllib2.HTTPError, e :
			from pyMicrodata import HTTPError
			import BaseHTTPServer
			msg = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code]
			raise HTTPError('%s' % msg[1], e.code)
		except Exception, e :
			from pyMicrodata import MicrodataError
			raise MicrodataError('%s' % e)

