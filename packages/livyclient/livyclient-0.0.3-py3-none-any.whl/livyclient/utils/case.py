import re


def hump2underline(val: str):
    """
    :param val: Hump string
    :return: Underlined string
    """
    p = re.compile(r'([a-z]|\d)([A-Z])')
    return re.sub(p, r'\1_\2', val).lower()


def underline2hump(val: str):
    """
    :param val: Underlined string
    :return: Hump string
    """
    return re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), val)


if __name__ == '__main__':
    print(hump2underline('ReadTable'))
    print(underline2hump('read_table'))
