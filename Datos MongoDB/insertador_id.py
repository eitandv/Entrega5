import json
import os
dir = os.path.dirname(__file__)

with open(dir + "/messages.json", 'r') as f:
        datastore = json.load(f)

counter = 0
info_list = list()

for elemento in datastore:
    elemento['mid'] = counter
    counter += 1
    info_list.append(elemento)

with open(dir + "/messages.json", 'w') as jsonfile:
    jsonfile.write(json.dumps(info_list, sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False))
