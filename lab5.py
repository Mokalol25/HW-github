class Flower:
    def __init__(self, height=0, size=0, color="Unknown", price=0.0, quantity=0, deliveryRate=0.0):
        self.set_height(height)
        self.set_size(size)
        self.color = color
        self.set_price(price)
        self.set_quantity(quantity)
        self.set_deliveryRate(deliveryRate)

    def __del__(self):
        pass
        print("Hello world!")

    def get_height(self):
        return self.height

    def get_size(self):
        return self.size

    def get_color(self):
        return self.color

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_deliveryRate(self):
        return self.deliveryRate

    def set_height(self, height):
        if height <= 0:
            print("Height must be positive! Setting default height = 1")
            height = 1
        self.height = height
    
    def set_size(self, size):
        if size <= 0:
            print("Size must be positive! Setting default size = 1")
            size = 1
        self.size = size
      
    def set_price(self, price):
        if price <= 0:
            print("Price must be positive! Setting default price = 25")
            price = 25
        self.price = price

    def set_quantity(self, q):
        if q <= 0:
            print("Quantity must be positive! Setting default quantity = 1")
            q = 1
        self.quantity = q
        
    def set_deliveryRate(self, dR):
        if dR <= 0:
            print("Delivery Rate must be positive! Setting default Delivery Rate = 1")
            dR = 1
        self.deliveryRate = dR

    def display(self):
        print(f"Flower: color={self.color}, height={self.height}, size={self.size}, "
              f"price={self.price}, quantity={self.quantity}, delivery={self.deliveryRate}")


class FlowerShop:
    def __init__(self):
        self.flowers = []

    def add_flower(self, flower):
        self.flowers.append(flower)

    def remove_flower(self, color):
        self.flowers = [f for f in self.flowers if f.color != color]

    def display_all(self):
        print("\nFlower Shop Assortment")
        for flower in self.flowers:
            flower.display()

    def top_expensive(self, k): 
        def get_price(flower): 
            return flower.price 
        sorted_flowers = sorted(self.flowers, key=get_price, reverse=True) 
        return sorted_flowers[:k]
    
    def least_deliveryRate_total(self):
        selected = [f for f in self.flowers if f.deliveryRate < 5]
        total = sum(f.price * f.quantity for f in selected)
        return selected, total

class Bouquet:
    def __init__(self):
        self.items = []

    def add_flower(self, flower, q):
        q = max(round(q), 0)
        if q > 0:
            self.items.append((flower, q))

    def total_price(self):
        return sum(flower.price * q for flower, q in self.items)

    def display(self):
        print("\nBouquet")
        for flower, q in self.items:
            print(f"{flower.color} × {q} (price {flower.price})")
        print(f"Total price: {self.total_price()}")


def main():
    rose = Flower(height=50, size=6, color="Red", price=50, quantity=20, deliveryRate=5)
    tulip = Flower(height=30, size=4, color="Yellow", price=25, quantity=15, deliveryRate=3)
    orchid = Flower(height=40, size=5, color="White", price=120, quantity=10, deliveryRate=10)
    sunflower = Flower(height=60, size=10, color="Orange", price=70, quantity=10, deliveryRate=4)

    shop = FlowerShop()
    shop.add_flower(rose)
    shop.add_flower(tulip)
    shop.add_flower(orchid)
    shop.add_flower(sunflower)

    shop.display_all()

    print("\nTop 2 expensive flowers:")
    for f in shop.top_expensive(2):
        f.display()

    print("\nRemoving Yellow flower")
    shop.remove_flower("Yellow")
    shop.display_all()

    bouquet = Bouquet()
    bouquet.add_flower(rose, 4.4)    
    bouquet.add_flower(orchid, 1.2)
    bouquet.display()
    
    selected, total = shop.least_deliveryRate_total()
    print("\nFlowers with deliveryRate < 5:")
    for f in selected:
        f.display()
    print(f"Total price for these flowers: {total}")
    


main()