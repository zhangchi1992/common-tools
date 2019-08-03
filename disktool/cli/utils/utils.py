def explode_array(list_str, separator=","):
    """
    Explode list string into array
    """
    if not list_str:
        return []
    return [item.strip() for item in list_str.split(separator) if item.strip() != '']