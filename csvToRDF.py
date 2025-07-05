import os
import pprint
import csv 
import hashlib
import rdflib
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC

# Namespaces 
BASE = Namespace("https://w3id.org/salemWitchTrials/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FABIO = Namespace("http://purl.org/spar/fabio")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

namespaces = {
    "crm": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "schema": Namespace("https://schema.org/"),
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "fabio": Namespace("http://purl.org/spar/fabio"),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
    "wd": Namespace("https://www.wikidata.org/wiki/"),
    "skos": Namespace("http://www.w3.org/2004/02/skos/core#"),
    "owl": Namespace("http://www.w3.org/2002/07/owl#"),
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    "viaf": Namespace("http://viaf.org/viaf/")
}

# Predicate mapping
predicate_map = {} # dictionary for storing RDF URI
with open("mapping.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nl_predicate = row["predicate"]
        prefix = row["ontology_prefix"]
        property = row["ontology_property"]
        predicate_map[nl_predicate.strip()] = URIRef(namespaces[prefix.strip()][property.strip()]) # strip() whitespace

# pprint.pprint(predicate_map)

# Entities mapping 
mapping_entities = {}
with open("mapping_entities.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mapping_entities[row["object"]] = row["entity"]

# print(my_entities)


# Initialize RDF graph
g = rdflib.Graph()

# List for our items
csv_items = []
csv_items_prefix = "item/"

# Read CSVs in folder
folder = "./csv_files"
for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        with open(path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subj = URIRef(BASE[row["subject"].replace(" ", "_")])
                pred = row["predicate"]
                obj = row["object"]

                csv_items.append(subj)

                # Replace natural language predicate with property
                if pred in predicate_map:
                    predicate = predicate_map[pred]
                else:
                    print(f"Unknown predicate '{pred}'") # If predicate match is missing
                    predicate = RDFS.comment

                # Check if object is entity or literal
                if obj in csv_items:
                    # create URIRef from base for it
                    object = URIRef(BASE + csv_items_prefix + obj)
                elif obj in mapping_entities:
                    entity = mapping_entities[obj]
                    if ":" not in entity:
                        # Simply use the base URI to create the object
                        obj = URIRef(BASE[entity])
                    else:
                        # Else split namespace and entity
                        namespace_str, entity_str = entity.split(":")
                        namespace = namespaces[namespace_str]
                        # Create object URI
                        obj = URIRef(namespace + entity_str)
                else:
                    # Otherwise create a Literal object
                    obj = Literal(obj)

                # Add triple to the graph
                g.add((subj, predicate, obj))

# for s,p,o in g.triples((None, None, None)):
#     print(s,p,o)

# Serialize the graph to Turtle format
g.serialize(destination="second_try.ttl", format="ttl")

