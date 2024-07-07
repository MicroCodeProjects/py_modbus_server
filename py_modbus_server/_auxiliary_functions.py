from typeguard import check_type, TypeCheckError


def is_type(value, expected_type, **kwargs):
    """Check if value is of the expected type"""

    try:
        check_type(value, expected_type, **kwargs)
        return True
    except TypeCheckError:
        return False
