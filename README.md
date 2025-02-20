# Sistema de gestión de pedidos en Restaurant
Se han realizado varias mejoras en la estructura de datos y la organización del código, incluyendo la adición de una cola FIFO para gestionar múltiples órdenes, el uso de named tuples en el menú y la implementación de una interfaz para la gestión de menús.

## Cambios y Mejoras

- Optimización de estructura y funcionalidades.

- Uso de una estructura FIFO Queue para gestionar múltiples órdenes de manera eficiente.

- Definición de un namedtuple en el menú para definir un conjunto de elementos organizados.

- Crear un nuevo menú.

- Agregar, actualizar y eliminar elementos del menú.

- Almacenar los menús en archivos JSON utilizando diccionarios.

## Estructura del Código
#### Clases Principales
1. `MenuItem`: Clase base para representar elementos del menú con nombre y precio.

2. `Beverage`, `Appetizer`, `MainCourse`: Clases que heredan de MenuItem y añaden atributos específicos.

3. `Order`: Maneja los pedidos y permite agregar, eliminar y calcular el total de una orden.

4. `MedioPago`: Interfaz para implementar diferentes métodos de pago.

5. `Tarjeta`: Permite pagar con tarjeta.

6. `Efectivo`: Permite pagar en efectivo con cálculo de cambio.

7. `Queue`: Utilizado para gestionar múltiples órdenes de forma FIFO.

## Uso de `namedtuple` para Menú
```python
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
```
- `namedtuple`: Se utiliza para definir una estructura de datos simple y eficiente para el menú, agrupando diferentes tipos de elementos del menú (bebidas, aperitivos y platos principales) en una sola estructura.

## Gestión de Órdenes y Transacciones con `Queue`
```python
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
```
- `Queue`: Se utiliza para gestionar las órdenes y transacciones de manera eficiente. Las órdenes y transacciones se añaden a las colas y se procesan en el orden en que se reciben.

## Almacenamiento del Menú
El menú se almacena y gestiona mediante archivos JSON. 


```python
{
    "Coca Cola": {
        "price": 3.2,
        "type": "Beverage"
    },
    "Lemon Juice": {
        "price": 2.5,
        "type": "Beverage"
    },
    "Hamburger": {
        "price": 14.0,
        "type": "MainCourse"
    },
    "Pizza": {
        "price": 13.0,
        "type": "MainCourse"
    },
    "Sushi": {
        "price": 13.5,
        "type": "MainCourse"
    },
    "Hot Dog": {
        "price": 6.5,
        "type": "MainCourse"
    },
    "Salchipapas": {
        "price": 7.0,
        "type": "Appetizer"
    },
    "Mojito": {
        "price": 8.0,
        "type": "Beverage"
    }
}
```
## Uso del Sistema

1. **Gestión del Menú**

- Crear el menú base.

- Agregar, actualizar y eliminar elementos.

2. **Gestión de Órdenes**

- Agregar y eliminar productos a la orden.

- Calcular el total de la orden y aplicar descuentos.

3. **Gestión de Pagos**

- Procesar pagos con tarjeta o efectivo.

