"""
@author:    Krzysztof Brzozowski
@file:      playgroun_save_to_arg
@time:      18/04/2022
@desc:      
"""

TEST = None


def saving_to_arg(slocation, some_other_args):
    slocation = 'test'


if __name__ == '__main__':
    print(TEST)
    saving_to_arg(TEST, 'None')
    print(TEST)
