from string import ascii_lowercase, ascii_uppercase
from typing import Dict, Optional

import deal


def make_table(characters: str, key: int) -> Dict[int, Optional[int]]:
    key %= 26
    return str.maketrans(characters, characters[key:] + characters[:key])


@deal.pre(lambda text, key: 0 <= key < 26)
def rotate(text: str, key: int) -> str:
    table = {**make_table(ascii_lowercase, key), **make_table(ascii_uppercase, key)}
    return text.translate(table)
