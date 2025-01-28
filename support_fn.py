import json
import re
from intents_classes import Wine_Bottle
import random

def parsing_json(text):
    """
    extract the json from the text
    """

    json_match = re.search(r"{.*}", text, re.DOTALL)

    if json_match:
        extracted_json = json_match.group()
        # Optionally format it without spaces or newlines
        compact_json = json.dumps(json.loads(extracted_json), separators=(',', ':'))
        # convert the json string to a dictionary
        compact_json = json.loads(compact_json)
        return compact_json
    
def can_find_wines(tracker, history):
    """
    check if at least the required slots are filled 
    """
    # Recupera il nome della classe corretta dall'intento precedente nella cronologia
    correct_class_name = history.get_last_int().lower()
    if correct_class_name in tracker.type_for_list:

        # Ottieni l'istanza della classe corretta dal tracker
        correct_class_instance = getattr(tracker, correct_class_name)

        required = correct_class_instance.required()

        if type(required[0]) == list:
            required_list_1 = required[0]
            required_list_2 = required[1]
        else:
            required_list_1 = required
            required_list_2 = []

        # understand if the required fields are filled
        if any(getattr(correct_class_instance, field) is not None for field in required_list_1) and all(getattr(correct_class_instance, field) is None for field in required_list_2):
            return True, required_list_2
        elif any(getattr(correct_class_instance, field) is not None for field in required_list_2) and all(getattr(correct_class_instance, field) is None for field in required_list_1):
            return True, required_list_1
        elif any(getattr(correct_class_instance, field) is not None for field in required_list_1) and any(getattr(correct_class_instance, field) is not None for field in required_list_2):
            # return the list of those that are not None
            list_none = [field for field in required_list_1 + required_list_2 if getattr(correct_class_instance, field) is None]
            return True, list_none
    
    return False, []

def searching_wine(tracker, intent):
    """
    according to the slots, search the wine in the dataset
    """

    dict_info = tracker.dictionary(intent)
    slots = dict_info["slots"]

    with open('WineDataset.json', 'r') as file:
        data = json.load(file)
    
    # filter the data according to the slots
    id_wine = [x for x in range(1, len(data)+1)]

    for index, item in enumerate(data):
        for slot in slots:
            if index+1 not in id_wine:
                break
            field = slot if 'sparkling' not in slot else 'sparkling_still'
            if slots[slot] is not None:
                search = slots[slot].capitalize() if isinstance(slots[slot], str) else slots[slot]
                multiple_search = search.split(',') if ',' in search else [search]
                for s in multiple_search:
                    if s not in item[field.capitalize()]:
                        id_wine.remove(index+1)
                        break

    list_wines = []
    # fill the fields with slots

    full_slots = [field for field in slots if slots[field] is not None] #TODO - field + values
    print('Given this information:')
    for slot in full_slots:
        print(f'\t\t{slot}: {slots[slot]}')

    # fields the ListWines class with slots exept the one in full_slots
    for index, item in enumerate(data):
        if index+1 in id_wine:
            wine = Wine_Bottle()
            for slot in slots:
                field = slot if 'sparkling' not in slot else 'sparkling_still'
                if slots[slot] is None:
                    values = item[field.capitalize()]
                    setattr(wine, slot, values)
            list_wines.append(wine)

    #choose 3 items from the list randomly
    if len(list_wines) > 3:
        rand_int = random.sample(range(0, len(list_wines)), 3)
        list_wines = [list_wines[i] for i in rand_int]
    return list_wines

def assign_field (intent_class: object, field: str, value: str, tracker: object):
    """
    assign the valure to the field if it is in the possible values
    """
    value = str(value) if type(value) == int else value
    # find the correct possible field
    possibilities = intent_class.possibilities()
    for possible_field in possibilities:
        if field in possible_field:
            # check if the value is in the possible values
            if possibilities[possible_field] == True:
                setattr(intent_class, field, value)
                return True
                break
            if possibilities[possible_field] == False:
                if getattr(intent_class, 'quantity') is not None:
                    quantity = int(getattr(intent_class, 'quantity'))
                    print('ok: ', quantity, value)
                    return compare_price_buget(quantity, value, tracker)
                break
            for v in possibilities[possible_field]:
                if v == value or (v == value.lower()):
                    setattr(intent_class, field, value)
                    return True
                    break
            # expanded_search(field, value, intent_class)
            #TODO - RETURN THE VALUE AND THE FIELD
    return False


# def expanded_search(field_to_exclude, value, intent):
#     for new_field in intent.possibilities:
#         if field_to_exclude in new_field:
#             continue

#         for ins in intent.possibilities[new_field]:
#             if ins == value:
#                 setattr(intent, new_field, value)
#                 break

def compare_price_buget(quantity, budget, tracker):
    """
    check if the budget is enough for the quantity
    """
    # retrieve the price of the wine
    dict_info = tracker.dictionary('wine_ordering')
    slots = dict_info["slots"]
    # search for the wine in the dataset
    with open('WineDataset.json', 'r') as file:
        data = json.load(file)

    fields = ['typology', 'title_bottle']
    for f in fields:
        if slots[f] is None:
            fields.remove(f)

    if len(fields) == 0:
        return
    
    price = 0.0
    ids = []
    for index, item in enumerate(data):
        if slots[fields[0]] in item[fields[0].capitalize()]:
            ids.append(index)
            price = float(item['Price']) if price > float(item['Price']) else price
   
    if len(fields) == 2:
        for index, item in enumerate(data):
            if index in ids and slots[fields[1]] in item[fields[1].capitalize()]:
                price = float(item['Price'])
                break

    print(price, budget, quantity)
    if price*quantity > float(budget):
        print('The budget is not enough for the quantity requested')
        print('The maximum quantity that can be purchased is: ', int(float(budget)/price))
        return False
    else:
        print('The budget is enough for the quantity requested')
        setattr('wine_ordering', 'budget', budget)
        return True



    # id_wine = [x for x in range(1, len(data)+1)]
    # for index, item in enumerate(data):
    #     for field in fields:
    #         if index+1 not in id_wine:
    #             break
    #         slot = field
    #         search = slots[slot].capitalize() if isinstance(slots[slot], str) else slots[slot]
    #         multiple_search = search.split(',') if ',' in search else [search]
    #         for s in multiple_search:
    #             if s not in item[field.capitalize()]:
    #                 id_wine.remove(index+1)
    #                 break
    
        
                    


def extract_action_and_argument(input_string):
    """
    used by the DM component, extract the action and the argument from the output string
    """
    # print(input_string)
    ## TODO add check in case there is more in the output string from the LLM
    input_string = input_string.replace("'`", "")
    input_string = input_string.replace("\"", "")
    # print(input_string)
    # Define the regex pattern for extracting action and argument
    pattern = r'(\w+)\((.*?)\)'
    match = re.match(pattern, input_string)
    # print(match)
    if match:
        action = match.group(1)  # Extract the action
        argument = match.group(2)  # Extract the argument
        if '=' in argument:
           argument = argument.split('=')[1]
        # return action, argument
        # arguments = match.group(2).split(',')  # Extract the arguments and split by comma
        # arguments = [arg.strip() for arg in arguments]  # Remove any leading/trailing whitespace
        return action, argument
