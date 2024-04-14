"""
Util functions for Calculator
"""
from decimal import Decimal, ROUND_HALF_UP


class Calculator:
    """Calculator"""

    @staticmethod
    def round_to_nearest(price: Decimal, base: Decimal = Decimal('0.01')) -> Decimal:
        """
        round to the nearest
        :param price:
        :param base:
        :return:
        """
        return (price / base).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * base
