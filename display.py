from typing import Iterable

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def largest_indices(ary: np.ndarray, n: int):
    """Returns the n largest indices from a numpy array."""
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return zip(*np.unravel_index(indices, ary.shape), strict=True)


def display_possible(
    *drones_days_counts: np.ndarray, days: Iterable[int] = range(1, 26)
):
    for day in days:
        # Combine and normalize the counts in that day to percentages
        data = np.ones((20, 20))
        for drone_days_counts in drones_days_counts:
            drone_day_counts = np.swapaxes(drone_days_counts[day - 1], 0, 1)
            drone_day_probabilities = drone_day_counts / drone_day_counts.sum()
            data *= 1 - drone_day_probabilities

        data = 1 - data

        data = np.pad(data, ((1, 0), (1, 0))) * 100

        fig, ax = plt.subplots()
        im = ax.imshow(data, vmin=0, vmax=4, origin="lower", cmap="gist_ncar")
        ax.set_xticks(range(1, 21))
        ax.set_yticks(range(1, 21))

        ax.set_ylim(0.5)
        ax.set_xlim(0.5)

        old_fmt = ax.format_coord
        ax.format_coord = lambda x, y, old_fmt=old_fmt: old_fmt(round(x), round(y))

        ax.grid(which="minor", color="black", linestyle="-", linewidth=2)

        # Show the minor ticks and grid.
        ax.minorticks_on()
        # Now hide the minor ticks (but leave the gridlines).
        ax.tick_params(which="minor", bottom=False, left=False)

        # Only show minor gridlines once in between major gridlines.
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))

        for i, (y, x) in enumerate(largest_indices(data, 5), 1):
            ax.text(x, y, f"{i}", ha="center", va="center", color="black")

        fig.colorbar(im, ax=ax, label="Probability of hit (%)")
        ax.set_title(f"Day {day}")

        fig.tight_layout()
        plt.show()
