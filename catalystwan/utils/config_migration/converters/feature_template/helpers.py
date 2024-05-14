def create_dict_without_none(**kwargs) -> dict:
    """Create a dictionary without None values.
    This speeds up the converting because we don't need to check for None values.
    If pydantic model input doesn't have a key:value pair, it will use a default value."""
    return {k: v for k, v in kwargs.items() if v is not None}
