# import pandas as pd
import json

def extract_db_init(field):
    with open('WineDataset.json', 'r') as file:
        data = json.load(file)
    
    #capitalize each word
    field = field.capitalize() 
    list_values = list(set(item[field] for item in data if field in item))
    list_values = [x for x in list_values if str(x) != 'nan' and x != '']
    new_list = []
    for x in list_values:
        if ',' in x:
            adding = x.split(', ')
            for i in adding:
                if i not in new_list:
                    new_list.append(i)
        elif x not in new_list:
            new_list.append(x)

    # separate the values of the same element in the list
    #remove nan values from list

    if type(new_list[0]) == str:
        new_list = [x.lower() for x in new_list]

    return new_list + ['unknown']
