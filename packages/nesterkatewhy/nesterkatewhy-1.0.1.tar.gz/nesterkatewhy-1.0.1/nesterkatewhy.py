""" This is the nester.py module that provides a function. This function can print the item of a list."""

def print_lol(data):
    for item in data:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)

