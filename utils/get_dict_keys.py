def get_keys(dictionary: dict, level: int):
    keys = []

    def find_keys(d, current_level):
        for key, value in d.items():
            if current_level == level:
                keys.append(key)
            elif isinstance(value, dict):
                find_keys(value, current_level + 1)

    find_keys(dictionary, 1)
    return keys


def get_leaf_values(dictionary):
    leaf_values = []

    def traverse(d):
        for key, value in d.items():
            if isinstance(value, dict):
                traverse(value)
            else:
                leaf_values.append(value)

    traverse(dictionary)
    return leaf_values


def find_path(nested_dict, target_value, path=None):
    if path is None:
        path = []
    for key, value in nested_dict.items():
        new_path = path + [key]
        if key == target_value or value == target_value or target_value in value:
            return new_path
        elif isinstance(value, dict):
            result = find_path(value, target_value, new_path)
            if result:
                return result
    return None
