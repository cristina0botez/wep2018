from collections import namedtuple, defaultdict
from functools import total_ordering


@total_ordering
class OrderlyPerson:

    def __lt__(self, other):
        result = (self.last < other.last or
                  self.last == other.last and self.first < other.first)
        return result


class Person(OrderlyPerson, namedtuple('PersonBase', ('first', 'last'))):

    def __str__(self):
        return "{0.last}, {0.first}".format(self)


class Table:

    def __init__(self, capacity):
        self._capacity = capacity
        self._guests = set()

    def __contains__(self, guest):
        return guest in self._guests

    def __iter__(self):
        return iter(self._guests)

    def __str__(self):
        sorted_guests = sorted(self._guests)
        return '{{{}}}'.format('; '.join([str(g) for g in sorted_guests]))

    @property
    def capacity(self):
        return self._capacity

    @property
    def occupied_seats(self):
        return len(self._guests)

    @property
    def empty_seats(self):
        return self._capacity - len(self._guests)

    def add(self, guest):
        if len(self._guests) < self._capacity:
            self._guests.add(guest)
        else:
            raise TableFull(
                'Guest {} cannot be seated at this table. The table is full.'
                .format(guest)
            )

    def remove(self, guest):
        if guest in self._guests:
            self._guests.remove(guest)


class TableFull(Exception):
    pass


class GuestList:

    def __init__(self, number_of_tables, table_size):
        self._tables = defaultdict(lambda: Table(table_size))
        self._unassigned = set()
        self._number_of_tables = number_of_tables

    def __len__(self):
        result = (
            sum([table.occupied_seats for table in self._tables.values()]) +
            len(self._unassigned)
        )
        return result

    def __str__(self):
        result = ''
        for table_number, table in self._tables.items():
            result += '{}\n'.format(table_number)
            for guest in sorted(table):
                result += '\t{}\n'.format(guest)
        return result

    def assign(self, guest, table_number):
        self._validate_table_number(table_number)
        try:
            current_table = self.find_table_for(guest)
        except NotRegistered:
            pass
        else:
            if current_table == table_number:
                return
            elif current_table is None:
                self._unassigned.remove(guest)
            else:
                self._tables[current_table].remove(guest)
        if table_number is None:
            self._unassigned.add(guest)
        else:
            self._tables[table_number].add(guest)

    def table(self, number):
        table_number = self._validate_table_number(number)
        return list(self._table[table_number])

    def unassigned(self):
        return list(self._unassigned)

    def find_table_for(self, guest):
        if guest in self._unassigned:
            return None
        for table_number, table in self._tables.items():
            if guest in table:
                return table_number
        raise NotRegistered(guest)

    def free_space(self):
        result = {table_number: table.capacity - table.occupied_seats
                  for table_number, table in self._tables}
        return result

    def guests(self):
        result = [guest for _, table in sorted(self._tables.items())
                  for guest in table]
        return result

    def _validate_table_number(self, number):
        out_of_range = number < 0 or self._number_of_tables > number
        if number is not None and out_of_range:
            raise ValueError(
                'Table number {} out of range. Must be between 1 and {}'
                .format(number, self._number_of_tables)
            )


class NotRegistered(Exception):
    pass
