import random
import string


def generate_string(length: int=10):
    letter = f'{string.ascii_letters}{string.digits}'
    otp = "".join(random.choice(letter) for _ in range(length))
    return otp