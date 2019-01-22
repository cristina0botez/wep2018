from functools import total_ordering


class Cart:

    FORMAT_STYLE_SHORT = 'short'
    FORMAT_STYLE_LONG = 'long'

    def __init__(self):
        self.items = set()

    def add(self, item):
        self.items.add(item)

    def __format__(self, format_style):
        if format_style == self.FORMAT_STYLE_SHORT:
            result = ', '.join([item.name for item in sorted(self.items)])
        elif format_style == self.FORMAT_STYLE_LONG:
            result = '\n'.join([str(item) for item in sorted(self.items)])
        else:
            raise ValueError('Invalid format specifier')
        return result


@total_ordering
class Item:

    def __init__(self, quantity, measure, name, price_per_measure):
        self.quantity = quantity
        self.measure = measure
        self.name = name
        self.price_per_measure = price_per_measure

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        result = ('{item.quantity:5} {item.measure:5} {item.name:10} @ '
                  '${item.price_per_measure:.<6.1f}${item.total_price:<2.1f}'
                  .format(item=self))
        return result

    @property
    def total_price(self):
        return self.quantity * self.price_per_measure
