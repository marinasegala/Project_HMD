import requests
import json
import re

def generate_response_Ollama(prompt, model="llama3.1:70b"):
    
    url = "http://10.234.0.160:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        text = response.json()
        return text.get("response", "")
        # return response.json().get("generated_text", "")
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return ""

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

def searching_wine(tracker, intent):
    """
    according to the slots, search the wine in the dataset
    """

    dict_info = tracker.dictionary(intent)
    slots = dict_info["slots"]

    with open('FinalWineDataset.json', 'r') as file:
        data = json.load(file)
    
    # filter the data according to the slots
    list_wine = [x for x in range(1, len(data)+1)]

    for index, item in enumerate(data):
        for slot in slots:
            field = slot.split('_')[0] if '_' in slot else slot
            if slots[slot] is not None:
                if str(item.get(field.capitalize(), 'nan')) == 'nan':
                    list_wine.remove(index+1)
                    continue
                search = slots[slot].capitalize() if isinstance(slots[slot], str) else slots[slot]
                if search not in item[field.capitalize()]:
                    list_wine.remove(index+1)

    return list_wine    

def assign_field (intent: object, field: str, value: str):
    """
    assign the valure to the field if it is in the possible values
    """

    # find the correct possible field
    for possible_field in intent.possibilities:
        if field in possible_field:
            # check if the value is in the possible values
            for ins in intent.possibilities[possible_field]:
                if ins == value or (ins == value.lower()):
                    setattr(intent, field, value)
                    break
            expanded_search(field, value, intent)
            break

def expanded_search(field_to_exclude, value, intent):
    for new_field in intent.possibilities:
        if field_to_exclude in new_field:
            continue

        for ins in intent.possibilities[new_field]:
            if ins == value:
                setattr(intent, new_field, value)
                break

def extract_action_and_argument(input_string):
    """
    used by the DM component, extract the action and the argument from the output string
    """
    ## TODO add check in case there is more in the output string from the LLM
    # Remove any ' characters from the input string
    input_string = input_string.replace("'", "")
    input_string = input_string.replace("\"", "")
    # Define the regex pattern for extracting action and argument
    pattern = r'(\w+)\(([\w\s=]+)\)' #r'(\w+)\((.*)\)\s*=\s*(.*)' #r'(\w+)\((\w+)\)'
    match = re.match(pattern, input_string)
    
    if match:
        action = match.group(1)  # Extract the action
        argument = match.group(2)  # Extract the argument
        if '=' in argument:
            argument = argument.split('=')[1]
        return action, argument