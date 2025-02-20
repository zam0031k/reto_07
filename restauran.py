from collections import namedtuple
import json
from queue import Queue

class MenuItem:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
    
    # Getters
    def get_name(self):
        return self._name
    
    def get_price(self):
        return self._price
    
    # Setters
    def set_name(self, new_name):
        self._name = new_name
        
    def set_price(self, new_price):
        self._price = new_price
    
    def calculate_total(self, quantity: int=1):
        """Calculate the total price for a given quantity of the item."""
        return self.get_price()*quantity
    
class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size_ml: int, container: str):
        super().__init__(name, price)
        self._size_ml = size_ml 
        self._container = container  
        
    # Getters
    def get_size_ml(self):
        return self._size_ml
    
    def get_container(self):
        return self._container
    
    # Setters
    def set_size_ml(self, new_size_ml):
        self._size_ml = new_size_ml
        
    def set_container(self, new_container):
        self._container = new_container
        
    def __str__(self):
        return f"{self.get_name()} ({self.get_size_ml()}ml, {self.get_container()}): ${self.get_price():.3f} COP"
        
class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, portion_size: str, sauses:bool):
        super().__init__(name, price)
        self._portion_size = portion_size
        self._sauses = sauses
        
    # Getters
    def get_portion_size(self):
        return self._portion_size
    
    def get_sauses(self):
        return self._sauses
    
    # Setters
    def set_portion_size(self, new_portion_size):
        self._portion_size = new_portion_size
        
    def set_sauses(self, new_sauses):
        self._sauses = new_sauses
    
    def __str__(self):
        return f"{self.get_name()} ({self.get_portion_size()}): ${self.get_price():.3f} COP"
        
class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, porcion_sinze: str, spiciness:bool, sauses:bool):
        super().__init__(name, price)
        self._sinze_portion = porcion_sinze
        self._spiciness = spiciness
        self._sauses = sauses
    
    # Getters
    def get_sinze_portion(self):
        return self._sinze_portion
    
    def get_spiciness(self):
        return self._spiciness
    
    def get_sauses(self):   
        return self._sauses
    
    # Setters
    def set_sinze_portion(self, new_sinze_portion):
        self._sinze_portion = new_sinze_portion
        
    def set_spicinesss(self, new_spiciness):
        self._spiciness = new_spiciness
    
    def set_sauses(self, new_sauses):
        self._sauses = new_sauses
    
    def __str__(self):
        return f"{self.get_name()} ({self.get_sinze_portion()}): ${self.get_price():.3f} COP"
   
class Order:
    MENU_FILE = "menu.json"
    def __init__(self):
        self._items = []
        self.total = 0
        self.menu = self.load_menu()

    def add_item(self, item: MenuItem, quantity: int=1):
        """Add an item to the order."""
        if item.get_name() in self.menu:
            self._items.append((item, quantity))
        else:
            print(f"ERROR: Order is not in the menu.")
    
    def remove_item(self, item: MenuItem, quantity_remove: int=1):
        """Remove an item specific to order"""
        for i, (name, quantity) in enumerate(self._items):
            if name == item.get_name():
                new_quantity = quantity - quantity_remove
            if new_quantity > 0:
                self._items[i] = (name, new_quantity)        
            elif new_quantity == 0:
                self._items.pop(i)
            break
        
    def total_invoice(self):
        """Calculate the total amount for the order."""
        self.total += sum(item.calculate_total(quantity) for item, quantity in self._items)        
        return self.total

    def discount_drink(self):
        """
        A discount applies to drinks depending on whether there is a main .
        """ 
        self.discount_beverage = 0
        self.reduction_drink = 0
        self.prices_beverages = 0
        count = 0
        for menu_item, _ in self._items:
            if isinstance(menu_item, MainCourse):
                for menu_item, _ in self._items[count:]:
                    count += 1
                    if isinstance(menu_item, Beverage):
                        self.prices_beverages += menu_item.get_price()
                        self.discount_beverage += 0.20
                        self.reduction_drink = self.prices_beverages * self.discount_beverage
                        break
            else: 
                self.discount_beverage += 0
                self.reduction_drink += 0

    def __str__(self):
        self.total_pay = self.total - self.reduction_drink
        return  (f"The total of the invoice is: ${self.total:.3f} COP\n\n"
                 f"DISCOUNT OF BERVERAGE BY MAIN COURSES: \n"
                 f"-The total price of berverages is: ${self.prices_beverages:.3f} COP \n"
                 f"-The total price of berverages with discount of {self.discount_beverage * 100}% is: ${self.prices_beverages - self.reduction_drink:.3f} COP \n\n"
                 f" The total price to pay is: ${self.total_pay:.3f} COP")
    
    def create_menu(self):
        """Create a base menu and save it to JSON."""
        menu = {
            "Coca Cola": {"price": 3.20, "type": "Beverage"},
            "Lemon Juice": {"price": 2.00, "type": "Beverage"},
            "Nachos": {"price": 5.00, "type": "Appetizer"},
            "French Fries": {"price": 4.30, "type": "Appetizer"},
            "Hamburger": {"price": 14.00, "type": "MainCourse"},
            "Pizza": {"price": 10.00, "type": "MainCourse"},
            "Sushi": {"price": 13.50, "type": "MainCourse"},
            "Tacos": {"price": 11.30, "type": "MainCourse"},
        }
        with open(self.MENU_FILE, "w") as file:
            json.dump(menu, file, indent=4)
         
    def load_menu(self):
        """Load the menu from JSON."""
        try:
            with open(self.MENU_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Menu not found. Creating...")
            self.create_menu()
            return self.load_menu()
           
    def add_menu_item(self, name, price: float, type): 
        """Adds a new item to the menu and saves it to JSON."""
        self.menu[name] = {"price": price, "type": type}
        self.save_menu()
        print(f"{name} added to menu.")     

    def update_menu(self, name, price=None, type=None):
        if name in self.menu:
            if price:       
                self.menu[name]["price"] = price
            if type:
                self.menu[name]["type"] = type
            self.save_menu()
            print(f"{name} updated in menu.")
        else: 
            print(f"{name} not found in menu.")

    def delete_menu_item(self, name):
        """Removes an item from the menu and saves it to JSON."""
        if name in self.menu:
            del self.menu[name]
            self.save_menu()
            print(f"{name} removed from menu.")
        else:
            print(f"{name} not in menu.")

    def save_menu(self):
        """Save the updated menu to JSON."""
        with open(self.MENU_FILE, "w") as file:
            json.dump(self.menu, file, indent=4)
        print("Menu updated.")

class MedioPago:
  def __init__(self):
    pass

  def pagar(self, order: Order):
    raise NotImplementedError("Subclasses must implement pagar()")

class Tarjeta(MedioPago):
  def __init__(self, numero, cvv):
    super().__init__()
    self.numero = numero
    self.cvv = cvv

  def pagar(self, order: Order):
    print("card payment: ")
    print(f"Paying ${order.total_pay:.3f} COP with card {self.numero[-4:]}")

class Efectivo(MedioPago):
  def __init__(self, monto_entregado):
    super().__init__()
    self.monto_entregado = monto_entregado

  def pagar(self, order: Order):
    print("Payment in cash:")
    if self.monto_entregado >= order.total_pay:
      print(f"Payment made in cash. Change: ${(self.monto_entregado - order.total_pay):.3f} COP")
    else:
      print(f"Insufficient funds. ${(order.total_pay - self.monto_entregado):.3f} COP missing to complete payment")

# Create menu items
Menu = namedtuple("Menu", ["beverage", "appetizer", "mainCourse"])

beverage = [
    Beverage("Coca Cola", 3.200, 500, "Bottle"),
    Beverage("Lemon Juice", 2.000, 300, "Glass")
]

appetizer = [
    Appetizer("Nachos", 5.000, "Medium", True),
    Appetizer("French Fries", 4.300, "Small", False),
    Appetizer("Fruit Salad", 6.000, "Medium", False)
]

mainCourse = [
    MainCourse("Hambuerger", 14.000, "Medium", False, True),
    MainCourse("Pizza", 10.000, "Family", False, True),
    MainCourse("Sushi", 13.500, "Large", True, True),
    MainCourse("Tacos", 11.300, "Medium", True, True)
]

menu_items = Menu(beverage, appetizer, mainCourse)
for itemas in menu_items:
    print(itemas)

# Create an order
order1 = Order()
order1.add_item(menu_items.beverage[0], 2)
order1.add_item(menu_items.beverage[1])
order1.add_item(menu_items.appetizer[0])
order1.total_invoice()
order1.discount_drink()

# menu management
order1.add_menu_item("Hot Dog", 6.50, "MainCourse")
order1.update_menu("Pizza", price=12.00)
order1.delete_menu_item("Tacos")

print(f"\nORDER 1: \n{order1}\n")

# Create another order
order2 = Order()
order2.add_item(menu_items.beverage[1], 3)
order2.add_item(menu_items.appetizer[0], 2)
order2.add_item(menu_items.appetizer[1])
order2.add_item(menu_items.mainCourse[3])
order2.total_invoice()
order2.discount_drink()

# menu management
order2.add_menu_item("Salchipapas", 7.00, "Appetizer")
order2.update_menu("Lemon Juice", price=2.50)
order2.delete_menu_item("French Fries")

print(f"ORDER 2: \n{order2}\n")

# Create another order
order3 = Order()
order3.add_item(menu_items.beverage[1])
order3.add_item(menu_items.beverage[0], 3)
order3.add_item(menu_items.mainCourse[2], 2)
order3.add_item(menu_items.mainCourse[3], 3)
order3.add_item(menu_items.appetizer[2])
order3.total_invoice()
order3.discount_drink()

# menu management
order3.add_menu_item("Mojito", 8.00, "Beverage")
order3.update_menu("Pizza", price=13.00)
order3.delete_menu_item("Nachos")

print(f"ORDER 3: \n{order3}\n")

ordenes = Queue()
ordenes.put(order1)
ordenes.put(order2) 
ordenes.put(order3) 

transacciones = Queue()
transacciones.put(Tarjeta("1234567890123456", 123))
transacciones.put(Efectivo(60.000))
transacciones.put(Efectivo(12.420))

while not ordenes.empty():
    orden = ordenes.get()
    metodo_pago = transacciones.get()
    metodo_pago.pagar(orden)