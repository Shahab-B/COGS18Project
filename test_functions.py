"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""

from app import format_fix

## Tests the function used to fix formatting from the api and language


def test_format_fix():
	##Performs test on the format_fix() function inside app.py

    assert format_fix("hi<test>hi") == "hihi"
    assert format_fix("hf") == "hf"
    assert format_fix("<a> something <\a>") == " something "
    assert format_fix("w/") == "with"

test_format_fix()
