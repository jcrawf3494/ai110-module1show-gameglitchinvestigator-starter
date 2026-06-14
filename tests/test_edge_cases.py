import pytest
from logic_utils import parse_guess, check_guess, update_score


def test_parse_guess_scientific_notation_rejected():
    # "1e2" is not parsed by int(raw) and should be rejected
    ok, guess, err = parse_guess("1e2", low=1, high=1000)
    assert ok is False
    assert guess is None
    assert "not a number" in err


def test_parse_guess_scientific_with_dot_accepted():
    # "1.0e2" contains a dot so float(raw) is attempted and should work -> 100
    ok, guess, err = parse_guess("1.0e2", low=1, high=1000)
    assert ok is True
    assert guess == 100


def test_parse_guess_commas_rejected():
    # Commas in numbers (1,000) should be rejected as non-numeric input
    ok, guess, err = parse_guess("1,000", low=1, high=2000)
    assert ok is False
    assert guess is None
    assert "not a number" in err


def test_parse_guess_whitespace_ok():
    # Leading/trailing whitespace should be tolerated by int()
    ok, guess, err = parse_guess(" 50 ", low=1, high=100)
    assert ok is True
    assert guess == 50


def test_parse_guess_large_integer_out_of_range():
    # Extremely large integers should be parsed but rejected if outside range
    big = "9999999999999999999999999999"
    ok, guess, err = parse_guess(big, low=1, high=100)
    assert ok is False
    assert guess is None


def test_check_guess_with_very_large_ints():
    # Ensure check_guess handles very large integers without overflow
    large = 10 ** 30
    outcome, message = check_guess(large, large)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_with_float_guess():
    # Passing a float guess that equals the secret should still count as a win
    outcome, message = check_guess(50.0, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_update_score_with_negative_attempt_number():
    # Verify behavior with negative attempt numbers (edge-case inputs)
    # The current formula should still compute deterministically.
    new_score = update_score(0, "Win", -10)
    # 100 - 10 * (-10 + 1) = 100 - 10 * -9 = 100 + 90 = 190
    assert new_score == 190
