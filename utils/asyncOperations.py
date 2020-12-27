import asyncio

async def aiter(iterable):
    """Asynchronously iterates through an object

    Due to how most responses will use store dictionaries in a list,
    this function will help to iterate through them while remaining
    asynchronous.

    Parameters
    ----------
    iterable : str, list, etc.
        the object the iterator will iterate through

    Returns
    -------
    ...

    Raises
    ------
    ...
    """
    for item in iterable:
        yield item