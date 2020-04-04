import datetime
import random
from myapp.models import ProductItem


class FakedData:
    def __init__(self, product_items, location, date):
        self.product_items = product_items
        self.location = location
        self.date = date


class Faker:
    def do(self, locations_count, products_count, data_package_count, days_count):
        locations = [i for i in range(locations_count)]
        products = [i for i in range(products_count)]
        probabilities = [
            [(random.random() + 0.8 if random.random() > 0.9 else random.random()) for j in range(products_count)]
            for i in range(locations_count)]
        result = []
        for index, location in enumerate(locations):
            for day in range(days_count):
                result.append(self.generate_data(products, probabilities[index], data_package_count, location, day))
        return result

    def generate_data(self, products, probabilities, count, location, date):
        items = []
        rand_sum = 0.0
        for i in range(len(products)):
            items.append([probabilities[i] + rand_sum, products[i]])
            rand_sum += probabilities[i]
        items.sort()
        product_count = [0 for i in range(len(items))]
        for i in range(count):
            p = random.random() * rand_sum
            l, r = -1, len(items)  # binary search
            while r - l > 1:
                m = (l + r) // 2
                if items[m][0] < p:
                    l = m
                else:
                    r = m
            product_count[r] += 1
        data = []
        for index, count in enumerate(product_count):
            # print(index, ':', count, end=' ')
            if count:
                data.append(ProductItem(items[index][1], count))
        return FakedData(data, location, date)


random.seed(datetime.datetime.now().microsecond)
faker = Faker()
result = faker.do(10, 20, 100, 3)
for data in result:
    print('location: ', data.location)
    print('date: ', data.date)
    for item in data.product_items:
        print(item.id, ':', item.count, end=' | ')
    print()
