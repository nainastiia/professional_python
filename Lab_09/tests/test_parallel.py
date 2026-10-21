import pytest
from threading import Thread
from warehouse_system.analytics import (
    generate_large_dataset,
    calculate_total_value_python,
    calculate_total_value_numpy
)
from warehouse_system.parallel import safe_increment_stock, stock_counter


def test_numpy_and_python_correctness():
    data = generate_large_dataset(1000)
    val_py = calculate_total_value_python(data)
    val_np = calculate_total_value_numpy(data)
    assert abs(val_py - val_np) < 1e-5


def test_lock_prevents_race_condition():
    global stock_counter
    import warehouse_system.parallel as p
    p.stock_counter = 0

    threads = [Thread(target=safe_increment_stock) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert p.stock_counter == 100