import argparse
import json
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument('-p','--path',type=str,default='output_json')
args = parser.parse_args()

with open(args.path) as f:
    json_data = json.loads(f.read())

with open('data/compiled.json',encoding='utf-8') as f:
    registry = json.loads(f.read())
skill_mapping = registry['skills_mapping']
all_items = []
for pot in json_data:
    for item in pot:
        if item['skill1'] == 0 and item['skill2'] == 0:
            continue
        for k in ['skill1','skill2']:
            key = str(item[k])
            item[k] = skill_mapping.get(key,key)
        all_items.append(item)
pd.DataFrame(all_items).to_csv(args.path+'.csv')
