################################################################################
# XML Generator


def myxml(tag: str, content: str = "", **kwargs) -> str:
    """Converts arguments into a XML formatted string.

    Args:
        tag: Name of the tag
        content: Text placed between the opening/closing tags
        *args: Attributes inside of the opening tag

    Returns:
        XML formatted string
    """
    # Attempt 1:
    # if kwargs:
    #     attributes = " " + " ".join(
    #         ["=".join([key, str(value)]) for key, value in kwargs.items()]
    #     )
    # else:
    #     attributes = ""
    # return f"<{tag}{attributes}>{content}</{tag}>"

    # Attempt 2:
    attributes = (
        "".join([f" {key}={value}" for key, value in kwargs.items()]) if kwargs else ""
    )
    return f"<{tag}{attributes}>{content}</{tag}>"


def factorial(*args) -> int:
    """Yet another function that takes any number of numeric arguments and returns the result of
    multiplying them all by one another."""
    result = 1
    for arg in args:
        result = result * arg
    return result
