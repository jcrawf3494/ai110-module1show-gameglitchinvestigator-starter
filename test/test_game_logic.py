import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


class TestParseGuessRangeValidation:
    """
    Bug Fix #2: Verify that parse_guess() now validates guesses are within the allowed range.
    Previously, guesses outside the range were incorrectly accepted.
    """

    def test_parse_guess_rejects_below_range(self):
        """Guess below range minimum should be rejected."""
        ok, guess_int, err = parse_guess("0", low=1, high=20)
        assert ok is False
        assert guess_int is None
        assert "between 1 and 20" in err

    def test_parse_guess_rejects_above_range(self):
        """Guess above range maximum should be rejected."""
        ok, guess_int, err = parse_guess("101", low=1, high=100)
        assert ok is False
        assert guess_int is None
        assert "between 1 and 100" in err

    def test_parse_guess_accepts_min_boundary(self):
        """Guess at minimum boundary should be accepted."""
        ok, guess_int, err = parse_guess("1", low=1, high=20)
        assert ok is True
        assert guess_int == 1
        assert err is None

    def test_parse_guess_accepts_max_boundary(self):
        """Guess at maximum boundary should be accepted."""
        ok, guess_int, err = parse_guess("100", low=1, high=100)
        assert ok is True
        assert guess_int == 100
        assert err is None

    def test_parse_guess_accepts_middle_value(self):
        """Guess in middle of range should be accepted."""
        ok, guess_int, err = parse_guess("50", low=1, high=100)
        assert ok is True
        assert guess_int == 50
        assert err is None

    def test_parse_guess_rejects_negative_number(self):
        """Negative guess should be rejected when range is positive."""
        ok, guess_int, err = parse_guess("-5", low=1, high=50)
        assert ok is False
        assert guess_int is None
        assert "between 1 and 50" in err

    def test_parse_guess_hard_difficulty_range(self):
        """Hard difficulty range is 1-50, test boundaries."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50
        
        # Should accept 50
        ok, guess_int, err = parse_guess("50", low, high)
        assert ok is True
        assert guess_int == 50
        
        # Should reject 51
        ok, guess_int, err = parse_guess("51", low, high)
        assert ok is False


class TestCheckGuessDirections:
    """
    Bug Fix #4: Verify that check_guess() returns CORRECT hint directions.
    Previously, directions were reversed (said "Go HIGHER!" when should go lower, etc).
    """

    def test_guess_too_high_says_go_lower(self):
        """When guess is too high, hint should say go LOWER."""
        outcome, message = check_guess(50, 25)
        assert outcome == "Too High"
        assert "Go LOWER!" in message
        assert "HIGHER" not in message

    def test_guess_too_low_says_go_higher(self):
        """When guess is too low, hint should say go HIGHER."""
        outcome, message = check_guess(25, 50)
        assert outcome == "Too Low"
        assert "Go HIGHER!" in message
        assert "LOWER" not in message

    def test_guess_correct(self):
        """When guess is correct, should get 'Correct!' message."""
        outcome, message = check_guess(42, 42)
        assert outcome == "Win"
        assert "Correct!" in message

    def test_guess_direction_with_large_numbers(self):
        """Test direction hints with larger numbers."""
        # Too high
        outcome, message = check_guess(100, 1)
        assert outcome == "Too High"
        assert "LOWER" in message

        # Too low
        outcome, message = check_guess(1, 100)
        assert outcome == "Too Low"
        assert "HIGHER" in message

    def test_guess_string_comparison_too_high(self):
        """String comparison: when guess > secret as strings, should say go LOWER."""
        # This tests the TypeError exception handling path
        outcome, message = check_guess("9", "10")
        assert outcome == "Too High"
        assert "LOWER" in message

    def test_guess_string_comparison_too_low(self):
        """String comparison: when guess < secret as strings, should say go HIGHER."""
        outcome, message = check_guess("1", "10")
        assert outcome == "Too Low"
        assert "HIGHER" in message


class TestDifficultyRanges:
    """
    Bug Fix #2: Verify that difficulty ranges are properly used.
    Tests that parse_guess validates against the correct range for each difficulty.
    """

    def test_easy_difficulty_range(self):
        """Easy difficulty should have range 1-20."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

        # Should accept 15
        ok, _, err = parse_guess("15", low, high)
        assert ok is True

        # Should reject 21
        ok, _, err = parse_guess("21", low, high)
        assert ok is False
        assert "between 1 and 20" in err

    def test_normal_difficulty_range(self):
        """Normal difficulty should have range 1-100."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

        # Should accept 100
        ok, _, err = parse_guess("100", low, high)
        assert ok is True

        # Should reject 101
        ok, _, err = parse_guess("101", low, high)
        assert ok is False
        assert "between 1 and 100" in err

    def test_hard_difficulty_range(self):
        """Hard difficulty should have range 1-50."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50

        # Should accept 50
        ok, _, err = parse_guess("50", low, high)
        assert ok is True

        # Should reject 51
        ok, _, err = parse_guess("51", low, high)
        assert ok is False
        assert "between 1 and 50" in err


class TestParseGuessValidation:
    """
    General parse_guess tests for input validation.
    """

    def test_parse_guess_empty_string(self):
        """Empty string should be rejected."""
        ok, guess_int, err = parse_guess("", low=1, high=100)
        assert ok is False
        assert guess_int is None
        assert "Enter a guess" in err

    def test_parse_guess_non_numeric(self):
        """Non-numeric input should be rejected."""
        ok, guess_int, err = parse_guess("abc", low=1, high=100)
        assert ok is False
        assert guess_int is None
        assert "not a number" in err

    def test_parse_guess_float_input(self):
        """Float input should be converted to int."""
        ok, guess_int, err = parse_guess("50.5", low=1, high=100)
        assert ok is True
        assert guess_int == 50  # Should truncate to 50, not round
        assert err is None

    def test_parse_guess_float_outside_range(self):
        """Float outside range should be rejected."""
        ok, guess_int, err = parse_guess("101.5", low=1, high=100)
        assert ok is False
        assert guess_int is None
        assert "between 1 and 100" in err


class TestUpdateScore:
    """
    Score update logic tests.
    """

    def test_update_score_win_first_attempt(self):
        """Winning on first attempt should give high score."""
        new_score = update_score(0, "Win", 1)
        # 100 - 10 * (1 + 1) = 100 - 20 = 80
        assert new_score == 80

    def test_update_score_win_many_attempts(self):
        """Winning on many attempts should give lower score."""
        new_score = update_score(0, "Win", 10)
        # 100 - 10 * (10 + 1) = 100 - 110 = -10, but minimum is 10
        assert new_score == 10

    def test_update_score_too_high_even_attempt(self):
        """Too high on even attempt should add points."""
        new_score = update_score(100, "Too High", 2)
        assert new_score == 105

    def test_update_score_too_high_odd_attempt(self):
        """Too high on odd attempt should subtract points."""
        new_score = update_score(100, "Too High", 1)
        assert new_score == 95

    def test_update_score_too_low(self):
        """Too low should always subtract points."""
        new_score = update_score(100, "Too Low", 1)
        assert new_score == 95

        new_score = update_score(100, "Too Low", 2)
        assert new_score == 95
