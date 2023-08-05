# coding=utf-8
import string
import random

name = 'NIFVerifier'
LEN_NIF = 9
VALID_INITIAL_VALUES = "1235689"


def am_i_a_dead_ass_valid_nif(nif):
    """
    Check if I'm a valid NIF.
    A valid NIF is calculated using the last digit. This digit is called the control digit.
    Feel free to read more about it here:
    https://pt.wikipedia.org/wiki/N%C3%BAmero_de_identifica%C3%A7%C3%A3o_fiscal
    The validation part was done thanks to this awesome guy:
    https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf#file-validators_pt-py-L58
    :param nif:
    :return:
    """

    if not isinstance(nif, str):
        raise TypeError('You motherfucker should pass a string of numbers and not an integer')

    # verify the length of the number passed
    if len(nif) != LEN_NIF:
        return False

    # verify initial value of the NIF passed
    if nif[0] not in VALID_INITIAL_VALUES:
        return False

    return validate_nif(nif)


def validate_nif(num):
    """
    Check the validity of NIF
    Receives a string with numbers to validate
    """

    # converts a string to a list of integers
    num = to_int_list(num)

    # computes the sum of all numbers to check the control digit
    sum = 0
    for pos, dig in enumerate(num[:-1]):
        sum += dig * (9 - pos)

    # verify the control digit
    return (sum % 11 and (11 - sum % 11) % 10) == num[-1]


def to_int_list(numstr):
    """
    Converts the string passed to a list of integers eliminating any invalid character.
    """
    res = []

    # converts all digits
    for i in numstr:
        if i in string.digits:
            res.append(int(i))

    return res


def generate_dead_ass_valid_nif(initial_value):
    """
    Generates a valid nif based on the initial value.
    Initial value must be a string passed
    :param initial_value:
    :return:
    """
    if not isinstance(initial_value, str):
        raise TypeError('Your dead ass just passed value different than a string. Please, my kind sir pass a string')

    if initial_value not in VALID_INITIAL_VALUES:
        raise TypeError('Your ass provided an invalid initial value for a NIF. Please provind one in {0}'
                        .format(VALID_INITIAL_VALUES))

    # Generate a number with 8 digits
    # The 9th digit will be the control digit
    rand_nif = initial_value + str(random.randint(1000000, 9999999))

    sum_ = 0
    for pos, digit in enumerate(rand_nif):
        sum_ += (int(digit) * (9 - pos))

    r_division = sum_ % 11

    if r_division == 1 or r_division == 0:
        return str(rand_nif) + '0'

    return str(rand_nif) + str(11 - r_division)
