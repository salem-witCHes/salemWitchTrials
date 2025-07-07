import xml.etree.ElementTree as ET
import rdflib
from rdflib.namespace import FOAF, RDF, RDFS, XSD, DC, OWL
from rdflib import URIRef, Literal, Namespace, Graph


# defining namespaces
TEI = Namespace("http://www.tei-c.org/ns/1.0")
ns = {"tei": TEI}
schema = Namespace("https://schema.org/")
my_ns = Namespace("https://w3id.org/salemWitchTrials/")
lode = Namespace("http://linkedevents.org/ontology/")

# parsing the XML file
tree = ET.parse("aShortHistory.xml")
root = tree.getroot()
my_graph = Graph()

# bind() = a method on the graph that associates a short prefix name with a full namespace URI
my_graph.bind("tei", TEI)
my_graph.bind("schema", schema)
my_graph.bind("my_ns", my_ns)
my_graph.bind("lode", lode)

# teiHeader -> bibliographic information
bibl = root.find(".//tei:sourceDesc/tei:bibl", ns)

main_title = bibl.findall("tei:title[@type='main']", ns)
sub_title = bibl.findall("tei:title[@type='sub']", ns)
titles = main_title + sub_title

full_title = ""
for title in titles:
    full_title += title.text

author = bibl.find("tei:author", ns).text
publisher = bibl.find("tei:publisher", ns).text
pub_date = bibl.find("tei:date", ns).attrib.get("when")
source_link = bibl.find("tei:idno", ns).text

# tei text
text = root.find(".//tei:text/tei:body", ns)
book_comment = text.find("tei:div[@type='page'][@n='1']/tei:p[@n='3']", ns)
full_comment = "".join(book_comment.itertext())
trials_comment = text.find("tei:div[@type='page'][@n='2']/tei:p[@n='3']", ns).text

# creating the uri of the metadata
doc_uri = my_ns.A_Short_History
author_uri = my_ns.Author
publisher_uri = my_ns.Publisher

# adding metadata to the graph
my_graph.add((doc_uri, RDF.type, schema.CreativeWork))
my_graph.add((doc_uri, schema.name, Literal(full_title)))
my_graph.add((doc_uri, schema.author, author_uri))
my_graph.add((doc_uri, schema.publisher, publisher_uri))
my_graph.add((doc_uri, schema.datePublished, Literal(pub_date, datatype=XSD.gYear)))
my_graph.add((doc_uri, schema.archivedAt, URIRef(source_link)))
my_graph.add((doc_uri, schema.description, Literal(full_comment)))

# author and publisher info
my_graph.add((author_uri, RDF.type, FOAF.Person))
my_graph.add((author_uri, FOAF.name, Literal(author)))

my_graph.add((publisher_uri, RDF.type, FOAF.Agent))
my_graph.add((publisher_uri, FOAF.name, Literal(publisher)))


# extraction of persons and places
persons = root.findall(".//tei:listPerson/tei:person", ns)
places = root.findall(".//tei:listPlace/tei:place", ns)

# adding places + persons to the graph
for person in persons:
    person_id = person.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
    person_uri = my_ns[f"person/{person_id}"]
    name = person.find("tei:persName", ns).text
    same_as = person.attrib.get("sameAs", None)

    my_graph.add((person_uri, RDF.type, FOAF.Person))
    my_graph.add((person_uri, FOAF.name, Literal(name)))
    if same_as:
        my_graph.add((person_uri, OWL.sameAs, URIRef(same_as)))

    # birth info
    birth = person.find("tei:birth", ns)
    if birth is not None:
        birth_date = birth.find("tei:date", ns)
        birth_place = birth.find("tei:placeName", ns)
        if birth_date is not None:
            when = birth_date.attrib.get("when")
            if when:
                my_graph.add((person_uri, schema.birthDate, Literal(when)))
            elif birth_date.text:
                my_graph.add((person_uri, schema.birthDate, Literal(birth_date.text.strip())))

        if birth_place is not None:
            birth_place_ref = birth_place.attrib.get("ref", "").lstrip("#")
            if birth_place_ref:
                my_graph.add((person_uri, schema.birthPlace, my_ns[f"place/{birth_place_ref}"]))
        
    # death info
    death = person.find("tei:death", ns)
    if death is not None:
        death_date = death.find("tei:date", ns)
        when = death_date.attrib.get("when")
        death_place = death.find("tei:placeName", ns)
        if death_date is not None:
            my_graph.add((person_uri, schema.deathDate, Literal(when, datatype=XSD.date)))
        if death_place is not None:
            death_place_ref = death_place.attrib.get("ref", "").lstrip("#")
            my_graph.add((person_uri, schema.deathPlace, my_ns[f"place/{death_place_ref}"]))

    note = person.find("tei:note/tei:quote", ns)
    if note is not None:
        quote_text = note.text.strip()
        source_url = note.attrib.get("source", None)

        my_graph.add((person_uri, RDFS.comment, Literal(quote_text)))

        if source_url:
            my_graph.add((person_uri, schema.citation, URIRef(source_url)))

for place in places:
    place_id = place.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
    place_uri = my_ns[f"place/{place_id}"]
    place_name = place.find("tei:placeName", ns).text
    same_as = place.attrib.get("sameAs", None)

    my_graph.add((place_uri, RDF.type, schema.Place))
    my_graph.add((place_uri, schema.name, Literal(place_name)))
    if same_as:
        my_graph.add((place_uri, OWL.sameAs, URIRef(same_as)))

# events
main_event = root.find(".//tei:profileDesc/tei:listEvent/tei:event[@type='main']", ns)

if main_event is not None:
    trials_uri = my_ns["event/salem_witch_trials"]
    my_graph.add((trials_uri, RDF.type, lode.Event))

    name = main_event.find("tei:eventName", ns)
    place = main_event.find("tei:place/tei:placeName", ns)
    agent = main_event.find("tei:person/tei:persName", ns)
    start_date = main_event.attrib.get("from")
    end_date = main_event.attrib.get("to")

    my_graph.add((trials_uri, schema.name, Literal(name.text.strip())))
    my_graph.add((trials_uri, lode.atPlace, Literal(place.text.strip())))
    my_graph.add((trials_uri, lode.involvedAgent, Literal(agent.text.strip())))
    my_graph.add((trials_uri, schema.startDate, Literal(start_date)))
    my_graph.add((trials_uri, schema.endDate, Literal(end_date)))
    my_graph.add((trials_uri, schema.description, Literal(trials_comment)))

    sub_event = root.find(".//tei:profileDesc/tei:listEvent/tei:event[@type='sub']", ns)
    if sub_event is not None:
        trial_eh = my_ns["event/trial_of_EH"]
        my_graph.add((trial_eh, RDF.type, lode.Event))
        my_graph.add((trials_uri, schema.subEvent, trial_eh))

        sub_name = sub_event.find("tei:eventName", ns)
        sub_agent = sub_event.find("tei:person/tei:persName", ns)
        sub_time = sub_event.attrib.get("when")
        
        my_graph.add((trial_eh, lode.involvedAgent, Literal(sub_agent.text.strip())))
        my_graph.add((trial_eh, schema.name, Literal(sub_name.text.strip())))
        my_graph.add((trial_eh, lode.atTime, Literal(sub_time)))

my_graph.serialize(destination="salem_witch_trials.ttl", format="turtle")
# print(my_graph.serialize(format="turtle"))
