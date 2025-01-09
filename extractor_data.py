# import pandas as pd
import json

def extract_db_init(field):
    with open('FinalWineDataset.json', 'r') as file:
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
'''
def extract_db_init(field):
    data = pd.read_csv('chatbots/dataset2.csv')
    #capitalize each word
    field = field.capitalize() 
    list_values = list(data[field].unique())
    list_values = [x for x in list_values if str(x) != 'nan']
    new_list = []
    for x in list_values:
        if ',' in x:
            adding = x.split(', ')
            for i in adding:
                if i not in new_list:
                    new_list.append(i)
        else:
            new_list.append(x)

    # separate the values of the same element in the list
    #remove nan values from list


    if type(new_list[0]) == str:
        new_list = [x.lower() for x in new_list]

    return new_list + ['unknown']

def searching_wine(tracker, intent):
    dict_info = tracker.dictionary(intent)
    slots = dict_info["slots"]

    data = pd.read_csv('chatbots/dataset2.csv')
    
    # filter the data according to the slots
    list_wine = [x for x in range(1, len(data)+1)]

    for index, row in data.iterrows():
        for slot in slots:
            field = slot.split('_')[0] if '_' in slot else slot
            if slots[slot] != None:
                if str(row[field.capitalize()]) == 'nan':
                    list_wine.remove(index+1)
                    continue
                search = slots[slot].capitalize() if type(slots[slot]) == str else slots[slot]
                if search not in row[field.capitalize()]:
                    list_wine.remove(index+1)

    return list_wine
'''