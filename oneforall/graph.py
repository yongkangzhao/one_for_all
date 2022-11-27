import argparse
from postgresAPI import PostgresAPI
import re
import pandas as pd

prompt_to_graph_df = pd.read_csv('prompt_to_graph.csv', index_col=0)

def entity_extractor(prompt_template, prompt):
    entities = re.findall(r'\[.*?\]', prompt_template)
    for entity in entities:
        if entity == '[MASK]':
            continue
        left,right = prompt_template.split(entity)
        break
    extracted_entity = prompt.replace(left, '').replace(right, '')
    return {'entity': extracted_entity, 'type': entity}


def get_triples(meta):
    # meta = {'entity_type': 'occupation', 'Occupation requiring [ncskills] skills: [MASK] and ': {'count': 12, 'Occupation requiring concentration skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring problem solving skills: [MASK] and ': {'Accounting': {'count': 2}}, 'Occupation requiring computer literacy skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring critical thinking skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring computer knowledge skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring in-depth knowledge skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring specialized knowledge skills: [MASK] and ': {'Accounting': {'count': 1}}, 'Occupation requiring the ability to analyze skills: [MASK] and ': {'Accounting': {'count': 3}}, 'Occupation requiring high level of knowledge skills: [MASK] and ': {'Accounting': {'count': 1}}}}
    triples = []
    for prompt_template, value in meta.items():
        if prompt_template == 'entity_type':
            continue
        for prompt, v in value.items():
            if prompt == 'count':
                continue
            extraction = entity_extractor(prompt_template, prompt)
            mask_entity = list(v.keys())[0]

            # check the triple relation type
            row = prompt_to_graph_df[prompt_to_graph_df['prompt'] == prompt_template]

            mask_type = row['MASK_TYPE'].values[0]
            head_type = row['head'].values[0]
            relation = row['relation'].values[0]
            tail_type = row['tail'].values[0]

            # check the triple relation type
            if extraction['type'][1:-1] == head_type and mask_type == tail_type:
                subject = extraction['entity']
                object = mask_entity
            elif extraction['type'][1:-1] == tail_type and mask_type == head_type:
                subject = mask_entity
                object = extraction['entity']
            
            triples.append((subject, relation, object))
    return triples
            


   

#dbname, user, password, host, port):
def main(dbname, user, password, host, port):
    db = PostgresAPI(dbname, user, password, host, port)
    samples = db.get_samples('triple classification', 'Positive', 10000)
    file = open('triples.txt', 'w')
    for meta in samples['meta']:
        # print(meta)
        triples = get_triples(meta)
        for triple in triples:
            file.write(str(triple)+'\n')
    file.close()
            
    





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dbname', type=str, default='postgres')
    parser.add_argument('--user', type=str, default='postgres')
    parser.add_argument('--password', type=str, default='postgres')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=str, default='5432')
    args = parser.parse_args()
    triples = main(args.dbname, args.user, args.password, args.host, args.port)
    print(triples)