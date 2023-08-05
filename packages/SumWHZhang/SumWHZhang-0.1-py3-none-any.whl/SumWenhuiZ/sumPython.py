"""
Help on module sumPython:

NAME
    sumPython

FILE
    /Users/zhangwenhui/PycharmProjects/HelloPython/SumWenhuiZ/sumPython.py

FUNCTIONS
    sum(n)
        Adds values from n inputs and return the sum
        :param n:
        :return: (1+n)*n/2

        >>> sum(10)
        55.0

"""
def sum(n):
    """
    Adds values from n inputs and return the sum
    :param n:
    :return: (1+n)*n/2

    >>> sum(10)
    55.0
    """
    return (1+n)*n/2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
