import time
import string, random


def small_large_string(arg: str) -> str:
    return ''.join(letter.lower() if idx % 2 == 0 else letter.upper() for idx, letter in enumerate(arg))


def small_large_string_2(arg: str) -> str:
    tmp = ''
    for idx, letter in enumerate(arg):
        if idx % 2 == 0:
            tmp += letter.lower()
        else:
            tmp += letter.upper()

    return tmp


if __name__ == '__main__':
    length = 10000000
    s = ''.join([random.choice(string.ascii_letters) for _ in range(length)])
    now = time.time()
    x = small_large_string_2(s)
    print(f'append method for string len = {length}: one in:{time.time() - now}s')
