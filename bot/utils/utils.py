def list_separator(values: list, max_len: int = 3) -> list[list]:
    if len(values) <= max_len:
        return [values]
    return [values[i : i + max_len] for i in range(0, len(values), max_len)]
