from html import entities
from t5 import T5Probe
import argparse
import json
import re
import random
import psycopg
from postgresAPI import PostgresAPI

from datetime import datetime
def main(args):

    db = PostgresAPI(args.database, args.user, args.password, args.host, args.port)

    prompts = json.load(open(args.prompt_path, "r"))
    
    
    print("loading model")
    prober = T5Probe(model_name_or_path="t5-large")
    print("model loaded")
    while True:
        for prompt_template in prompts:

            entities = get_entity_from_prompt(prompt_template['prompt'])
            if 'MASK' in entities:
                entities.remove('MASK')
            
            entity = {}
            for entity_type in entities:
                if entity_type not in entity:
                    # entity[entity_type] = sample_entity(db, entity_type)
                    entity[entity_type] = db.get_limited_entities(entity_type, 50)
                    
            # print(entity)
            entity_sample = [[]]
            for entity_type in entities:
                temp = []
                for t in entity_sample:
                    for e in entity[entity_type]:
                        t_temp = t.copy()
                        t_temp.append([entity_type, e])
                        temp.append(t_temp)
                entity_sample = temp

            for query_sample in entity_sample:
                query_prompt = prompt_template['prompt']
                for entity_type, ent in query_sample:
                    query_prompt = query_prompt.replace('['+entity_type+']', ent, 1)
                # prompt = prompt_template['prompt'].format(**entity)
                print(query_prompt)
                try:
                    tokens = prober(query_prompt, topk=20, max_new_tokens=50)
                except Exception as e:
                    print("Error: ", e)
                    continue
                for token in tokens['values']:
                    data = {
                        "value": token['token'],
                        "updated_at": datetime.now(),
                    }
                    set_on_insert = {
                            "created_at": datetime.now(),
                            "status": "new",
                    }
                    # collection.update_one({"value": token['token']}, {"$set": data, "$setOnInsert": set_on_insert, "$addToSet":{"source.prompt_template."+prompt_template['prompt']:query_prompt,"disposition": "new"} ,"$inc":{"count":1}}, upsert=True)
                    db.upsert_entity(prompt_template['MASK_TYPE'], token['token'], prompt_template['prompt'], query_prompt)
                    print(token['token'], end='; ')
                print("\n=====================================")
        break


def get_entity_from_prompt(prompt):
    return re.findall('\[([A-z.]*)\]', prompt)

def get_limited_entities(db, entity_type, query={}, limit=0):
    collection = db[entity_type]
    entity = list(collection.aggregate([{"$match":query},{"$sample": {"size": limit}}]))
    return [e['value'] for e in entity]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--database", type=str, default="postgres")
    parser.add_argument("--user", type=str, default="postgres")
    parser.add_argument("--password", type=str, default="postgres")
    parser.add_argument("--prompt_path", type=str, required=True)
    args = parser.parse_args()
    main(args)
