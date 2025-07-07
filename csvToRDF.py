import os
import pprint
import csv 
import hashlib
import rdflib
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC

# Namespaces 
BASE = Namespace("https://w3id.org/salemWitchTrials/")

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
    "viaf": Namespace("http://viaf.org/viaf/"),
    "lode": Namespace("http://linkedevents.org/ontology/")
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


# Entities mapping 
mapping_entities = {}
with open("mapping_entities.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mapping_entities[row["object"]] = row["entity"]


# List for our items
csv_items = []
csv_items_prefix = "item/"

always_literal = ["has title"]

# Read CSVs in folder
folder = "csv_files"
for file in os.listdir(folder):
    if file.endswith(".csv"):
        # Initialize RDF graph
        g = rdflib.Graph()
        for prefix, ns in namespaces.items():
            g.bind(prefix, ns)

        path = os.path.join(folder, file)
        with open(path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subj_str = row["subject"].strip().replace(" ", "_")
                subj = URIRef(BASE + csv_items_prefix + subj_str)
                pred = row["predicate"].strip()
                obj = row["object"].strip()

                # Track subjects to recognize them later
                item = row["subject"]
                csv_items.append(item)

                # Replace natural language predicate with property
                if pred in predicate_map:
                    predicate = predicate_map[pred]
                else:
                    print(f"Unknown predicate '{pred}'") # If predicate match is missing
                    predicate = RDFS.comment

                # Check if object is entity or literal
                # Just for titles
                if pred in always_literal:
                    object = Literal(obj)
                else:
                # If it's an item from our ontology
                    if obj in csv_items:
                        # create URIRef from base for it
                        object = URIRef(BASE + csv_items_prefix + obj.replace(" ", "_"))
                    elif obj in mapping_entities:
                        entity = mapping_entities[obj]
                        if ":" not in entity:
                            # Simply use the base URI to create the object
                            object = URIRef(BASE[entity])
                        else:
                            # Else split namespace and entity
                            namespace_str, entity_str = entity.split(":")
                            namespace = namespaces[namespace_str]
                            # Create object URI
                            object = URIRef(namespace + entity_str)
                    else:
                        # Otherwise create a Literal object
                        object = Literal(obj)

                # Add triple to the graph
                g.add((subj, predicate, object))

                # for s,p,o in g.triples((None, None, None)):
                #     print(s,p,o)

    # Serialize the graph to Turtle format
    ttl_filename = os.path.splitext(file)[0] + ".ttl"
    g.serialize(destination=os.path.join("items_ttls", ttl_filename), format="ttl", base=BASE) 



