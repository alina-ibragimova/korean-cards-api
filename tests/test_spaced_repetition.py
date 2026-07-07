import pytest
from app.spaced_repetition import calculate_sm2


def test_first_correct_review():
    result = calculate_sm2(repetitions=0, ease_factor=2.5, interval=0, quality=5)
    assert result.repetitions == 1
    assert result.interval == 1


def test_second_correct_review():
    result = calculate_sm2(repetitions=1, ease_factor=2.5, interval=1, quality=5)
    assert result.repetitions == 2
    assert result.interval == 6


def test_wrong_answer_resets():
    result = calculate_sm2(repetitions=5, ease_factor=2.5, interval=30, quality=1)
    assert result.repetitions == 0
    assert result.interval == 1


def test_ease_factor_increases_on_easy():
    result = calculate_sm2(repetitions=1, ease_factor=2.5, interval=1, quality=5)
    assert result.ease_factor > 2.5


def test_ease_factor_decreases_on_hard():
    result = calculate_sm2(repetitions=1, ease_factor=2.5, interval=1, quality=3)
    assert result.ease_factor < 2.5


def test_ease_factor_never_below_minimum():
    result = calculate_sm2(repetitions=1, ease_factor=1.3, interval=1, quality=0)
    assert result.ease_factor >= 1.3


def test_invalid_quality_raises_error():
    with pytest.raises(ValueError):
        calculate_sm2(repetitions=0, ease_factor=2.5, interval=0, quality=6)