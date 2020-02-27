class StoringSlot():
    def __init__(self, ID):
        self.ID = ID
        self.SlotCoord = [1, 1, 1, 1] # ​Row, Shelf, Level, SlotNu>  
        self.Capacity = [50, 100, 40] # Height, Width, Lenght in CM
        self.WeightMax = "80 kg"
        self.is_occupied = False

# TODO: Add method of yelding next slot coordinates with given boundares
# TODO: Row, Shelf, Level, SlotNum (1, 1, 1, 4) --> (1, 1, 2, 5)

class Property():
    def __init__(self):
        self.ID = 0
        self.Location = "None"
        self.Storage = []
        self.Workers_count = 0

class Warehouse(): # ! WH
    def __init__(self):
        self.ID = 1
        self.Location = "Groove St, 420"
        self.Storage = [StoringSlot(1), StoringSlot(2), StoringSlot(3)]
        self.Workers_count = 1

        def add_new_entry():
            pass
        
        def Send_entry(RP_ID, entry_id, count):
            pass
    
class RetailPoint(): # ! RP
    def __init__(self):
        self.ID = 2
        self.Location = "Korolev, 1337"
        self.Storage = [StoringSlot(1)]
        self.Showcase = [StoringSlot(1), StoringSlot(2), StoringSlot(3)]
        self.Workers_count = 3

        def recieve_entry(self):
            pass
            
        def move2showcase(self):
            pass

        def sell(self):
            pass

class NROS():
    def __init__(self):
