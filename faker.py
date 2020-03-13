import datetime
import random

from final_abstract import ProductItem


class FakedData:
    def __init__(self, product_items, location, date):
        self.product_items = product_items
        self.location = location
        self.date = date


class Faker:
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
            print(index, ':', count, end=' ')
            if count:
                data.append(ProductItem(items[index][1], count))
        return FakedData(data, location, date)


random.seed(datetime.datetime.now().microsecond)
faker = Faker()
faker.generate_data([i for i in range(20)], [1 / 2 for i in range(10)] + [2 / 4 for i in range(10)], 40, 'Kremlin',
                    '01.01.2001')
