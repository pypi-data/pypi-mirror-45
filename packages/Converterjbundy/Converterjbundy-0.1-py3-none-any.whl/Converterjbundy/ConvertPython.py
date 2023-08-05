def toCelsius(x):
    '''
    Converts x from Fahrenheit to Celsius
    :param x:
    :return: (x - 32) *5 / 9

    >>> toCelsius(32)
    0
    '''
    return (x - 32) *5 / 9


def toFahrenheit(x):
    '''
    Converts x from Celsius to Fahrenheit
    :param x:
    :return: (x * 9 / 5) + 32

    >>> toFahrenheit(0)
    32
    '''
    return (x * 9 / 5) + 32


def toKilometers(x):
    '''
    Converts x from Miles to Kilometers
    :param x:
    :return: x * 1.609

    >>> toKilometers(1)
    1.60934
    '''
    return x * 1.609


def toMiles(x):
    '''
    Converts x from Kilometers to Miles
    :param x:
    :return: x / 1.609
     >>> toMiles(1)
    0.621371
    '''

    return x / 1.609


def toPounds(x):
    '''
    Converts x from Kilograms to Pounds
    :param x:
    :return: x * 2.205
    >>> toPounds(1)
    2.20462
    '''
    return x * 2.205


def toKilograms(x):
    '''
    Converts x from Pounds to Kilograms
    :param x:
    :return: x / 2.205
    >>> toKilograms(1)
    0.453592
    '''
    return x / 2.205

