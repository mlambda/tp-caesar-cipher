from typing import Any
from unittest import TestCase

from deal import PreContractError
from hypothesis import given
from hypothesis.strategies import characters, composite, integers, lists

from tp_caesar_cipher.caesar_cipher import rotate


@composite
def keys(draw: Any) -> list[int]:
    keys = draw(lists(integers(min_value=0, max_value=25)))
    rest = sum(keys) % 26
    if rest != 0:
        keys.append(26 - rest)
    return keys


class TestCaesarCipher(TestCase):
    def test_rotate_a_by_0_same_output_as_input(self) -> None:
        self.assertEqual(rotate("a", 0), "a")

    def test_rotate_a_by_1(self) -> None:
        self.assertEqual(rotate("a", 1), "b")

    def test_rotate_m_by_13(self) -> None:
        self.assertEqual(rotate("m", 13), "z")

    def test_rotate_n_by_13_with_wrap_around_alphabet(self) -> None:
        self.assertEqual(rotate("n", 13), "a")

    def test_rotate_capital_letters(self) -> None:
        self.assertEqual(rotate("OMG", 5), "TRL")

    def test_rotate_spaces(self) -> None:
        self.assertEqual(rotate("O M G", 5), "T R L")

    def test_rotate_numbers(self) -> None:
        self.assertEqual(rotate("Testing 1 2 3 testing", 4), "Xiwxmrk 1 2 3 xiwxmrk")

    def test_rotate_punctuation(self) -> None:
        self.assertEqual(rotate("Let's eat, Grandma!", 21), "Gzo'n zvo, Bmviyhv!")

    def test_rotate_all_letters(self) -> None:
        self.assertEqual(
            rotate("The quick brown fox jumps over the lazy dog.", 13),
            "Gur dhvpx oebja sbk whzcf bire gur ynml qbt.",
        )

    @given(characters())
    def test_length(self, characters: str) -> None:
        self.assertEqual(len(characters), len(rotate(characters, 13)))

    @given(keys(), characters())
    def test_many_rotate(self, keys: list[int], characters: str) -> None:
        current = characters
        for key in keys:
            current = rotate(current, key)
        self.assertEqual(characters, current)

    @given(characters())
    def test_double_rotate(self, characters: str) -> None:
        self.assertEqual(characters, rotate(rotate(characters, 13), 13))

    def test_bad_key(self) -> None:
        with self.assertRaises(PreContractError):
            rotate("The quick brown fox jumps over the lazy dog.", 26)
