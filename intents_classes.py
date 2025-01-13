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

    def __str__(self):
        return f"Flavor: {self.flavor}, Grape: {self.grape}, Color: {self.color}, Sparkling: {self.sparkling}, ABV: {self.abv}, Year: {self.year}, Typology: {self.typology}"
    
    def name(self):
        return 'Wine_details'
    
    def possibilities(self):
        values = {
            'flavor': possible_flavor,
            'grape': possible_grape,
            'color': possible_color,
            'sparkling': possible_sparkling,
            'abv': possible_abv,
            'year': possible_year,
            'typology': possible_typology
        }
        return values

class Wine_origin():
    def __init__(self):
        self.country = None
        self.region = None
        self.typology = None
        self.title_bottle = None

    def __str__(self):
        return f"Country: {self.country}, Region: {self.region}, Typology: {self.typology}, Title: {self.title_bottle}"

    def name(self):
        return 'Wine_origin'
    
    def possibilities(self):
        values = {
            'country': possible_country,
            'region': possible_region,
            'typology': possible_typology,
            'title_bottle': possible_title
        }
        return values
    
    def required(self):
        # false -> the two fields are not required TOGETHER
        if self.country or self.region:
            return [False, 'typology', 'title_bottle']
        if self.typology or self.title_bottle:
            return [False, 'country', 'region']

class Wine_production():
    def __init__(self):
        self.grape = None
        self.abv = None
        self.closure = None
        # self.typology = None

    def __str__(self):
        return f"Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}"

    def name(self):
        return 'Wine_production'
    
    def possibilities(self):
        values = {
            'grape': possible_grape,
            'abv': possible_abv,
            'closure': possible_closure
        }
        return values

class Wine_conservation():
    def __init__(self):
        self.fridge = None
        self.cellar = None
        self.temperature = None

    def __str__(self):
        return f"Fridge: {self.fridge}, Cellar: {self.cellar}, Temp: {self.temp}"

    def name(self):
        return 'Wine_conservation'
    
    def possibilities(self):
        values = {
            'fridge': possible_fridge,
            'cellar': possible_cellar,
            'temperature': possible_temperature
        }
        return values

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

    def name(self):
        return 'Wine_paring'
    
    def possibilities(self):
        values = {
            'style': possible_style,
            'color': possible_color,
            'typology': possible_typology
        }
        return values

class Food_paring(): # from the food, suggest the best wine
    def __init__(self):
        self.food = None
        self.style = None
        self.abv = None

    def __str__(self):
        return f"Food: {self.food}, Style: {self.style}, ABV: {self.abv}"

    def name(self):
        return 'Food_paring'
    
    def possibilities(self):
        values = {
            'food': possible_food,
            'style': possible_style,
            'abv': possible_abv
        }
        return values

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

    def name(self):
        return 'Wine_order'
    
    def possibilities(self):
        values = {
            'typology': possible_typology,
            'color': possible_color,
            'quantity': possible_quantity,
            'title_bottle': possible_title
        }
        return values

"""
classes used ONLY by the systems 
"""
class ListWines():
    pass

class Delivery():
    def __init__(self):
        self.address = None
        self.phone = None
        self.gift = None
        self.kind_pagament = None

    def __str__(self):
        return f"Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.kind_pagament}"
    
    def name(self):
        return 'Delivery'
    
    def possibilities(self):
        values = {
            'gift': possible_gift,
            'kind_pagament': possible_pagament
        }
        return values