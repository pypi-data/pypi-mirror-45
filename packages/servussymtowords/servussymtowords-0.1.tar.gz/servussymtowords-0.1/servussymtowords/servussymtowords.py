#!/usr/bin/env python3

from re import findall, IGNORECASE

from num2words import num2words
from caseireplace import case_insensitive_replace

from servusnumre import float_pattern, exponent_pattern

from typing import Dict, List, Union

float_number = f"{float_pattern}{exponent_pattern}"

IntFloat = Union[int, float]
IntFloatStr = Union[int, float, str]

symbol_word_dict: Dict[str, str] = {
    "h": "hour",
    "m": "minute",
    "s": "second"
    }


def find_number_and_unit(text: str, unit: str) -> List[str]:
    """
    Find {number}{unit} in text.
    :param text: str: Text to search for pattern.
    :param unit: str: Unit to search for.

    """
    return [
        x for x in findall(
            rf"((?:{float_number}){unit})",
            text,
            IGNORECASE
            )
        ]


def find_number(text: str) -> str:
    """
    Find number on a text.
    :param text: str: Text to search for pattern.

    """
    return findall(rf"(?:{float_number})", text)[0]


def int_or_float(number: IntFloatStr) -> IntFloat:
    """
    Return int or float if it's necessary.
    :param number: IntFloatStr: Number to be converted.

    """
    number = float(number)
    if number % 1 == 0:
        return int(number)
    return number


def text_singular_or_plural(text: str, number: IntFloatStr) -> str:
    """
    Add an s to a string if required.
    :param text: str: Text to add or not an "s"
    :param number: IntFloatStr: Number.

    """
    if abs(float(number)) // 1 not in [1, -1]:
        text += "s"
    return text


def singular_or_plural_units(
    text: str,
    text_substrings: List[str],
    unit_as_text: str
        ) -> str:
    """
    Singular or plural operating with desired unit.
    :param text: str: Text to replace pattern.
    :param text_substrings: List[str]: substrings to be converted.
    :param unit_as_text: str: To be used by text_singular_or_plural.

    """
    for unit in text_substrings:
        number = find_number(unit)
        text = text.replace(
            unit,
            f"{num2words(int_or_float(number))} "
            f"{text_singular_or_plural(unit_as_text, number)}"
            )
    return text


def celsius_degrees_text(text: str) -> str:
    """
    Search for and convert to words {number}°C.
    :param text: str: Text to convert.

    """
    return singular_or_plural_units(
        text=text,
        text_substrings=find_number_and_unit(text, "°C"),
        unit_as_text="Celsius degree"
        )


def fahrenheit_degrees_text(text: str) -> str:
    """
    Search for and convert to words {number}°F.
    :param text: str: Text to convert.

    """
    return singular_or_plural_units(
        text=text,
        text_substrings=find_number_and_unit(text, "°F"),
        unit_as_text="Fahrenheit degree"
        )


def kelvin_degrees_text(text: str) -> str:
    """
    Search for and convert to words {number}°K.
    :param text: str: Text to convert.

    """
    return singular_or_plural_units(
        text=text,
        text_substrings=find_number_and_unit(text, "°K"),
        unit_as_text="Kelvin degree"
        )


def kilometers_text(text: str) -> str:
    """
    Search for and convert to words {number}Km/time.
    :param text: str: Text to convert.

    """
    kilometers_list = find_number_and_unit(text, "Km")
    for kilometers in kilometers_list:
        number = int_or_float(find_number(kilometers))
        text = text.replace(
            kilometers,
            f"{num2words(number)} "
            f"{text_singular_or_plural('Kilometer', number)}"
            )
    per_time_list = findall(
        r"Kilometer[s]*/[h|m|s]",
        text,
        IGNORECASE
        )
    for time in per_time_list:
        symbol = time.split("/")[1]
        if symbol in symbol_word_dict.keys():
            word = symbol_word_dict[symbol]

        plural = time.split("/")[0].endswith("s")
        if plural:
            text = case_insensitive_replace(
                text=text,
                old=f"kilometers/{symbol}",
                new=f"Kilometers per {word}"
                )
        else:
            text = case_insensitive_replace(
                text=text,
                old=f"Kilometer/{symbol}",
                new=f"Kilometer per {word}"
                )

    return text


def symbols_to_words(text: str) -> str:
    """
    Convert °C, °F, °K and Km/time to words.

    :param text: str: Text to search for pattern.

    """
    text = celsius_degrees_text(text)
    text = fahrenheit_degrees_text(text)
    text = kelvin_degrees_text(text)
    text = kilometers_text(text)
    return text


def numbers_to_words(text: str) -> str:
    """
    Convert numbers to words.
    :param text: str: Text to convert.

    """
    numbers = findall(
        rf"({float_number})",
        text
        )
    for number in numbers:
        text = text.replace(
            number,
            num2words(int_or_float(float(number)))
            )
    return text


def units_and_numbers_to_words(text: str) -> str:
    """
    Convert units and numbers to words.
    :param text: str: Text to convert.

    """
    text = symbols_to_words(text)
    text = numbers_to_words(text)
    return text
