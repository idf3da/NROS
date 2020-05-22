import random
import re
import string


class Utils:
    @staticmethod
    def random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def is_email_valid(email):
        reg_expression = r"[^@]+@[^@]+\.[^@]+"
        return re.match(reg_expression, email)
