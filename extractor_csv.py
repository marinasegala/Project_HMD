import pandas as pd

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

# def extract_database(field, value):
#     data = pd.read_csv('dataset2.csv')
#     # first letter to uppercase
#     field = field.capitalize()
#     list_values = data[field].unique()
#     #remove nan values from list
#     list_values = [x for x in list_values if str(x) != 'nan']

#     if type(list_values[0]) == str:
#         print(list_values[0])
#         list_values = [x.lower() for x in list_values]
#         print(list_values[0])
    
#     # print(list_values)
#     if type(value) == str:
#         value = value.lower()

#     # return the value if it is an element of the list
#     for x in list_values:
#         if x == value:
#             return x

#     return None

def searching_wine(tracker, intent):
    dict_info = tracker.dictionary(intent)
    slots = dict_info["slots"]

    data = pd.read_csv('chatbots/dataset2.csv')
    
    # filter the data according to the slots
    list_wine = [x for x in range(1, len(data)+1)]


    for index, row in data.iterrows():
        for slot in slots:
            if slots[slot] != None:
                if str(row[slot.capitalize()]) == 'nan':
                    list_wine.remove(index+1)
                    continue
                search = slots[slot].capitalize() if type(slots[slot]) == str else slots[slot]
                if search not in row[slot.capitalize()]:
                    list_wine.remove(index+1)

    return list_wine