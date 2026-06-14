def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Helper class so callers can either unpack (outcome, message)
    # or compare the return value directly to a string.
    class GuessResult:
        def __init__(self, outcome: str, message: str):
            self.outcome = outcome
            self.message = message

        def __iter__(self):
            return iter((self.outcome, self.message))

        def __eq__(self, other):
            # Allow direct comparison to the outcome string
            if isinstance(other, str):
                return other == self.outcome
            # Allow comparison to tuple (outcome, message)
            if isinstance(other, tuple):
                return (self.outcome, self.message) == other
            return False

        def __repr__(self):
            return f"GuessResult({self.outcome!r}, {self.message!r})"

    # Normalize types so comparisons work whether secret is str or int
    if guess == secret:
        return GuessResult("Win", "🎉 Correct!")

    try:
        if guess > secret:
            return GuessResult("Too High", "📉 Go LOWER!")
        else:
            return GuessResult("Too Low", "📈 Go HIGHER!")
    except TypeError:
        g = str(guess)
        if g == secret:
            return GuessResult("Win", "🎉 Correct!")
        if g > secret:
            return GuessResult("Too High", "📉 Go LOWER!")
        return GuessResult("Too Low", "📈 Go HIGHER!")


def get_hint_message(outcome: str) -> str:
    """Return a user-facing hint message for an outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
