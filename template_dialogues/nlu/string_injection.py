from itertools import product

# pizza-count, pizza-type
# template1 = "I would like to order {} {} pizza."
# ds = {
#     "intent": "pizza_ordering",
#     "slots": {
#         "pizza_type": "",
#         "pizza_size": None,
#         "pizza_count": ""
#     },
# }
# pizza_count = ["a", "1", "2"]
# pizza_type = ["salamino", "margherita", "capricciosa", "vegetariana", ""]

# for c, t in product(pizza_count, pizza_type):
#     filled_template = template1.format(c, t)
#     ds["slots"]["pizza_type"] = t
#     ds["slots"]["pizza_count"] = int(c) if c.isdigit() else 1
#     print(filled_template)
#     print(ds)
#     print()

# DETAILS
'''
temp2 = "I want some information about a {} wine. {} {} {} {}"

ds2 = {
    "intent": "wine_details",
    "slots": {
        "flavor": None,
        "grape": "",
        "color": "",
        "sparkling": "",
        "abv": "",
        "year": "",
        "typology": ""
    }
}

color = ["white", "red", ""]
sparkling = ["It is sparkling", "It is still", ""]
typology = ["It's a Primitivo", "It's a Champagne", "It's a Prosecco", ""]
grape = ["The grape is Chardonnay", "The grape is Pinot Noir", "The grape is Valdobbiadene", ""]
year = ["Made in 2019", "Made in 2020", "Made in 2021", ""]

for c, s, t, g, y in product(color, sparkling, typology, grape, year):
    filled_template = temp2.format(c, s, t, y, g)
    ds2["slots"]["grape"] = g[13:]
    ds2["slots"]["color"] = c

    # sparkling has to be a yes, no, or empty string
    ds2["slots"]["sparkling"] = "yes" if "sparkling" in s else "no" if "still" in s else ""
    ds2["slots"]["typology"] = t[7:]
    ds2["slots"]["year"] = y[8:]

    # ds2["slots"]["pizza_count"] = int(c) if c.isdigit() else 1
    # save in a txt file
    with open("wine_details.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_details_json.txt", "a") as f:
        f.write(str(ds2) + "\n")
'''
# ORIGIN
'''
temp2 = "Can you tell me the origin of a {} wine?"
temp3 = "I want to know a{} wine from {} {}."
ds3 = {
    "intent": "wine_origin",
    "slots": {
        "region": "",
        "country": "",
        "color": "",
        "typology": "",
        "title_bottle": None
    }
}

region = ["Tuscany", "Champagne", ""]
country = [", Italy", ", France", ""]
color = [" white", " red", " rose", ""]
#---
typology = ["Primitivo", "Champagne", "Prosecco", ""]

for t in typology:
    filled_template = temp2.format(t)
    ds3["slots"]["typology"] = t

    with open("wine_origin.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_origin_json.txt", "a") as f:
        f.write(str(ds3) + "\n")

for c, r, col in product(country, region, color):
    if c == "" and r == "":
        continue
    filled_template = temp3.format(col, r, c)
    ds3["slots"]["country"] = c[2:]
    ds3["slots"]["region"] = r
    ds3["slots"]["color"] = col[1:]

    with open("wine_origin.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_origin_json.txt", "a") as f:
        f.write(str(ds3) + "\n")
'''
# PRODUCTION
'''
temp3 = "Can you tell me other info about the production of a wine? {} {} {}"
ds = {
    "intent": "wine_production",
    "slots": {
        "grape": "",
        "abv": None,
        "closure": "",
        "typology": "",
    }
}

closure = ["conserved in natural cork", "conserved in screwcap", "conserved in vinolok", ""]
grape = ["Chardonnay grape", "Pinot Noir grape", "Valdobbiadene grape", ""]
#---
typology = ["It is a Primitivo", "It is a Champagne", "It is a Prosecco", ""]

for c, g, t in product(closure, grape, typology):
    filled_template = temp3.format(t, c, g)
    ds["slots"]["closure"] = c[13:]
    ds["slots"]["grape"] = g[:10]
    ds["slots"]["typology"] = t[8:]

    with open("wine_production.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_production_json.txt", "a") as f:
        f.write(str(ds) + "\n")
'''

# CONSERVATION
'''
temp = 'Wine that to keep {} {}'
temp2 = 'How i can conserve a {} wine?'
ds = {
    "intent": "wine_conservation",
    "slots": {
        "fridge": "",
        "celler": "",
        "temperature": "",
        "typology": ""
    }
}

fridge = ["not in the fridge", "in the fridge", '']
celler = ["not in the celler", "in the celler", '']

typology = ["Primitivo", "Champagne", "Prosecco", ""]

for t in typology:
    filled_template = temp2.format(t)
    ds["slots"]["typology"] = t

    with open("wine_conservation.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_conservation_json.txt", "a") as f:
        f.write(str(ds) + "\n")

for c, f in product(fridge, celler):
    if c == "" and f == "":
        print("skipping")
    else:
        filled_template = temp.format(c, f)
        ds["slots"]["celler"] = 'no' if "not" in c else 'yes' if "in" in c else ''
        ds["slots"]["fridge"] = 'no' if "not" in f else 'yes' if "in" in f else ''

        with open("wine_conservation.txt", "a") as f:
            f.write(filled_template + "\n")
        
        with open("wine_conservation_json.txt", "a") as f:
            f.write(str(ds) + "\n")
'''
# CHOOSING FOOD

# temp = 'I want to drink a {} wine, which food should I choose?'
# temp2 = 'I want to eat {}, tell me the wine to drink.'
# ds = {
#     "intent": "choosing_food",
#     "slots": {
#         "style": "",
#         "color": "",
#         "typology": "",
#         "food": ""
#     }
# }
# food = ["aperitif", "fish", "desser"]
# color = ["white", "red", "rose"]
# typology = ["Primitivo", "Champagne", "Prosecco"]

# for t in typology:
#     filled_template = temp.format(t)
#     ds["slots"]["typology"] = t

#     with open("wine_paring.txt", "a") as f:
#         f.write(filled_template + "\n")
    
#     with open("wine_paring_json.txt", "a") as f:
#         f.write(str(ds) + "\n")
# for t in color:
#     filled_template = temp.format(t)
#     ds["slots"]["typology"] = t

#     with open("wine_paring.txt", "a") as f:
#         f.write(filled_template + "\n")
    
#     with open("wine_paring_json.txt", "a") as f:
#         f.write(str(ds) + "\n")

# for f in food:
#     filled_template = temp2.format(f)
#     ds["slots"]["food"] = f
#     with open("wine_paring.txt", "a") as f:
#         f.write(filled_template + "\n")
#     with open("wine_paring_json.txt", "a") as f:
#         f.write(str(ds) + "\n")
# for c, f in product(fridge, celler):
#     filled_template = temp.format(t, c, g)
#     ds["slots"]["closure"] = c[13:]
#     ds["slots"]["grape"] = g[:10]
#     ds["slots"]["typology"] = t[8:]

#     with open("wine_conservation.txt", "a") as f:
#         f.write(filled_template + "\n")
    
#     with open("wine_conservation_json.txt", "a") as f:
#         f.write(str(ds) + "\n")

#ORDERING   

temp = 'I want to buy {} bottles of {} wine. {}'
ds = {
    "intent": "wine_ordering",
    "slots": {
        "typology": "",
        "quantity": "",
        "total_budget": "", 
        "title_bottle": ""
    }
}
qnt = [1, 5, '']
typology = ["Prosecco", ""]
total_budget = ['My total budget is 100', 'My total budget is 40', '']
for q, t, b in product(qnt, typology, total_budget):
    filled_template = temp.format(q, t, b)
    ds["slots"]["typology"] = t
    ds["slots"]["quantity"] = q
    ds["slots"]["total_budget"] = b[19:]

    with open("wine_ordering.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("wine_ordering_json.txt", "a") as f:
        f.write(str(ds) + "\n")

#DELIVERY
temp = '{} {} {} {}'
ds = {
    "intent": "delivery",
    "slots": {
        "address": "",
        "phone": "",
        "gift": "",
        "kind_pagament": ""
    }
}
address = ["My address is Via Roma 1", ""]
phone = ["My phone number is 333444555", ""]
gift = ["This is order is a gift", "This is not a gift", "This order is for me", ""]
kind_pagament = ["I want to pay by credit card", "I want to pay by cash", ""]

for a, p, g, k in product(address, phone, gift, kind_pagament):
    filled_template = temp.format(a, p, g, k)
    ds["slots"]["address"] = a[14:]
    ds["slots"]["phone"] = p[19:]
    ds["slots"]["gift"] = 'yes' if "gift" in g else 'no' if ("not" in g or 'me' in g) else ''
    ds["slots"]["kind_pagament"] = k[17:]

    with open("delivery.txt", "a") as f:
        f.write(filled_template + "\n")
    
    with open("delivery_json.txt", "a") as f:
        f.write(str(ds) + "\n")