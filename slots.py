class Ordering():
    def __init__(self):
        self.name = None
        self.qty = None
        self.address = None
        self.phone = None
        self.gift = None
        self.pagament = None
        self.price = None

        self.possible_name = True # True if the values are all in the csv file 
        self.possible_qty = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.possible_address = [] # don't care
        self.possible_phone = [] # don't care
        self.possible_gift = [True, False] 
        self.possible_pagament = ['cash', 'credit card', 'paypal']
        self.possible_price = True # True if the values are all in the csv file

    def __str__(self):
        return f"Name: {self.name}, Quantity: {self.qty}, Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}, Price: {self.price}"


class ParingFood():
    def __init__(self):
        self.kind = None
        self.food_pairing = None
        self.year = None
        self.name = None
        self.grape = None
        self.style = None

        self.possible_kind = ['Porsecco', 'Pinot', 'Gavi', 'Valdobbiadene', 'Macon', 'Saumur', 'Champagne', 'Ripasso', 'Brunello di Montalcino', 'Etna', 'Bordeaux Supérieur', 'Haut-Médoc', 'Rully', 'Fleurie', 'Saint-Émilion', 'Cotes Du Rhone', 'Lirac', 'La Clape', 'Lugana','Cotes De Provence', 'Coteaux Varois-En-Provence', "Coteaux D'Aix-En-Provence"]
        self.possible_food_pairing = ['aperitif', 'starters', 'first course', 'cold cuts', 'savory pies', 'pheasant meat', 'pumpkin dishes', 'meat', 'fish', 'white meat', 'red meat', 'poultry', 'pork', 'game', 'mashroom', 'cheese', 'dessert']
        self.possible_year = True # True if the values are all in the csv file
        self.possible_name = True # True if the values are all in the csv file
        self.possible_grape = True # True if the values are all in the csv file
        self.possible_style = True # True if the values are all in the csv file

    def __str__(self):
        return f"Kind: {self.kind}, Food Pairing: {self.food_pairing}, Year: {self.year}, Name: {self.name}, Grape: {self.grape}, Style: {self.style}"


class AskInfo():
    def __init__(self):
        self.name = None
        self.kind = None
        self.country = None
        self.region = None
        self.color = None
        self.grape = None
        self.abv = None
        self.closure = None
        self.flavor = None
        self.style = None
        self.food_pairing = None

        self.possible_name = True # True if the values are all in the csv file
        self.possible_kind = True # True if the values are all in the csv file
        self.possible_country = ['Italy', 'France']
        self.possible_region = True # True if the values are all in the csv file
        self.possible_color = ['white', 'red', 'rose']
        self.possible_grape = True # True if the values are all in the csv file
        self.possible_abv = True # True if the values are all in the csv file
        self.possible_closure = ['Natural Cork', 'Screwcap', 'Synthetic Cork'] 
        self.possible_flavor = True # True if the values are all in the csv file
        self.possible_style = True # True if the values are all in the csv file
        self.possible_foodpairing = ['aperitif', 'starters', 'first course', 'cold cuts', 'savory pies', 'pheasant meat', 'pumpkin dishes', 'meat', 'fish', 'white meat', 'red meat', 'poultry', 'pork', 'game', 'mashroom', 'cheese', 'dessert']

    def __str__(self):
        return f"Name: {self.name}, Kind: {self.kind}, Country: {self.country}, Region: {self.region}, Color: {self.color}, Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}, Flavor: {self.flavor}, Style: {self.style}, Food Pairing: {self.food_pairing}"