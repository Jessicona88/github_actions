import time
from your_module import Timer


def test_timer_start_sets_fields():
    timer = Timer("Test timer")

    timer.start()

    assert timer.running is True
    assert timer.start_time is not None
    assert isinstance(timer.start_time, float)
    assert timer.start_time <= time.time()
