def add(x, y):
    """
    Adds values from two inputs and return the sum
    :param x:
    :param y:
    :return: (x + y)

    >>> add(19, 3)
    22
    """
    return x + y


def sub(x, y):
    """
    Decreases first value from second input and return the difference
    :param x:
    :param y:
    :return: (x - y)

    >>> sub(19, 3)
    16
    """
    return x - y


def percent(x):
    """
    Makes input into a percent value
    :param x:
    :return: (x/100)

    >>> percent(350)
    3.5
    """
    return x / 100


def square(x):
    """
    Multiplies the input by its own value
    :param x:
    :return: (x*x)

    >>> square(8)
    64
    """
    return x * x


def multiply(x, y):
    """
    Multiplies the input by the second input
    :param x:
    :param y:
    :return: (x*y)

    >>> multiply(8, 7)
    56
    """
    return x * y


def divide(x, y):
    """
    Divides the input by the second input
    :param x:
    :param y:
    :return: (x/y)

    >>> divide(21, 7)
    3.0
    """
    return x / y


def power(x, y):
    """
    Takes the initial input and puts it to the power of the second value
    >>> power(2, 4)
    32
    """
    i = 0
    original_x = x
    while i < y:
        x = x*original_x
        i = i + 1
    return x