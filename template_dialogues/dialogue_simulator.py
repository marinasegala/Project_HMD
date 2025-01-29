from utils import generate, load_model, get_args
args = get_args()
model, tokenizer = load_model(args)

prompt = """dialogue state are the values the NLU system extracts from user turns.
A turn is one utterance from either the user or the system.
Generate a dialogue of 6 turns (3 user turns and 3 system turns)
that has the following dialogue state by the end of 6 turns
"""

input = """dialogue_state = {
    "intent": "pizza_ordering",
    "slots": {
        "pizza_type": "salamino",
        "pizza_size": "medium",
        "pizza_count": 3
    }
}"""

# Format and tokenize the input
input_text = args.chat_template.format(prompt, input)
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

# Generate a response
response = generate(model, inputs, tokenizer, args)
print(response)

# DETAILS

input1 = """dialogue_state = {
    "intent": "wine_details",
    "slots": {
        "flavor": "",
        "grape": "",
        "color": "white",
        "sparkling": "yes",
        "abv": "unknown",
        "year": "",
        "typology": ""
        "giving_list_wine": ""
    }
}"""

input2 = """dialogue_state = {
    "intent": "wine_details",
    "slots": {
        "flavor": "floral",
        "grape": "Pinot Grigio",
        "color": "",
        "sparkling": "",
        "abv": "",
        "year": "",
        "typology": ""
        "giving_list_wine": ""
    }
}"""

input3 = """dialogue_state = {
    "intent": "wine_details",
    "slots": {
        "flavor": "",
        "grape": "Chardonnay",
        "color": "",
        "sparkling": "still",
        "abv": "",
        "year": "",
        "typology": ""
        "giving_list_wine": ""
    }
}"""

input4 = """dialogue_state = {
    "intent": "wine_details",
    "slots": {
        "flavor": "",
        "grape": "Merlot",
        "color": "red",
        "sparkling": "",
        "abv": "13.00",
        "year": "2014",
        "typology": ""
        "giving_list_wine": ""
    }
}"""


# ORIGIN

input4 = """dialogue_state = {
    "intent": "wine_origin",
    "slots": {
        "region": "Tuscany",
        "country": "Italy",
        "color": "",
        "typology": ""
        "title_bottle": ""
    }
}"""

input5 = """dialogue_state = {
    "intent": "wine_origin",
    "slots": {
        "region": "",
        "country": "France",
        "color": "white",
        "typology": ""
        "title_bottle": ""
    }
}"""

input6 = """dialogue_state = {
    "intent": "wine_origin",
    "slots": {
        "region": "Bordeaux",
        "country": "France",
        "color": "",
        "typology": "Saint-Émilion",
        "title_bottle": ""
    }
}"""

input7 = """dialogue_state = {
    "intent": "wine_origin",
    "slots": {
        "region": "",
        "country": "",
        "color": "",
        "typology": "",
        "title_bottle": "Primo Rosso Appassimento"
    }
}"""

# PRODUCTION

input8 = """dialogue_state = {
    "intent": "wine_production",
    "slots": {
        "grape": "",
        "abv": "12.50",
        "closure": "",
        "typology": "",
    }
}"""

input9 = """dialogue_state = {
    "intent": "wine_production",
    "slots": {
        "grape": "Chardonnay",
        "abv": "",
        "closure": "natural cork",
        "typology": "",
    }
}"""

input10 = """dialogue_state = {
    "intent": "wine_production",
    "slots": {
        "grape": "Syrah",
        "abv": "",
        "closure": "",
        "typology": "",
    }
}"""

input11 = """dialogue_state = {
    "intent": "wine_production",
    "slots": {
        "grape": "",
        "abv": "12.00",
        "closure": "Synthetic Cork",
        "typology": "",
    }
}"""

# CONSERVATION

input12 = """dialogue_state = {
    "intent": "wine_conservation",
    "slots": {
        "fridge": "no",
        "celler": "no",
        "temperature": "",
        "typology": ""
    }
}"""

input13 = """dialogue_state = {
    "intent": "wine_conservation",
    "slots": {
        "fridge": "yes",
        "celler": "",
        "temperature": "7",
        "typology": ""
    }
}"""

input14 = """dialogue_state = {
    "intent": "wine_conservation",
    "slots": {
        "fridge": "no",
        "celler": "yes",
        "temperature": "",
        "typology": ""
    }
}"""

# CHOOSING FOOD

input15 = """dialogue_state = {
    "intent": "wine_paring",
    "slots": {
        "style": "light",
        "color": "red",
        "typology": "Ripasso",
        "food": ""
    }
}"""

input16 = """dialogue_state = {
    "intent": "wine_paring",
    "slots": {
        "style": "",
        "color": "white",
        "typology": "",
        "food": "fish"
    }
}"""

input17 = """dialogue_state = {
    "intent": "wine_paring",
    "slots": {
        "style": "",
        "color": "",
        "typology": "Valpolicella",
        "food": ""
    }
}"""

input18 = """dialogue_state = {
    "intent": "wine_paring",
    "slots": {
        "style": "",
        "color": "",
        "typology": "",
        "food": "cheese"
    }
}"""

# ORDERING (+ DELIVERY)

input19 = """dialogue_state = {
    "intent": "wine_ordering",
    "slots": {
        "typology": "",
        "quantity": 2,
        "total_budget": "",
        "title_bottle": "La Toledana Gavi di Gavi DOCG"
    }
}"""

input20 = """dialogue_state = {
    "intent": "wine_ordering",
    "slots": {
        "typology": "Primitivo",
        "quantity": "",
        "total_budget": "50",
        "title_bottle": ""
    }
}"""

input21 = """dialogue_state = {
    "intent": "wine_ordering",
    "slots": {
        "typology": "Côtes De Provence",
        "quantity": 1,
        "total_budget": "67",
        "title_bottle": "Miraval Rosé"
    }
}"""