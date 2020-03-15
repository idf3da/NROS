class Property():
    def __init__(self):
        self.ID = 0
        self.Name = "NoneName"
        self.Location = "None"
        self.StorageCapacity = "0 kg"


class ProductType:  # singletone object
    def __init__(self, ID, Count, Name, Tags, Price, Volume):
        self.ID = ID
        self.Count = Count
        self.Name = Name
        self.Tags = Tags
        self.Price = Price
        self.Volume = Volume


class ProductItem:  # Молоко: 2 шт.
    def __init__(self, id, count):
        self.id = id
        self.count = count
        # ...


class ProductGroup:  # [Молоко: 2шт, Кефир: 3шт]
    def __init__(self, products):  # products - list ProductItem
        self.products = products


class Warehouse(Property):  # ! WH
    def __init__(self, ID, Location, StorageCapacity):
        self.ID = ID
        self.Name = "NoneName"
        self.Location = Location
        self.StorageCapacity = StorageCapacity

    def recieve_product(self):
        pass

    def send_product(self):
        pass

class RetailPoint(Property):  # ! RP
    def __init__(self, ID, Location, StorageCapacity):
        self.ID = ID
        self.Name = "NoneName"
        self.Location = Location
        self.StorageCapacity = StorageCapacity

    def recieve_product(self):
        pass

    def send_product(self):
        pass


class NROS():
    def __init__(self):
        pass
