PROMPTS = {
    "START": """Hi, I am your wine assistant. How can I help you?""",

    "Infos": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is asking_info, extract the slots values from the input of the user. The slots are: [name, kind, country, region, color, grape, abv, closure, flavor, style, food_pairing].
""",

    "Food": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is asking_info, extract the slots values from the input of the user. The slots are: [kind, food_paring, year, name, grape, color, style].
""",

    "Order": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is asking_info, extract the slots values from the input of the user. The slots are: [name, quantity, address, phone, gift, pagament].
""",

    "NLU": """Do not invent! If values are not present in the user input, and so they are not specified, you have to put 'null' as value in the slot.
Do not assume any value as default! If they are not specified by the user, put 'null' as value.
Return only the json object composed as {"intent": "", "slots": {}}. 
""", 

    "PRE-NLU": """Break the user input into multiple sentences based on the following intents:
- wine_ordering, if the user wants to buy wine.
- paring_food, if the user wants to know what food pairs with the wine.
- asking_info, if the user wants to know more about the wine.
- out_of_domain, if the input does not match any of the above.
Only provide the sequences of intents, as follow: ["sentence1", "sentence2", ...]
Return only the list.
""",

    "DM": """You are the Dialogue Manager.
Given the output of the NLU component, you should only generate the next best action from this list:
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled
Return only the next best action""",

    "NLG": """You are the NLG component: you must be very polite.
Given the next best action classified by the Dialogue Manager (DM),
you should only generate a lexicalized response for the user.
Possible next best actions are:
- request_info(slot): generate an appropriate question to ask the user for the missing slot value
- confirmation(intent): generate an appropriate confirmation message for the user intent"""
 }
