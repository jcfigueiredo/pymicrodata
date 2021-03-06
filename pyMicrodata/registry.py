# -*- coding: utf-8 -*-
"""

Hardcoded version of the current microdata->RDF registry. There is also a local registry to include some test cases.
Finally, there is a local dictionary for prefix mapping for the registry items; these are the preferred prefixes
for those vocabularies, and are used to make the output nicer.

@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
@license: This software is available for use under the
U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231">}
"""

"""
$Id: registry.py,v 1.4 2012/03/26 13:18:31 ivan Exp $
$Date: 2012/03/26 13:18:31 $
"""

import sys

_registry = """
{
  "http://schema.org/": {
    "propertyURI":    "vocabulary",
    "multipleValues": "unordered",
    "properties": {
      "blogPosts": {"multipleValues": "list"},
      "breadcrumb": {"multipleValues": "list"},
      "byArtist": {"multipleValues": "list"},
      "creator": {"multipleValues": "list"},
      "episodes": {"multipleValues": "list"},
      "events": {"multipleValues": "list"},
      "founders": {"multipleValues": "list"},
      "itemListElement": {"multipleValues": "list"},
      "musicGroupMember": {"multipleValues": "list"},
      "performerIn": {"multipleValues": "list"},
      "performers": {"multipleValues": "list"},
      "producer": {"multipleValues": "list"},
      "recipeInstructions": {"multipleValues": "list"},
      "seasons": {"multipleValues": "list"},
      "subEvents": {"multipleValues": "list"},
      "tracks": {"multipleValues": "list"}
    }
  },
  "http://xmlns.com/foaf/0.1/": {
    "propertyURI":    "vocabulary",
    "multipleValues": "unordered"
  },
  "http://microformats.org/profile/hcard": {
    "propertyURI":    "vocabulary",
    "multipleValues": "unordered"
  },
  "http://microformats.org/profile/hcalendar#": {
    "propertyURI":    "vocabulary",
    "multipleValues": "unordered",
    "properties": {
      "categories": {"multipleValues": "list"}
    }
  }
}
"""

vocab_names = {
	"http://schema.org/"                         : "schema",
	"http://xmlns.com/foaf/0.1/"     			 : "foaf",
	"http://microformats.org/profile/hcard#"     : "hcard",
	"http://microformats.org/profile/hcalendar#" : "hcalendar"
}

# This is the local version, added mainly for testing
_myRegistry = """
{
  "http://n.whatwg.org/work": {
    "propertyURI":    "contextual",
    "multipleValues": "list"
  } 
}
"""

registry   = []
myRegistry = []
if sys.version_info[1] >= 6 :
	import json
	registry   = json.loads(_registry)
	myRegistry = json.loads(_myRegistry)
else :
	import simplejson
	registry   = simplejson.loads(_registry)
	myRegistry = simplejson.loads(_myRegistry)

for (k,v) in myRegistry.items() : registry[k] = v

		




























