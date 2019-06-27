import json

# En este archivo transformamos el csv de usuarios en un archivo json

info_list = list()
with open('usuarios.csv',"r",encoding = "UTF-8") as users:
    users.readline()
    for line in users:
        line = line.replace("\n", "").split(",")
        dictionary = {
                    'uid': int(line[0]),
                    'nombre': line[1],
                    'nacimiento': line[2],
                    'correo':line[3],
                    'nacionalidad':line[4]
                    }
        info_list.append(dictionary)

with open ('users.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(info_list, sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False))
