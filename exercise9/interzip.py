def interzip(*iterables):
    for parallel_elements in zip(*iterables):
        for element in parallel_elements:
            yield element
