def find_key_in_nested_dict(dictionary, target_key):
    if target_key in dictionary:
        return dictionary[target_key]

    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = find_key_in_nested_dict(value, target_key)
            if result is not None:
                return result

    return None


def find_key_or_value_in_nested_dict(dictionary, target):
    if target in dictionary:
        return dictionary[target]

    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = find_key_or_value_in_nested_dict(value, target)
            if result is not None:
                return result
        elif isinstance(value, list) and target in value:
            return value

    return None
