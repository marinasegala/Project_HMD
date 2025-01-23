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
general class
"""
class ClassBase:
    def __init__(self):
        pass

    def name(self):
        return self.__class__.__name__.lower()

"""
classes for actions that can be grouped into 'asking for information' 
"""
class Wine_details(ClassBase):
    def __init__(self):
        self.flavor = None
        self.grape = None
        self.color = None
        self.sparkling = None
        self.abv = None
        self.year = None
        self.typology = None
    
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
    
    def required(self):
        return [['flavor', 'grape', 'color', 'sparkling', 'abv', 'year'], ['typology']]

class Wine_origin(ClassBase):
    def __init__(self):
        self.country = None
        self.region = None
        self.color = None
        self.typology = None
        self.title_bottle = None

    def possibilities(self):
        values = {
            'country': possible_country,
            'region': possible_region,
            'color': possible_color,
            'typology': possible_typology,
            'title_bottle': possible_title
        }
        return values
    
    def required(self):
        return [['country', 'region', 'color'], ['typology', 'title_bottle']]
        #if all are None
        #if all(getattr(self, field) is None for field in poss1):
        
        #if at least one is not None for values of self
        #count = sum(getattr(self, key) is not None for key in slots)

class Wine_production(ClassBase):
    def __init__(self):
        self.grape = None
        self.abv = None
        self.closure = None
        self.typology = None
    
    def possibilities(self):
        values = {
            'grape': possible_grape,
            'abv': possible_abv,
            'closure': possible_closure,
            'typology': possible_typology
        }
        return values
    
    def required(self):
        return [['grape', 'abv', 'closure'], ['typology']]

class Wine_conservation(ClassBase):
    def __init__(self):
        self.fridge = None
        self.cellar = None
        self.temperature = None
        self.typology = None

    def possibilities(self):
        values = {
            'fridge': possible_fridge,
            'cellar': possible_cellar,
            'temperature': possible_temperature, 
            'typology': possible_typology
        }
        return values
    
    def required(self):
        return [['fridge', 'cellar', 'temperature'], ['typology']]

"""
classes for actions that can be grouped into 'paring the correct wine with food'
"""

class Wine_paring(ClassBase): # from the wine, suggest the best food
    def __init__(self):
        self.style = None
        self.color = None
        self.typology = None
    
    def possibilities(self):
        values = {
            'style': possible_style,
            'color': possible_color,
            'typology': possible_typology
        }
        return values
    
    def required(self):
        return [['style', 'color'], ['typology']]

class Food_paring(ClassBase): # from the food, suggest the best wine
    def __init__(self):
        self.food = None
        self.style = None
        self.abv = None
    
    def possibilities(self):
        values = {
            'food': possible_food,
            'style': possible_style,
            'abv': possible_abv
        }
        return values
    
    def required(self):
        return ['food']

"""
classes for actions that can be grouped into 'ordering wine'
"""

class Wine_ordering(ClassBase):
    def __init__(self):
        self.typology = None
        self.quantity = None
        self.total_budget = None
        self.title_bottle = None
    
    def possibilities(self):
        values = {
            'typology': possible_typology,
            'quantity': possible_quantity,
            'title_bottle': possible_title, 
            'total_budget': True
        }
        return values
    
    def required(self):
        return ['total_budget', 'quantity','typology']

"""
classes used ONLY by the systems 
"""

class Wine_Bottle():
    def __init__(self):
        self.title_bottle = None
        self.description = None
        self.typology = None
        self.price = None
        self.grape = None
        self.closure = None
        self.country = None
        self.region = None
        self.flavor = None
        self.color = None
        self.abv = None
        self.style = None
        self.year = None
        self.food = None
        self.sparkling = None
        self.temperature = None
        self.fridge = None
        self.cellar = None
        self.quantity = None
        self.gift = None
        self.kind_pagament = None
        self.phone = None
        self.address = None

    def __str__(self):
        
        # return fields that are not None
        fields = [field for field in self.__dict__ if getattr(self, field) is not None]
        ret = ''
        for field in fields:
            ret += f"\t{field}: {getattr(self, field)}\n"

        if ret == '':
            return "There are no wines that match the information you provided"
        return ret 


class Delivery(ClassBase):
    def __init__(self):
        self.address = None
        self.phone = None
        self.gift = None
        self.kind_pagament = None
    
    def possibilities(self):
        values = {
            'gift': possible_gift,
            'kind_pagament': possible_pagament, 
            'address': True,
            'phone': True
        }
        return values
    
    def required(self):
        return ['address', 'phone', 'gift', 'kind_pagament']
