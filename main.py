from itertools import product
from typing import Generator

import numpy as np

from display import display_possible

# Answers:
# Day 1  - 162
# Day 2  - 840
# Day 3  - 369
# Day 4  - 625
# Day 5  - 315
# Day 6  - 128
# Day 7  - 476
# Day 8  - 840
# Day 9  - 532
# Day 10 - 800
# Day 11 - 987
# Day 12 - 143
# Day 13 - 564
# Day 14 - 614
# Day 15 - 243

# fmt: off
SHOTS_MADE = {
    5:  [(3 , 7 ), (12, 12), (2 , 12), (13, 13), (3 , 12)],
    6:  [(5 , 5 ), (5 , 9 ), (5 , 14), (5 , 15), (5 , 16)],
    7:  [(20, 1 ), (20, 3 ), (20, 19), (1 , 17), (8 , 5 )],
    8:  [(12, 6 ), (10, 6 ), (20, 6 ), (10, 10), (4 , 6 )],
    9:  [(13, 3 ), (13, 12), (13, 4 ), (17, 3 ), (3 , 9 )],
    10: [(9 , 12), (10, 12), (11, 12), (5 , 20), (7 , 20)],
    11: [(18, 5 ), (14, 5 ), (2 , 5 ), (6 , 5 ), (7 , 5 )],
    12: [(4 , 20), (20, 20), (12, 20), (14, 20), (16, 20)],
    13: [(4 , 10), (7 , 10), (11, 10), (9 , 10), (10, 10)],
    14: [],
    15: [(2 , 19), (6 , 19), (14, 19), (18, 19), (10, 19)],
    16: [(1 , 4 ), (17, 4 ), (16, 4 ), (15, 4 ), (2 , 4 )],
}
# fmt: on


def all_possible():
    return product(*(range(1, 21) for _ in range(4)))


def was_shot_at(day: int, x: int, y: int) -> bool:
    assert 1 <= day <= 25 and 1 <= x <= 20 and 1 <= y <= 20
    if day not in SHOTS_MADE:
        return False

    for shot in SHOTS_MADE[day]:
        if shot == (x, y):
            return True

    return False


def positions_each_day(
    x0: int, y0: int, dx: int, dy: int
) -> Generator[tuple[int, int, int], None, None]:
    assert 1 <= x0 <= 20 and 1 <= y0 <= 20 and 1 <= dx <= 20 and 1 <= dy <= 20
    x, y = x0, y0
    for day in range(1, 26):
        yield day, x, y

        x += dx
        y += dy

        if x > 20:
            x -= 20
        if y > 20:
            y -= 20


print("Simulating red drone...")
red_possible = np.zeros((25, 20, 20))
for x0, y0, dx, dy in all_possible():
    # Day 1 clue
    if dy != 1:
        continue

    # Day 2 clue
    if 840 % dx != 0:
        continue

    # Day 6 clue
    if 128 % dx == 0:
        continue

    # Day 11 clue
    if dx not in (7, 8, 9):
        continue

    for day, x, y in positions_each_day(x0, y0, dx, dy):
        if was_shot_at(day, x, y):
            # Ignore where shot down
            if day != 7 or (x, y) != (20, 19):
                break

        # Day 4 clue
        if day == 2 and x != 5:
            break

        # Shot down!
        if day == 7 and (x, y) != (20, 19):
            break
    else:
        for day, x, y in positions_each_day(x0, y0, dx, dy):
            # Day 10 clue
            if day == 8:
                # Relying on this for orange to be correct
                assert y == 20

            # Day 13 clue
            if day == 10:
                # Relying on this for blue and orange to be correct
                assert y != 4

            red_possible[day - 1, x - 1, y - 1] += 1
assert all(day_sum >= 1 for day_sum in red_possible.sum(axis=(1, 2)))

print("Simulating blue drone...")
blue_possible = np.zeros((25, 20, 20))
for x0, y0, dx, dy in all_possible():
    # Day 3 clue
    if dx in (3, 6, 9):
        continue

    # Day 5 clue
    if dy in (3, 1, 5):
        continue

    # Day 7 clue
    if dy in (4, 7, 6):
        continue

    # Day 8 clue
    if 840 % dy != 0:
        continue

    # Day 15 clue
    if dy % 2 == 0:
        continue

    for day, x, y in positions_each_day(x0, y0, dx, dy):
        if was_shot_at(day, x, y):
            break

        # Day 13 clue
        # Can rely on this due to assertion in red
        if day == 6 and y != 4:
            break

        # Day 14 clue
        if day == 4 and y != 14:
            break
    else:
        for day, x, y in positions_each_day(x0, y0, dx, dy):
            # Day 10 clue
            if day == 8:
                # Relying on this for orange to be correct
                assert y != 20

            blue_possible[day - 1, x - 1, y - 1] += 1
assert all(day_sum >= 1 for day_sum in blue_possible.sum(axis=(1, 2)))

print("Simulating orange drone...")
orange_possible = np.zeros((25, 20, 20))
for x0, y0, dx, dy in all_possible():
    # Day 12 clue
    if dx not in (1, 4, 3):
        continue

    # Day 16 clue
    if dx not in (2, 3, 4):
        continue

    for day, x, y in positions_each_day(x0, y0, dx, dy):
        if was_shot_at(day, x, y):
            break

        # Day 9 clue
        if day == 5 and y == 6:
            break

        # Day 10 clue
        # Can rely on this due to assertions for red and blue
        if day == 8 and y != 20:
            break

        # Day 13 clue
        # Can rely on this due to assertion in red
        if day == 6 and y != 4:
            break
    else:
        for day, x, y in positions_each_day(x0, y0, dx, dy):
            orange_possible[day - 1, x - 1, y - 1] += 1
assert all(day_sum >= 1 for day_sum in orange_possible.sum(axis=(1, 2)))

display_possible(blue_possible, orange_possible, days=range(16, 26))
