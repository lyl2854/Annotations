"""
After we get the unique entity properties from the 67 schemas, we want to add example values to each 
property to build a small dataset for the future training in the Spacy.
This script extract the property values based on the prop_id.

"""

from SPARQLWrapper import SPARQLWrapper,JSON
import json 
import pandas as pd 

# 1. get all the wiki_event_type
def get_wiki_type(path):
    """
    Based on the schema_descriptions_67sch.json to extract all the wiki event type, return the list of it
    """
    wiki_event_type_list = []
    with open(path,'r') as f:
        # decode json
        schmeas = json.load(f)
        # iterate through all the schemas 
        for schema in schmeas:
            wiki_event_types = schmeas[schema]["wiki_event_types"]
            for key in wiki_event_types.keys():
                wiki_event_type_list.append("wd:"+key)
                
    return wiki_event_type_list

def extract_prop_example(prop,wiki_event_type,wikidata_sparql_endpoint):
    """
    Based on the target property, we extract the property values into a list and return it 

    prop: string of a property id 
    wiki_event_type: string of all the wiki_event_types connected by space with a prefix of wd:
    """
    # SPARQL query
    sparql = SPARQLWrapper(wikidata_sparql_endpoint)
    query_commands = """
        SELECT DISTINCT ?valueLabel WHERE {
        ?item wdt:P17/rdfs:label ?valueLabel .
        FILTER(LANG(?valueLabel) = "en")
        ?item wdt:P31 ?type .
        VALUES ?type"""+"{" + wiki_event_type + "}" +"""
        }
        """
    
    sparql.setQuery(query_commands)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    examples = []
    for result in results["results"]["bindings"]:
        examples.append(result["valueLabel"]["value"])
    
    return examples

def main():
    # 1. get all the wiki event types from the 67 schemas 
    schema_path = './schema_descriptions_67sch.json'
    wiki_event_type = get_wiki_type(schema_path)
    #print(wiki_event_type)
    
    # 2. get all the unique entity properties 
    entity_prop_csv_path = './unique_entity1.CSV'
    df = pd.read_csv(entity_prop_csv_path)
    entity_properties = df["entity"]
    prop_id_list = []
    for prop in entity_properties:
        data = prop.split(",")
        prop_id_list.append(data[-1])
    
    # 3. extract all the examples of the properties 
    wikidata_sparql_endpoint = 'https://query.wikidata.org/sparql'
    wiki_event_type_str = " ".join(wiki_event_type)
    
    examples={}
    for prop_id in prop_id_list:
        examples[prop_id] = extract_prop_example(prop_id,wiki_event_type_str,wikidata_sparql_endpoint)
    print('------------------------------------------------------------------------------------------------')
    print(examples)
    # 4. save all the examples to the txt file
    """
    with open("./examples.txt", 'w') as out:
        out.write() 
    """
 
if __name__ == "__main__":
    main()
