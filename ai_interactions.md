# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Scientific notation rejected ("1e2") | See "Prompts used" below | `test_parse_guess_scientific_notation_rejected` | Yes | Ensure plain scientific notation without a dot is not accidentally parsed by `int()`.
| Scientific notation with dot accepted ("1.0e2") | See "Prompts used" below | `test_parse_guess_scientific_with_dot_accepted` | Yes | Confirm `float()` path handles dotted scientific notation and converts correctly.
| Commas in numbers ("1,000") | See "Prompts used" below | `test_parse_guess_commas_rejected` | Yes | Comma-separated thousands are common user input but not valid for `int()`; assert rejection.
| Leading/trailing whitespace (" 50 ") | See "Prompts used" below | `test_parse_guess_whitespace_ok` | Yes | Users often paste/enter whitespace; `int()` should tolerate it and parse correctly.
| Extremely large integer out-of-range | See "Prompts used" below | `test_parse_guess_large_integer_out_of_range` | Yes | Very large values should be parsed (or rejected) deterministically and validated against range.
| Very large ints in `check_guess` | See "Prompts used" below | `test_check_guess_with_very_large_ints` | Yes | Ensure no overflow/precision issues when comparing very large integers.
| Float guesses equal to secret (50.0 vs 50) | See "Prompts used" below | `test_check_guess_with_float_guess` | Yes | Confirm numeric equality between float and int behaves as a win.
| `update_score` with negative attempt number | See "Prompts used" below | `test_update_score_with_negative_attempt_number` | Yes | Document deterministic formula behavior for unexpected negative inputs.

### Prompts used

```
Create pytest edge-case tests for the game's parsing and logic functions. Cover cases including:
- scientific notation ("1e2" and "1.0e2"),
- numbers containing commas ("1,000"),
- leading/trailing whitespace (" 50 "),
- extremely large integers,
- float guesses (50.0 vs 50), and
- odd inputs to scoring (negative attempt numbers).

For each edge case, write a concise pytest that asserts the expected behavior and add a one-line comment explaining why the case is important.
```

Each table row above maps the generated test to a one-line justification for why that edge case was included.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
