from collections import defaultdict


visits = defaultdict(dict)


def collect_places():
    while True:
        try:
            user_input = input('Tell me where you went: ')
            state, city = extract_state_and_city(user_input)
            store_visit(state, city, visits)
        except ValueError:
            print("That's not a legal city, state combination")
        except InputFinished:
            break


def extract_state_and_city(user_input):
    if user_input == '':
        raise InputFinished()
    city, state = user_input.split(',')
    city = city.strip()
    state = state.strip()
    if city == '' or state == '':
        raise ValueError('Empty value for city/state')
    return state, city


def store_visit(state, city, visits):
    try:
        visits[state][city] += 1
    except KeyError:
        visits[state][city] = 1


def display_places():
    print('You visited')
    for state in sorted(visits):
        print(state)
        cities = visits[state]
        for city in sorted(cities):
            visit_count = cities[city]
            visit_count_display = ' ({})'.format(
                visit_count if visit_count > 1 else '')
            print('    {}{}'.format(city, visit_count_display))


class InputFinished(Exception):
    pass


if __name__ == '__main__':
    collect_places()
    print()
    display_places()
