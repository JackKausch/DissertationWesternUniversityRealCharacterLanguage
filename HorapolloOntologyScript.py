'''
Adapted on 08 March 2022

@author: ejimenez-ruiz
@modified-by: jack-kausch
'''
import sys
sys.path.append("../")
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
from rdflib.util import guess_format
import pandas as pd
from isub import isub
from lookup import DBpediaLookup
import csv
import owlrl

#Most of this script was written by Ernesto Jiminez-Ruiz for his course on Semantic Web Technologies and Knowledge Graphs at City University of London. It was modified by Jack Kausch to produce the Horapollo ontology.

class hrpSolution(object):
    '''
    Example of a partial solution for Lab 5 
    '''
    def __init__(self, input_file):
   
        #The idea is to cover as much as possible from the original csv file, but for the lab and coursework I'm more interested 
        #in the ideas and proposed implementation than covering all possible cases in all rows (a perfect solution fall more into
        #the score of a PhD project). Also in terms of scalability calling the 
        #look-up services may be expensive so if this is a limitation, a solution tested over a reasonable percentage of the original 
        #file will be of course accepted.        
        self.file = input_file
    
        #Dictionary that keeps the URIs. Specially useful if accessing a remote service to get a candidate URI to avoid repeated calls
        self.stringToURI = dict()
        
        
        #1. GRAPH INITIALIZATION
    
        #Empty graph
        self.g = Graph()
        
        #Note that this is the same namespace used in the ontology "ontology_lab5.ttl"
        self.hrp_ns_str= "http://realcharacterlanguage.world/horapollo/"
        self.wikidata_ns_str ="http://wikidata.org/wiki/Property:"
        self.rdf_ns_str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        
        #Special namspaces class to create directly URIRefs in python.           
        self.hrp = Namespace(self.hrp_ns_str)
        self.wikidata = Namespace(self.wikidata_ns_str)
        self.rdf = Namespace(self.rdf_ns_str)
        
        #Prefixes for the serialization
        self.g.bind("hrp", self.hrp) #hrp is a newly created namespace
        
        
        #Load data in dataframe  
        self.data_frame = pd.read_csv(self.file, sep=',', quotechar='"',escapechar="\\")    
    
        
        #KG
        self.dbpedia = DBpediaLookup()
    
    
    
    def Task1(self):
        self.CovertCSVToRDF(False)
        
    def Task2(self):
        self.CovertCSVToRDF(True)

            
    def CovertCSVToRDF(self, useExternalURI):
                 
        #In a large ontology one would need to find a more automatic way to use the ontology vocabulary. 
        #E.g.,  via matching. In a similar way as we match entities to a large KG like DBPedia or Wikidata
        #Since we are dealing with very manageable ontologies, we can integrate their vocabulary 
        #within the code. E.g.,: hrp.City
        
        
        #We modularize the transformation to RDF. The transformation is tailored to the given table, but 
        #the individual components/mappings are relatively generic (especially type and literal triples).
        
        #Mappings may required one or more columns as input and create 1 or more triples for an entity
        
        
        self.g.add((URIRef('http://purl.org/textontology/unicode/uo_core.owl#describesUnicodeCharacter'), RDF.type, OWL.ObjectProperty))
        
        self.g.add((URIRef('http://purl.org/textontology/texteme/texteme_core.owl#describesTexteme'), RDF.type, OWL.ObjectProperty))
        self.g.add((URIRef(self.wikidata.P11473),RDF.type, OWL.ObjectProperty))
        self.g.add((URIRef(self.wikidata.P898), RDF.type, OWL.ObjectProperty))
      #  self.g.add((URIRef('http://purl.org/textontology/unicode/uo_core.owl#describesUnicodeCharacter'), URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'),URIRef("http://http://www.w3.org/2002/07/owl#topObjectProperty")))
     #   self.g.add((URIRef('http://purl.org/textontology/unicode/uo_core.owl#describesUnicodeCharacter'), URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'),URIRef("http://http://www.w3.org/2002/07/owl#topObjectProperty")))
     #   self.g.add((URIRef(self.wikidata.P11473), URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'), URIRef("http://http://www.w3.org/2002/07/owl#topObjectProperty")))
       # self.g.add((URIRef(self.wikidata.P898), URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'),URIRef("http://http://www.w3.org/2002/07/owl#topObjectProperty")))
        self.g.parse('uo_core.owl')
        self.g.parse('texteme_core.owl')
        self.g.parse('ontolex.owl')
        self.g.parse('horapollo.owl')
        
        if 'Font PNG URI ' in self.data_frame:
            
            #We give subject column and target type
            self.mappingToCreateTypeTriple('Font PNG URI ', self.hrp.RealCharacter)
            self.mappingToCreateTypeTriple('Egyptian Hieroglyph URI ', "http://purl.org/textontology/unicode/uo_core.owl#UnicodeCharacter")
            self.mappingToCreateTypeTriple('Emoji URI', "http://purl.org/textontology/unicode/uo_core.owl#UnicodeCharacter")
            self.mappingToCreateTypeTriple('Phone URI', "http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#Expression")
            self.mappingToCreateTypeTriple('Roman Texteme URI', "http://purl.org/textontology/texteme/texteme_core.owl#Texteme")

            
            
            #We give subject and object columns (they could be the same), predicate and datatype 
            self.mappingToCreateObjectTriple('Font PNG URI ',  'CLLD URI', self.wikidata.P11473)
            self.mappingToCreateObjectTriple('Font PNG URI ', 'Phone URI',self.wikidata.P898 )
            self.mappingToCreateObjectTriple('Font PNG URI ','Emoji URI', 'http://purl.org/textontology/unicode/uo_core.owl#describesUnicodeCharacter')
            self.mappingToCreateObjectTriple('Font PNG URI ','Egyptian Hieroglyph URI ', 'http://purl.org/textontology/unicode/uo_core.owl#describesUnicodeCharacter')
            self.mappingToCreateObjectTriple('Font PNG URI ','Roman Texteme URI', 'http://purl.org/textontology/texteme/texteme_core.owl#describesTexteme')
            self.mappingToCreateLiteralTriple('Font PNG URI ', 'Egyptian Hieroglyph', self.hrp.Name, XSD.string)
            self.mappingToCreateLiteralTriple('Font PNG URI ', 'Unicode Emoji', self.hrp.Name, XSD.string)
            self.mappingToCreateLiteralTriple('Font PNG URI ', 'CLLD Concept Set', self.hrp.Name, XSD.string)


        
          
    def createURIForEntity(self, name, useExternalURI):
        
        #We create fresh URI (default option)
        self.stringToURI[name] = self.hrp_ns_str + name.replace(" ", "_")
        
        if useExternalURI: #We connect to online KG
            uri = self.getExternalKGURI(name)
            if uri!="":
                self.stringToURI[name]=uri
        
        return self.stringToURI[name]
    
    
        
    def getExternalKGURI(self, name):
        '''
        Approximate solution: We get the entity with highest lexical similarity
        The use of context may be necessary in some cases        
        '''
        
        entities = self.dbpedia.getKGEntities(name, 5)
        #print("Entities from DBPedia:")
        current_sim = -1
        current_uri=''
        for ent in entities:           
            isub_score = isub(name, ent.label) 
            if current_sim < isub_score:
                current_uri = ent.ident
                current_sim = isub_score
        
            #print(current_uri)
        return current_uri 
            
    
    '''
    Mapping to create triples like hrp:London rdf:type hrp:City
    A mapping may create more than one triple
    column: columns where the entity information is stored
    useExternalURI: if URI is fresh or from external KG
    '''
    def mappingToCreateTypeTriple(self, subject_column, class_type):
        
        for subject in self.data_frame[subject_column]:
                
            #We use the ascii name to create the fresh URI for a city in the dataset
           
            #TYPE TRIPLE
            #For the individuals we use URIRef to create an object "URI" out of the string URIs
            #For the concepts we use the ones in the ontology and we are using the NameSpace class
            #Alternatively one could use URIRef(self.hrp_ns_str+"City") for example 
            self.g.add((URIRef(subject), RDF.type, URIRef(class_type)))
        
    def is_nan(self, x):
        return (x != x)
                        

            
    '''
    Mappings to create triples of the form hrp:london hrp:name "London"
    '''    
    def mappingToCreateLiteralTriple(self, subject_column, object_column, predicate, datatype):
        
        for subject, lit_value in zip(self.data_frame[subject_column], self.data_frame[object_column]):
            
     
                #New triple
                self.g.add((URIRef(subject), URIRef(predicate), Literal(lit_value, datatype=datatype)))
            
    '''
    Mappings to create triples of the form hrp:london hrp:cityIsLocatedIn hrp:united_kingdom
    '''
    def mappingToCreateObjectTriple(self, subject_column, object_column, predicate):
        
        for subject, object in zip(self.data_frame[subject_column], self.data_frame[object_column]):
                    
                #New triple
                self.g.add((URIRef(subject), URIRef(predicate), URIRef(object)))
    
    
    
    def performReasoning(self, ontology_file):
        
        #We expand the graph with the inferred triples
        #We use owlrl library with OWL2 RL Semantics (instead of RDFS semantic as we saw in lab 4)
        #More about OWL 2 RL Semantics in lecture/lab 7
        
        print("Data triples from CSV: '" + str(len(self.g)) + "'.")    
    
        #We should load the ontology first
        #print(guess_format(ontology_file))
     #   self.g.load(ontology_file,  format=guess_format(ontology_file)) #e.g., format=ttl
        
        
        print("Triples including ontology: '" + str(len(self.g)) + "'.")
        
        
        #We apply reasoning and expand the graph with new triples 
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(self.g)
        
        print("Triples after OWL 2 RL reasoning: '" + str(len(self.g)) + "'.")
    
    
    
    def performSPARQLQuery(self, file_query_out):
        
        qres = self.g.query(
            """SELECT DISTINCT ?country ?city ?pop WHERE {
              ?city rdf:type hrp:City .
              ?city hrp:isCapitalOf ?country .
              ?city hrp:population ?pop .
              FILTER (xsd:integer(?pop) > 5000000)
        }
        ORDER BY DESC(?pop)
        """)


        print("%s capitals satisfying the query." % (str(len(qres))))
        
        f_out = open(file_query_out,"w+")

        for row in qres:
            #Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\",\"%s\"\n' % (row.country, row.city, row.pop)


            f_out.write(line_str)
            
     
        f_out.close()       
        
        
    def performSPARQLQueryLab7(self):
        
        qres = self.g.query(
            """SELECT DISTINCT ?country (COUNT(?city) AS ?num_cities) WHERE { 
              ?country hrp:hasCity ?city .
        }
        GROUP BY ?country
        ORDER BY DESC(?num_cities)
        """)


   
        for row in qres:
            #Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\"' % (row.country, row.num_cities)
            print(line_str)

     
          
    def saveGraph(self, file_output):
        
        ##SAVE/SERIALIZE GRAPH
        #print(self.g.serialize(format="turtle").decode("utf-8"))
        self.g.serialize(destination=file_output, format='xml')
        
        
    
        

    

if __name__ == '__main__':
    
    #Format:
    file = "Horapollo1.3.csv"
    
    solution = hrpSolution(file)
    
    task = "task1"
    #task = "task2"
   # task = "Simple_Mapping"
    
    #Create RDF triples
    if task == "task1":
        solution.Task1()  #Fresh entity URIs
    elif task == "task2":
        solution.Task2()  #Reusing URIs from DBPedia
    else:
        solution.SimpleUniqueMapping()  #Simple and unique mapping/transformation
        
    
    #Graph with only data
    solution.saveGraph(file.replace(".csv", "-"+task)+".owl")
    
    #OWL 2 RL reasoning
    #We will see reasoning next week. Not strictly necessary for this 
   # solution.performReasoning("ontology_lab5.ttl") ##ttl format
    solution.performReasoning("horapollo.owl") ##owl (rdf/xml) format
    solution.performReasoning("uo_core.owl")
    solution.performReasoning("texteme_core.owl")
    solution.performReasoning("semiotics.owl")
    solution.performReasoning("ontolex.owl")
    
    #Graph with ontology triples and entailed triples       
    solution.saveGraph(file.replace(".csv", "-"+task)+"-reasoning.owl")
    
    #SPARQL results into CSV
   # solution.performSPARQLQuery(file.replace(".csv", "-"+task)+"-query-results.csv")
    
    
    #SPARQL for Lab 7 2021
    #solution.performSPARQLQueryLab7()
    
    
    
    
     



