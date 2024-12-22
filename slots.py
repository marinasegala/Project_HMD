class Ordering():
    def __init__(self):
        self.name = None
        self.qty = None
        self.address = None
        self.phone = None
        self.gift = None
        self.pagament = None
        #self.price = None

        self.possibilities = {
            "name": True,
            "qty": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "address": True,
            "phone": True,
            "gift": [True, False],
            "pagament": ['cash', 'credit card', 'paypal'],
            #"price": True
        }

    def __str__(self):
        return f"Name: {self.name}, Quantity: {self.qty}, Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}, Price: {self.price}"

    def extract(self):
        return {
            "name": self.name,
            "qty": self.qty,
            "address": self.address,
            "phone": self.phone,
            "gift": self.gift,
            "pagament": self.pagament,
            "price": self.price
        }

class ParingFood():
    def __init__(self):
        self.kind = None
        self.food_pairing = None
        self.year = None
        self.name = None
        self.grape = None
        self.color = None
        self.style = None

        self.possibilities = {
            "kind": ['Porsecco', 'Pinot', 'Gavi', 'Valdobbiadene', 'Macon', 'Saumur', 'Champagne', 'Ripasso', 'Brunello di Montalcino', 'Etna', 'Bordeaux Supérieur', 'Haut-Médoc', 'Rully', 'Fleurie', 'Saint-Émilion', 'Cotes Du Rhone', 'Lirac', 'La Clape', 'Lugana','Cotes De Provence', 'Coteaux Varois-En-Provence', "Coteaux D'Aix-En-Provence"],
            "food_pairing": ['aperitif', 'starters', 'first course', 'cold cuts', 'savory pies', 'pheasant meat', 'pumpkin dishes', 'meat', 'fish', 'white meat', 'red meat', 'poultry', 'pork', 'game', 'mashroom', 'cheese', 'dessert'],
            "year": True,
            "name": True,
            "grape": True,
            "color": ['white', 'red', 'rose'],
            "style": True
            
        }

    def __str__(self):
        return f"Kind: {self.kind}, Food Pairing: {self.food_pairing}, Year: {self.year}, Name: {self.name}, Grape: {self.grape}, Color:{self.color}, Style: {self.style}"

    def extract(self):
        return {
            "kind": self.kind,
            "food_pairing": self.food_pairing,
            "year": self.year,
            "name": self.name,
            "grape": self.grape,
            "color": self.color,
            "style": self.style
        }

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

        self.possibilities = {
            'name': True,
            'kind': True,
            'country': ['Italy', 'France'],
            'region': True,
            'color': ['white', 'red', 'rose'],
            'grape': True,
            'abv': True,
            'closure': ['Natural Cork', 'Screwcap', 'Synthetic Cork'],
            'flavor': True,
            'style': True,
            'foodpairing': ['aperitif', 'starters', 'first course', 'cold cuts', 'savory pies', 'pheasant meat', 'pumpkin dishes', 'meat', 'fish', 'white meat', 'red meat', 'poultry', 'pork', 'game', 'mashroom', 'cheese', 'dessert']
        }
        
    def __str__(self):
        return f"Name: {self.name}, Kind: {self.kind}, Country: {self.country}, Region: {self.region}, Color: {self.color}, Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}, Flavor: {self.flavor}, Style: {self.style}, Food Pairing: {self.food_pairing}"
    
    def extract(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "country": self.country,
            "region": self.region,
            "color": self.color,
            "grape": self.grape,
            "abv": self.abv,
            "closure": self.closure,
            "flavor": self.flavor,
            "style": self.style,
            "food_pairing": self.food_pairing
        }
    

def assign_field (intent: object, field: str, value: str):
    # find the correct possible field
    for possible in intent.possibilities:
        if field in possible:
            setattr(intent, field, value)
            break
