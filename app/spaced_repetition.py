from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

@dataclass
class ReviewResult:
    repetitions: int
    ease_factor: float
    interval: int
    next_review: datetime

def calculate_sm2(repetitions: int, ease_factor: float, interval: int, quality: int) -> ReviewResult:
    if quality<0 or quality>5:
        raise ValueError("Оценка должна быть от 0 до 5")
    if quality >= 3:
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval * ease_factor)
        new_repetitions = repetitions + 1
    else:
        new_interval = 1
        new_repetitions = 0
    new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease_factor = max(1.3, round(new_ease_factor, 2))  # не может быть меньше 1.3

    next_review = datetime.now(timezone.utc) + timedelta(days=new_interval)

    return ReviewResult(
        repetitions=new_repetitions,
        ease_factor=new_ease_factor,
        interval=new_interval,
        next_review=next_review,
    )