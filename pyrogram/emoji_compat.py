"""Emoji constants that existed in pyroblack <= 2.7.6 but not in the current table.

``pyrogram/emoji.py`` is regenerated from the Unicode CLDR names, and that
regeneration renamed or dropped 215 constants. Applications that referenced them
(``from pyrogram.emoji import BULLSEYE``) broke on the rebase.

Editing the generated file directly would lose the fix on the next regeneration,
so the old names are declared here instead and grafted onto :mod:`pyrogram.emoji`
by :func:`install` during ``import pyrogram``.

Two kinds of entries:

``RENAMED``
    the emoji still exists under a new CLDR name; the old name aliases it, so
    the value tracks whatever the generated table says.

``REMOVED``
    the name is gone entirely; the original codepoints are kept verbatim.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

# old name -> current name in pyrogram.emoji
RENAMED: dict[str, str] = {
    "BLUE_CIRCLE": "LARGE_BLUE_CIRCLE",
    "BLUE_SQUARE": "LARGE_BLUE_SQUARE",
    "BROWN_CIRCLE": "LARGE_BROWN_CIRCLE",
    "BROWN_SQUARE": "LARGE_BROWN_SQUARE",
    "BULLSEYE": "DIRECT_HIT",
    "EIGHT_O_CLOCK": "EIGHT_OCLOCK",
    "ELEVEN_O_CLOCK": "ELEVEN_OCLOCK",
    "ENRAGED_FACE": "POUTING_FACE",
    "FACE_WITH_CROSSED_OUT_EYES": "DIZZY_FACE",
    "FIVE_O_CLOCK": "FIVE_OCLOCK",
    "FLAG_ANTIGUA_ANDAMP_BARBUDA": "FLAG_ANTIGUA_BARBUDA",
    "FLAG_BOSNIA_ANDAMP_HERZEGOVINA": "FLAG_BOSNIA_HERZEGOVINA",
    "FLAG_CEUTA_ANDAMP_MELILLA": "FLAG_CEUTA_MELILLA",
    "FLAG_COTE_D_IVOIRE": "FLAG_COTE_DIVOIRE",
    "FLAG_HEARD_ANDAMP_MCDONALD_ISLANDS": "FLAG_HEARD_MCDONALD_ISLANDS",
    "FLAG_SAO_TOME_ANDAMP_PRINCIPE": "FLAG_SAO_TOME_PRINCIPE",
    "FLAG_SOUTH_GEORGIA_ANDAMP_SOUTH_SANDWICH_ISLANDS": "FLAG_SOUTH_GEORGIA_SOUTH_SANDWICH_ISLANDS",
    "FLAG_ST_KITTS_ANDAMP_NEVIS": "FLAG_ST_KITTS_NEVIS",
    "FLAG_ST_PIERRE_ANDAMP_MIQUELON": "FLAG_ST_PIERRE_MIQUELON",
    "FLAG_ST_VINCENT_ANDAMP_GRENADINES": "FLAG_ST_VINCENT_GRENADINES",
    "FLAG_SVALBARD_ANDAMP_JAN_MAYEN": "FLAG_SVALBARD_JAN_MAYEN",
    "FLAG_TRINIDAD_ANDAMP_TOBAGO": "FLAG_TRINIDAD_TOBAGO",
    "FLAG_TURKS_ANDAMP_CAICOS_ISLANDS": "FLAG_TURKS_CAICOS_ISLANDS",
    "FLAG_U_S_OUTLYING_ISLANDS": "FLAG_US_OUTLYING_ISLANDS",
    "FLAG_U_S_VIRGIN_ISLANDS": "FLAG_US_VIRGIN_ISLANDS",
    "FLAG_WALLIS_ANDAMP_FUTUNA": "FLAG_WALLIS_FUTUNA",
    "FOUR_O_CLOCK": "FOUR_OCLOCK",
    "GREEN_CIRCLE": "LARGE_GREEN_CIRCLE",
    "GREEN_SQUARE": "LARGE_GREEN_SQUARE",
    "MAN_S_SHOE": "MANS_SHOE",
    "MEN_S_ROOM": "MENS_ROOM",
    "NINE_O_CLOCK": "NINE_OCLOCK",
    "ONE_O_CLOCK": "ONE_OCLOCK",
    "ORANGE_CIRCLE": "LARGE_ORANGE_CIRCLE",
    "ORANGE_SQUARE": "LARGE_ORANGE_SQUARE",
    "PURPLE_CIRCLE": "LARGE_PURPLE_CIRCLE",
    "PURPLE_SQUARE": "LARGE_PURPLE_SQUARE",
    "RED_CIRCLE": "LARGE_RED_CIRCLE",
    "RED_EXCLAMATION_MARK": "EXCLAMATION_MARK",
    "RED_QUESTION_MARK": "QUESTION_MARK",
    "RED_SQUARE": "LARGE_RED_SQUARE",
    "RESCUE_WORKER_S_HELMET": "RESCUE_WORKERS_HELMET",
    "SEVEN_O_CLOCK": "SEVEN_OCLOCK",
    "SIX_O_CLOCK": "SIX_OCLOCK",
    "SMILING_FACE_WITH_OPEN_HANDS": "HUGGING_FACE",
    "TEN_O_CLOCK": "TEN_OCLOCK",
    "THREE_O_CLOCK": "THREE_OCLOCK",
    "TWELVE_O_CLOCK": "TWELVE_OCLOCK",
    "TWO_O_CLOCK": "TWO_OCLOCKTIME",
    "WATER_PISTOL": "PISTOL",
    "WOMAN_S_BOOT": "WOMANS_BOOT",
    "WOMAN_S_CLOTHES": "WOMANS_CLOTHES",
    "WOMAN_S_HAT": "WOMANS_HAT",
    "WOMAN_S_SANDAL": "WOMANS_SANDAL",
    "WOMAN_WITH_HEADSCARF": "PERSON_WITH_HEADSCARF",
    "WOMEN_S_ROOM": "WOMENS_ROOM",
    "YELLOW_CIRCLE": "LARGE_YELLOW_CIRCLE",
    "YELLOW_SQUARE": "LARGE_YELLOW_SQUARE",
}

# old name -> original codepoints (no current equivalent)
REMOVED: dict[str, str] = {
    "ASTERISK": "*\ufe0f",
    "CANCEL_TAG": "\U000e007f",
    "COMBINING_ENCLOSING_KEYCAP": "\u20e3",
    "DIAMOND_WITH_A_DOT": "\U0001f4a0",
    "DIGIT_EIGHT": "8\ufe0f",
    "DIGIT_FIVE": "5\ufe0f",
    "DIGIT_FOUR": "4\ufe0f",
    "DIGIT_NINE": "9\ufe0f",
    "DIGIT_ONE": "1\ufe0f",
    "DIGIT_SEVEN": "7\ufe0f",
    "DIGIT_SIX": "6\ufe0f",
    "DIGIT_THREE": "3\ufe0f",
    "DIGIT_TWO": "2\ufe0f",
    "DIGIT_ZERO": "0\ufe0f",
    "E_MAIL": "\U0001f4e7",
    "FEMALE_SIGN": "\u2640\ufe0f",
    "HASH_SIGN": "#\ufe0f",
    "MALE_SIGN": "\u2642\ufe0f",
    "MEDICAL_SYMBOL": "\u2695\ufe0f",
    "PERSON_IN_BED_DARK_SKIN_TONE": "\U0001f6cc\U0001f3ff",
    "PERSON_IN_BED_LIGHT_SKIN_TONE": "\U0001f6cc\U0001f3fb",
    "PERSON_IN_BED_MEDIUM_DARK_SKIN_TONE": "\U0001f6cc\U0001f3fe",
    "PERSON_IN_BED_MEDIUM_LIGHT_SKIN_TONE": "\U0001f6cc\U0001f3fc",
    "PERSON_IN_BED_MEDIUM_SKIN_TONE": "\U0001f6cc\U0001f3fd",
    "SNOWBOARDER_DARK_SKIN_TONE": "\U0001f3c2\U0001f3ff",
    "SNOWBOARDER_LIGHT_SKIN_TONE": "\U0001f3c2\U0001f3fb",
    "SNOWBOARDER_MEDIUM_DARK_SKIN_TONE": "\U0001f3c2\U0001f3fe",
    "SNOWBOARDER_MEDIUM_LIGHT_SKIN_TONE": "\U0001f3c2\U0001f3fc",
    "SNOWBOARDER_MEDIUM_SKIN_TONE": "\U0001f3c2\U0001f3fd",
    "VARIATION_SELECTOR_16": "\ufe0f",
    "WOMAN_WITH_HEADSCARF_DARK_SKIN_TONE": "\U0001f9d5\U0001f3ff",
    "WOMAN_WITH_HEADSCARF_LIGHT_SKIN_TONE": "\U0001f9d5\U0001f3fb",
    "WOMAN_WITH_HEADSCARF_MEDIUM_DARK_SKIN_TONE": "\U0001f9d5\U0001f3fe",
    "WOMAN_WITH_HEADSCARF_MEDIUM_LIGHT_SKIN_TONE": "\U0001f9d5\U0001f3fc",
    "WOMAN_WITH_HEADSCARF_MEDIUM_SKIN_TONE": "\U0001f9d5\U0001f3fd",
    "ZERO_WIDTH_JOINER": "\u200d",
}

# Regional indicator letters and the tag characters used to build subdivision
# flags: 26 + 26 + 26 + digits + punctuation. Generated below instead of being
# spelled out, since the codepoints are contiguous.
for _i, _letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    REMOVED[f"REGIONAL_INDICATOR_SYMBOL_LETTER_{_letter}"] = chr(0x1F1E6 + _i)
    REMOVED[f"TAG_LATIN_CAPITAL_LETTER_{_letter}"] = chr(0xE0041 + _i)
    REMOVED[f"TAG_LATIN_SMALL_LETTER_{_letter}"] = chr(0xE0061 + _i)

for _digit in range(10):
    REMOVED[
        f"TAG_DIGIT_{('ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE')[_digit]}"
    ] = chr(0xE0030 + _digit)

_TAG_PUNCTUATION = {
    "TAG_SPACE": 0x20,
    "TAG_EXCLAMATION_MARK": 0x21,
    "TAG_QUOTATION_MARK": 0x22,
    "TAG_NUMBER_SIGN": 0x23,
    "TAG_DOLLAR_SIGN": 0x24,
    "TAG_PERCENT_SIGN": 0x25,
    "TAG_AMPERSAND": 0x26,
    "TAG_APOSTROPHE": 0x27,
    "TAG_LEFT_PARENTHESIS": 0x28,
    "TAG_RIGHT_PARENTHESIS": 0x29,
    "TAG_ASTERISK": 0x2A,
    "TAG_PLUS_SIGN": 0x2B,
    "TAG_COMMA": 0x2C,
    "TAG_HYPHEN_MINUS": 0x2D,
    "TAG_FULL_STOP": 0x2E,
    "TAG_SOLIDUS": 0x2F,
    "TAG_COLON": 0x3A,
    "TAG_SEMICOLON": 0x3B,
    "TAG_LESS_THAN_SIGN": 0x3C,
    "TAG_EQUALS_SIGN": 0x3D,
    "TAG_GREATER_THAN_SIGN": 0x3E,
    "TAG_QUESTION_MARK": 0x3F,
    "TAG_COMMERCIAL_AT": 0x40,
    "TAG_LEFT_SQUARE_BRACKET": 0x5B,
    "TAG_REVERSE_SOLIDUS": 0x5C,
    "TAG_RIGHT_SQUARE_BRACKET": 0x5D,
    "TAG_CIRCUMFLEX_ACCENT": 0x5E,
    "TAG_LOW_LINE": 0x5F,
    "TAG_GRAVE_ACCENT": 0x60,
    "TAG_LEFT_CURLY_BRACKET": 0x7B,
    "TAG_VERTICAL_LINE": 0x7C,
    "TAG_RIGHT_CURLY_BRACKET": 0x7D,
    "TAG_TILDE": 0x7E,
}
for _name, _ascii in _TAG_PUNCTUATION.items():
    REMOVED[_name] = chr(0xE0000 + _ascii)

del _i, _letter, _digit, _name, _ascii, _TAG_PUNCTUATION


def install(module: ModuleType) -> list[str]:
    """Bind the legacy names onto *module* (:mod:`pyrogram.emoji`).

    Returns the names that were added. Existing attributes are never
    overwritten, so a future regeneration that reintroduces one of these names
    wins over the shim.
    """
    added = []

    for old, new in RENAMED.items():
        if hasattr(module, old):
            continue
        value = getattr(module, new, None)
        if value is None:
            continue
        setattr(module, old, value)
        added.append(old)

    for name, value in REMOVED.items():
        if hasattr(module, name):
            continue
        setattr(module, name, value)
        added.append(name)

    return added
