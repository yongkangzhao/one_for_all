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
    iteration = 0
    while True:
        iteration += 1
        print("\nIteration:", iteration)
        # get the least used prompt
        prompts = json.load(open(args.prompt_path, "r"))
        prompt_counts = db.prompt_counts()
        # merge the used prompts with the prompts
        # {p['prompt']:p['count'] for p in used_prompts_counts}
        for p in prompts:
            if p['prompt'] not in prompt_counts:
                prompt_counts[p['prompt']] = 0.0001
        # sample a least used prompt based on the inverse counts
        least_used_prompt = random.choices(list(prompt_counts.keys()), weights=[1/prompt_counts[p] for p in prompt_counts], k=20)

        #prompts = [{'prompt': 'person seen as [pers...SK] person', 'MASK_TYPE': 'perception', 'prompt_quality': 'good'},...]
        # get the prompt with the least used prompt
        try:
            prompts = [p for p in prompts if p['prompt'] for l in least_used_prompt if p['prompt'] == l]
            
        except:
            print('.', end='')
            continue

        
        for prompt in prompts:
            # get the entities from the prompt
            entities = get_entity_from_prompt(prompt['prompt'])
            if 'MASK' in entities:
                entities.remove('MASK')
            
            entity = {}
            for entity_type in entities:
                if entity_type not in entity:
                    # entity[entity_type] = sample_entity(db, entity_type)
                    entities_samples = db.get_limited_entities(entity_type, 1000)
                    random.shuffle(entities_samples)
                    entity[entity_type] = entities_samples[:100]
                    
            # sample entities:


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
                query_prompt = prompt['prompt']
                for entity_type, ent in query_sample:
                    query_prompt = query_prompt.replace('['+entity_type+']', ent, 1)
                # prompt = prompt['prompt'].format(**entity)
                # print(query_prompt)
                # check if the prompt is already in the database
                if db.check_prompt_exists(query_prompt):
                    print('.',end='')
                    continue

                try:
                    tokens = prober(query_prompt, topk=20, max_new_tokens=50)
                except Exception as e:
                    print("Error: ", e)
                    continue
                print("\n")
                for token in tokens['values']:
                    db.upsert_entity(prompt['MASK_TYPE'], token['token'], prompt['prompt'], query_prompt)
                    print("inserting:", "prompt:", query_prompt, "entity type:", prompt['MASK_TYPE'], token['token'])
                print("\n=====================================")
    


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
