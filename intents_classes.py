from extractor_data import *

possible_flavor = extract_db_init('flavor')
possible_grape = set(extract_db_init('grape') + extract_db_init('Secondary grape'))
possible_color = ['red', 'white', 'rose']
possible_sparkling = [True, False]
possible_abv = extract_db_init('abv')
possible_year = extract_db_init('year')
possible_typology = extract_db_init('typology')
possible_country = ['italy', 'france']
possible_region = extract_db_init('region')
possible_closure = ['natural cork', 'screwcap', 'synthetic cork']
possible_fridge = [True, False]
possible_cellar = [True, False]
possible_temperature = [int(x) for x in extract_db_init('temp')]
possible_style = extract_db_init('style')
possible_food = extract_db_init('food')
possible_quantity = [x for x in range(1, 20)]
possible_gift = [True, False]
possible_pagament = ['credit card', 'paypal', 'cash', 'revolut']



"""
classes for actions that can be grouped into 'asking for information' 
"""
class Wine_details():
    def __init__(self):
        self.flavor = None
        self.grape = None
        self.color = None
        self.sparkling = None
        self.abv = None
        self.year = None
        self.typology = None

    def __str__(self):
        return f"Flavor: {self.flavor}, Grape: {self.grape}, Color: {self.color}, Sparkling: {self.sparkling}, ABV: {self.abv}, Year: {self.year}, Typology: {self.typology}"
    
class Wine_origin():
    def __init__(self):
        self.country = None
        self.region = None
        self.typology = None
        self.title_bottle = None

    def __str__(self):
        return f"Country: {self.country}, Region: {self.region}, Typology: {self.typology}, Title: {self.title_bottle}"

class Wine_production():
    def __init__(self):
        self.grape = None
        self.abv = None
        self.closure = None
        # self.typology = None

    def __str__(self):
        return f"Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}"

class Wine_conservation():
    def __init__(self):
        self.fridge = None
        self.cellar = None
        self.temp = None

    def __str__(self):
        return f"Fridge: {self.fridge}, Cellar: {self.cellar}, Temp: {self.temp}"

"""
classes for actions that can be grouped into 'paring the correct wine with food'
"""

class Wine_paring(): # from the wine, suggest the best food
    def __init__(self):
        self.style = None
        self.color = None
        self.typology = None

    def __str__(self):
        return f"Style: {self.style}, Color: {self.color}, Typology: {self.typology}"

class Food_paring(): # from the food, suggest the best wine
    def __init__(self):
        self.food = None
        self.style = None
        self.abv = None

    def __str__(self):
        return f"Food: {self.food}, Style: {self.style}, ABV: {self.abv}"

"""
classes for actions that can be grouped into 'ordering wine'
"""

class Wine_order():
    def __init__(self):
        self.typology = None
        self.color = None
        self.quantity = None
        self.budget = None
        self.title_bottle = None

    def __str__(self):
        return f"Typology: {self.typology}, Color: {self.color}, Quantity: {self.quantity}, Budget: {self.budget}, Title: {self.title_bottle}"


"""
classes used ONLY by the systems 
"""
class ListWines():
    pass

class Shipping():
    def __init__(self):
        self.address = None
        self.phone = None
        self.gift = None
        self.pagament = None

    def __str__(self):
        return f"Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}"