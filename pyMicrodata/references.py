# -*- coding: utf-8 -*-

import rdflib

#unsafe for versions greater than 9 
if int(rdflib.__version__[0]) >= 3:
	from rdflib	import RDF  as ns_rdf
	from rdflib	import RDFS as ns_rdfs
	from rdflib	import Graph
else :
	from rdflib.RDFS	import RDFSNS as ns_rdfs
	from rdflib.RDF		import RDFNS  as ns_rdf
	from rdflib.Graph import Graph
