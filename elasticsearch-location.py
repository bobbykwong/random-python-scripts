from elasticsearch import Elasticsearch
import pandas as pd
import json

# Convert json file to pandas dataframe
with open("schools_raw_1.json") as file:
    data = json.load(file)

trans = pd.DataFrame(data)

es = Elasticsearch(hosts=["http://35.240.189.27:9200"],
                   http_auth=('tingxian', 'pqzmowxn123!'))

def get_latlng_from_ES(es, postal_code):
    query_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"POSTAL": postal_code}}
                ]
            }
        }
    }

    result = es.search(index="buildings_1", body=query_body)

    if len(result['hits']['hits']) == 0:
        print(postal_code)
        return {
            "latitude": "",
            "longitude": ""
        }
    elif result['hits']['hits'][0]['_source']:
        return {
            "latitude": result['hits']['hits'][0]['_source']['LATITUDE'],
            "longitude": result['hits']['hits'][0]['_source']['LONGITUDE']
        } 


for index, row in trans.iterrows():

    latlngObj = get_latlng_from_ES(es, row["postal_code"])
    trans.loc[index, "latitude"] = latlngObj["latitude"]
    trans.loc[index, "longitude"] = latlngObj["longitude"]


trans.to_json('schools_formatted_1.json' ,orient='records')