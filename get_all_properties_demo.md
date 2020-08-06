# code and an example of the *get_all_properties* function

## 1. code
```python 
def get_all_properties(wiki_id, wikidata_sparql_endpoint):

"""
    query wikidata sparQL end point to get all the properties of the wikidata instance and return a dictionary
    in the folowing format :
    d_properties_wiki = {"wiki_id": 'Q1',
                         "properties": [{"prop_id": 'P31',
                                        "type": 'Classification',
                                        "value": 'bli',
                                        "wiki_id": 'Q2'
                                        },
                                        {"prop_id": 'P17',
                                        "type": 'entity',
                                        "value": 'bla',
                                        "wiki_id": 'Q3'
                                        },
                                        {"prop_id": 'P1561',
                                         "type": 'quantity',
                                         "value": '17',
                                         "wiki_id": '17'
                                         }
                                        ]
                        }

    :param wiki_id: QXXXX representing a Wikidata Instance
    :type wiki_id: str
    :param wikidata_sparql_endpoint: URL where the sparQL server is running
    :type wikidata_sparql_endpoint: str
    :return: dictionary of the properties of the wikidata instance
    {"wiki_id": wiki_id,
     "properties": {"prop_id" : 'Pxxx : Wikidata id of the property',
                    "type": 'The name(label) of a property, eg: country, location',
                    "value": 'value of the property text, quantity or entity',
                    "wiki_id" : 'Qxxx of the value of the property if entity, same with value if quantity'
                    },
     }
    :rtype: dict()
    """

    # SPARQL query
    sparql = SPARQLWrapper.SPARQLWrapper(wikidata_sparql_endpoint, agent="Asrael/1.0 (https://asrael.limsi.fr/) SPARQLWrapper")
    query_result = """
    SELECT ?item ?itemLabel ?propertie_ent ?propertie_label ?value ?valueLabel WHERE {

      VALUES ?item {wd:"""+wiki_id+"""}
      ?item ?p ?event_type.
      ?event_type ?properties ?value.

      FILTER( STRSTARTS(STR(?properties), "http://www.wikidata.org/prop/statement/P") )
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }

      BIND( IRI( REPLACE( STR(?properties), "prop/statement/", "entity/")) as ?propertie_ent )
      ?propertie_ent rdfs:label ?propertie_label.
      FILTER((LANG(?propertie_label)) = "en")

      ?propertie_ent wikibase:propertyType ?type
      FILTER( ?type = wikibase:WikibaseItem || ?type = wikibase:Time || ?type = wikibase:String || ?type = wikibase:Quantity)
    }
    """
    sparql.setQuery(query_result)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    results = sparql.query().convert()
    d_prop = results['results']['bindings']

    # format properties in clean python dictionary
    d_props = {"wiki_id": wiki_id, "properties": [{"prop_id": prop["propertie_ent"]["value"].split('/')[-1],
                                                  "type": prop["propertie_label"]["value"],
                                                  "value": prop["valueLabel"]["value"],
                                                  "wiki_id": prop["value"]["value"].split('/')[-1]}
                                                  for prop in d_prop]}
    return d_props
```

## 2. example
Here, we use the wiki_id: **Q10818**, which describes  [afp.com-20050707T105743Z-TX-SGE-JWQ09](https://github.com/crudnik/asrael) from gold-standard articles

The resutls:

```
{'wiki_id': 'Q10818', 'properties': [{'prop_id': 'P17', 'type': 'country', 'value': 'United Kingdom', 'wiki_id': 'Q145'},
{'prop_id': 'P31', 'type': 'instance of', 'value': 'suicide attack', 'wiki_id': 'Q217327'}, 
{'prop_id': 'P276', 'type': 'location', 'value': 'Liverpool Street tube station', 'wiki_id': 'Q3257126'},
{'prop_id': 'P276', 'type': 'location', 'value': 'Piccadilly line', 'wiki_id': 'Q207689'}, 
{'prop_id': 'P276', 'type': 'location', 'value': 'Tavistock Square', 'wiki_id': 'Q1936696'}, 
{'prop_id': 'P276', 'type': 'location', 'value': 'Edgware Road tube station', 'wiki_id': 'Q1284426'},
{'prop_id': 'P131', 'type': 'located in the administrative territorial entity', 'value': 'London Borough of Camden', 'wiki_id': 'Q202088'}, 
{'prop_id': 'P373', 'type': 'Commons category', 'value': 'London bombing, July 2005', 'wiki_id': 'London bombing, July 2005'}, 
{'prop_id': 'P533', 'type': 'target', 'value': 'civilian', 'wiki_id': 'Q206887'}, 
{'prop_id': 'P910', 'type': "topic's main category", 'value': 'Category:July 2005 London bombings', 'wiki_id': 'Q8568972'}, 
{'prop_id': 'P585', 'type': 'point in time', 'value': '2005-07-07T00:00:00Z', 'wiki_id': '2005-07-07T00:00:00Z'}, 
{'prop_id': 'P8032', 'type': 'victim', 'value': 'Germaine Lindsay', 'wiki_id': 'Q322411'}, 
{'prop_id': 'P8032', 'type': 'victim', 'value': 'Shehzad Tanweer', 'wiki_id': 'Q706780'}, 
{'prop_id': 'P8032', 'type': 'victim', 'value': 'Mohammad Sidique Khan', 'wiki_id': 'Q674709'}, 
{'prop_id': 'P8032', 'type': 'victim', 'value': 'Hasib Hussain', 'wiki_id': 'Q338417'}, 
{'prop_id': 'P7959', 'type': 'historic county', 'value': 'Middlesex', 'wiki_id': 'Q19186'}, 
{'prop_id': 'P8031', 'type': 'perpetrator', 'value': 'Shehzad Tanweer', 'wiki_id': 'Q706780'}, 
{'prop_id': 'P8031', 'type': 'perpetrator', 'value': 'Hasib Hussain', 'wiki_id': 'Q338417'}, 
{'prop_id': 'P8031', 'type': 'perpetrator', 'value': 'Mohammad Sidique Khan', 'wiki_id': 'Q674709'}, 
{'prop_id': 'P8031', 'type': 'perpetrator', 'value': 'Germaine Lindsay', 'wiki_id': 'Q322411'}, 
{'prop_id': 'P1441', 'type': 'present in work', 'value': 'Hereafter', 'wiki_id': 'Q185490'}, 
{'prop_id': 'P1120', 'type': 'number of deaths', 'value': '56', 'wiki_id': '56'}, 
{'prop_id': 'P1339', 'type': 'number of injured', 'value': '700', 'wiki_id': '700'}]}
```
