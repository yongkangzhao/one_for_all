from html import entities
from t5 import T5Probe
import argparse
import json
import re
import random
import pymongo
from datetime import datetime
def main(prompts, db):
    print("loading model")
    prober = T5Probe(model_name_or_path="t5-large")
    print("model loaded")
    while True:
        for prompt_template in prompts:
            # prompt_template = random.sample(prompts, 1)[0]
            # print(prompt_template)
            collection = db[prompt_template['MASK_TYPE']]
            collection.create_index("value", unique=True)
            collection.create_index("created_at", unique=False)
            collection.create_index("updated_at", unique=False)
            collection.create_index("status", unique=False)
            collection.create_index("source", unique=False)

            entities = get_entity_from_prompt(prompt_template['prompt'])
            if 'MASK' in entities:
                entities.remove('MASK')
            
            entity = {}
            for entity_type in entities:
                if entity_type not in entity:
                    # entity[entity_type] = sample_entity(db, entity_type)
                    entity[entity_type] = get_limited_entities(db, entity_type, {"disposition":"seed"}, 50)
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
                    collection.update_one({"value": token['token']}, {"$set": data, "$setOnInsert": set_on_insert, "$addToSet":{"source.prompt_template."+prompt_template['prompt']:query_prompt,"disposition": "new"} ,"$inc":{"count":1}}, upsert=True)
                    print(token['token'], end='; ')
                print("\n=====================================")
        break


def get_entity_from_prompt(prompt):
    return re.findall('\[([A-z]*)\]', prompt)

def get_limited_entities(db, entity_type, query={}, limit=0):
    collection = db[entity_type]
    entity = list(collection.aggregate([{"$match":query},{"$sample": {"size": limit}}]))
    return [e['value'] for e in entity]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=27017)
    parser.add_argument("--db", type=str, default="psycho_dev")
    parser.add_argument("--prompt_path", type=str, required=True)


    args = parser.parse_args()

    prompts = json.load(open(args.prompt_path, "r"))
    client = pymongo.MongoClient(args.host, args.port)
    db = client[args.db]
    main(prompts, db)
