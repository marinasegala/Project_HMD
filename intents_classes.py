from extractor_data import *

possible_flavor = extract_db_init('flavor')
possible_grape = set(extract_db_init('grape') + extract_db_init('Secondary grape'))
possible_color = ['red', 'white', 'rose']
possible_sparkling = ['sparkling', 'still'] # True, False
possible_abv = extract_db_init('abv')
possible_year = extract_db_init('year')
possible_typology = extract_db_init('typology')
possible_country = ['italy', 'france']
possible_region = extract_db_init('region')
possible_closure = ['natural cork', 'screwcap', 'synthetic cork']
possible_fridge = ['yes', 'no'] # True, False
possible_cellar = ['yes', 'no'] # True, False
possible_temperature = extract_db_init('temperature') #int
possible_style = extract_db_init('style')
possible_food = extract_db_init('food')
possible_quantity = [str(x) for x in range(1, 20)] #int
possible_gift = ['yes', 'no'] # True, False
possible_pagament = ['credit card', 'paypal', 'cash', 'revolut']
possible_title = extract_db_init('title_bottle')


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

        self.possibilities = {
            'flavor': possible_flavor,
            'grape': possible_grape,
            'color': possible_color,
            'sparkling': possible_sparkling,
            'abv': possible_abv,
            'year': possible_year,
            'typology': possible_typology
        }

    def __str__(self):
        return f"Flavor: {self.flavor}, Grape: {self.grape}, Color: {self.color}, Sparkling: {self.sparkling}, ABV: {self.abv}, Year: {self.year}, Typology: {self.typology}"
    
    def name(self):
        return 'Wine_details'

class Wine_origin():
    def __init__(self):
        self.country = None
        self.region = None
        self.typology = None
        self.title_bottle = None

        self.possibilities = {
            'country': possible_country,
            'region': possible_region,
            'typology': possible_typology
        }

    def __str__(self):
        return f"Country: {self.country}, Region: {self.region}, Typology: {self.typology}, Title: {self.title_bottle}"

    def name(self):
        return 'Wine_origin'

class Wine_production():
    def __init__(self):
        self.grape = None
        self.abv = None
        self.closure = None
        # self.typology = None

        self.possibilities = {
            'grape': possible_grape,
            'abv': possible_abv,
            'closure': possible_closure
        }

    def __str__(self):
        return f"Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}"

    def name(self):
        return 'Wine_production'

class Wine_conservation():
    def __init__(self):
        self.fridge = None
        self.cellar = None
        self.temperature = None

        self.possibilities = {
            'fridge': possible_fridge,
            'cellar': possible_cellar,
            'temperature': possible_temperature
        }

    def __str__(self):
        return f"Fridge: {self.fridge}, Cellar: {self.cellar}, Temp: {self.temp}"

    def name(self):
        return 'Wine_conservation'

"""
classes for actions that can be grouped into 'paring the correct wine with food'
"""

class Wine_paring(): # from the wine, suggest the best food
    def __init__(self):
        self.style = None
        self.color = None
        self.typology = None

        self.possibilities = {
            'style': possible_style,
            'color': possible_color,
            'typology': possible_typology
        }

    def __str__(self):
        return f"Style: {self.style}, Color: {self.color}, Typology: {self.typology}"

    def name(self):
        return 'Wine_paring'

class Food_paring(): # from the food, suggest the best wine
    def __init__(self):
        self.food = None
        self.style = None
        self.abv = None

        self.possibilities = {
            'food': possible_food,
            'style': possible_style,
            'abv': possible_abv
        }

    def __str__(self):
        return f"Food: {self.food}, Style: {self.style}, ABV: {self.abv}"

    def name(self):
        return 'Food_paring'

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

        self.possibilities = {
            'typology': possible_typology,
            'color': possible_color,
            'quantity': possible_quantity,
            'title_bottle': possible_title
        }

    def __str__(self):
        return f"Typology: {self.typology}, Color: {self.color}, Quantity: {self.quantity}, Budget: {self.budget}, Title: {self.title_bottle}"

    def name(self):
        return 'Wine_order'

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

        self.possibilities = {
            'gift': possible_gift,
            'pagament': possible_pagament
        }

    def __str__(self):
        return f"Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}"