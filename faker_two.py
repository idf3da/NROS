import random
import datetime

random.seed(datetime.datetime.now().microsecond)
max_demand_product = 20
norm_demand_product = max_demand_product // 2 - 3


class FakerLocation:
    def __init__(self, count):
        self.count = count

        self.data_demand = [0] * self.count
        self.data_location = [0] * self.count
        self.count_demand = 0
        self.change_location()

    def change_location(self):
        self.data_demand = [0] * self.count
        self.count_demand = self.count // random.randint(3, self.count // 3)  # количество привелигорованного тавара
        a = random.randint(0, self.count - self.count_demand)
        b = a + self.count_demand
        self.data_demand[a:b] = [1] * self.count_demand
        self.data_demand[random.randint(0, self.count - 1)] = 1
        self.data_demand[random.randint(0, self.count - 1)] = 1
        self.generate()

    def generate(self):
        for i in range(self.count):
            self.data_location[i] = random.randint(1, norm_demand_product)
            if self.data_demand[i]:
                self.data_location[i] = random.randint(10, max_demand_product)
        return self.data_location

    def get(self):
        return self.data_location

    def print_for_test(self):
        print(self.data_demand)
        print(self.data_location)


class Faker:
    def __init__(self, location_count, days_count, product_count):
        self.location_count = location_count
        self.days_count = days_count
        self.grid = []
        self.location = FakerLocation(product_count)

    def print(self):
        for i in range(self.location_count):
            print('LOCATION: ', i)
            for j in range(self.days_count):
                print('- date: ', j)
                print('  ', self.location.get())
                self.location.generate()
            self.location.change_location()


Faker = Faker(10, 3, 50)
print(Faker.print())
