
def get_value(dict, key):
    if key == None or dict == None:
        print(dict, key)
    return dict[key] if key in dict else 0
