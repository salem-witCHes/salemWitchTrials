import os
import pprint
import csv 
import hashlib
import rdflib
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC

# Namespaces 

g = rdflib.Graph()

EX = Namespace("http://example.org/item/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("(http://purl.org/dc/terms/")
FABIO = Namespace("http://purl.org/spar/fabio")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

namespaces = {
    "crm": CRM,
    "schema": SCHEMA,
    "dcterms": DCTERMS,
    "fabio": FABIO,
    "foaf": FOAF
}

# Predicate mapping
predicate_map = {} # dictionary for storing RDF URI
with open("mapping.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nl_predicate = row["predicate"]
        prefix = row["ontology_prefix"]
        property = row["ontology_property"]
        predicate_map[nl_predicate] = URIRef(namespaces[prefix][property])

# pprint.pprint(predicate_map)

# Read CSVs in folder
folder = "./csv_files"
for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            subj = URIRef(EX[row["subject"].replace(" ", "_")])
            pred = row["predicate"]
            obj = row["object"]

            # Replace natural language predicate with property
            if pred in predicate_map:
                predicate = predicate_map[pred]
            else:
                print(f"Unknown predicate '{pred}'") # If predicate match is missing
                predicate = RDFS.comment

            # Check if object is URI or literal SISTEMA
            obj_lit = Literal(obj)

            g.add((subj, predicate, obj_lit))

for s,p,o in g.triples((None, None, None)):
    print(s,p,o)

g.serialize(destination="first_try.ttl", format="ttl")