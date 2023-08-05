#arithPython.py
"""
This is a PyPI module for calculating the Prime Factors of a number

Example:

>>> primeFactors(10)
Prime Factors are:
2
5

>>> primeFactors(25)
Prime Factors are:
5
"""


def primeFactors(x):
    """
    primeFactors(n) takes an argument for which the Prime Factors are to be calculated
    :param n: any integer
    """
    print("Prime Factors are:")
    i = 1
    while (i <= x):
        k = 0
        if (x % i == 0):
            j = 1
            while (j <= i):
                if (i % j == 0):
                    k = k + 1
                j = j + 1
            if (k == 2):
                print(i)
        i = i + 1


if __name__ == '__main__':
    import doctest
