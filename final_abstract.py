class Property():
    def __init__(self):
        self.ID = 0
        self.Name = "NoneName"
        self.Location = "None"
        self.StorageCapacity = "0 kg"

class Product():
    def __init__(self, ID, Count, Name, Tags, Price, Volume):
        self.ID = ID
        self.Count = Count
        self.Name = Name
        self.Tags = Tags
        self.Price = Price
        self.Volume = Volume

class ProductGroup():
    def __init__(self, ID, Products_IDs):
        self.product_type = product_IDS #[id_хлеб ид_молоко]
        self.counts = [2,1] 
        

class Warehouse(Property): # ! WH
    def __init__(self, ID, Location, StorageCapacity):
        self.ID = ID
        self.Name = "NoneName"
        self.Location = Location
        self.StorageCapacity = StorageCapacity
    
    def recieve_product(self):
        pass

    def send_product(self):
        pass

class RetailPoint(Property): # ! RP
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