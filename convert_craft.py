import argparse
import json
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument('-p','--path',type=str,default='output_json')
parser.add_argument('-t','--table',type=int,default=5)
args = parser.parse_args()

with open(args.path) as f:
    json_data = json.loads(f.read())

with open('data/compiled.json',encoding='utf-8') as f:
    registry = json.loads(f.read())
skill_mapping = registry['skills_mapping']
crafts_mapping = registry['crafts_mapping']
table = crafts_mapping[str(args.table)]
all_items = []
for craft_res in json_data:
    payload = {}
    for slot in craft_res:
        lotId = slot['lotId']
        skillId = slot['skillId']
        val = slot['val']
        if lotId == 0:
            continue
        if skillId == 0:
            skillName = ""
        else:
            skillName = skill_mapping.get(str(skillId),str(skillId))
        lot_name = table[str(lotId)]['name']
        key= lot_name+':'+skillName if skillName else lot_name 
        payload[key] = payload.get(key, table[str(lotId)]['vals'][val])
    all_items.append(payload)
print('\n'.join([str(y) for y in all_items]))
with open(args.path+'.csv','w',encoding="utf-8") as f:
    f.write('\n'.join([str(y) for y in all_items]))
