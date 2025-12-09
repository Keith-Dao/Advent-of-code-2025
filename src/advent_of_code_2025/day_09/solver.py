"""Day 9 solver."""

import bisect
import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    import pathlib

    Point = tuple[int, int]
    Line = tuple[int, int, int]

from .. import base


class Solver(base.Solver):
    """Day 9 solver."""

    def _parse_input(self, filepath: pathlib.Path) -> list[Point]:
        """Parses the input file.

        Args:
            filepath: The input filepath.

        Returns:
            The points in the input.
        """
        points: list[Point] = []
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                line = line.strip()
                x, y = line.split(",")
                points.append((int(x), int(y)))

        return points

    def _area(self, /, a: Point, b: Point) -> int:
        """Calculates the area for the rectangle.

        The area includes the perimeter grid cells.

        Args:
            a: Coordinates of one corner of the rectangle (x, y).
            b: Coordinates of the opposite corner of the rectangle (x, y).

        Returns:
            The area of the rectangle including its perimeter.
        """
        return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

    def _are_all_lines_outside_the_rectangle(
        self, lines: tuple[list[Line], list[Line]], /, a: Point, b: Point
    ) -> bool:
        """Checks that all given lines are outside the rectangle.

        Args:
            lines: A tuple containing two lists:
                    - The vertical lines represented as (x, y_min, y_max).
                    - The horizontal lines represented as (y, x_min, x_max).
                Both lists MUST be sorted in ascending order by its primary
                axis (x for vertical lines and y for horizontal lines).
            a: Coordinates of one corner of the rectangle (x, y).
            b: Coordinates of the opposite corner of the rectangle (x, y).

        Returns:
            True if all lines lie completely outside or exactly on the perimeter
            of the rectangle. False if any line intersects with the inside of the
            rectangle.
        """
        bounds = [[min(a[axis], b[axis]), max(a[axis], b[axis])] for axis in range(2)]

        for axis in range(2):
            lower_axis_bound, upper_axis_bound = bounds[axis]
            search_start = bisect.bisect(
                lines[axis], lower_axis_bound, key=lambda x: x[0]
            )
            search_end = bisect.bisect_left(
                lines[axis], upper_axis_bound, key=lambda x: x[0]
            )

            lower_bound, upper_bound = bounds[1 - axis]
            for k in range(search_start, search_end):
                _, lower, upper = lines[axis][k]
                if lower_bound < upper and lower < upper_bound:
                    return False

        return True

    @override
    def part_1(self, filepath: pathlib.Path) -> int | str:
        points = self._parse_input(filepath)

        return max(
            self._area(points[i], points[j])
            for i in range(len(points))
            for j in range(i)
        )

    @override
    def part_2(self, filepath: pathlib.Path) -> int | str:
        points = self._parse_input(filepath)

        lines: tuple[list[Line], list[Line]] = [], []
        for i in range(len(points)):
            a = points[i]
            b = points[(i + 1) % len(points)]

            axis = 0 if a[0] == b[0] else 1
            lines[axis].append(
                (a[axis], min(a[1 - axis], b[1 - axis]), max(a[1 - axis], b[1 - axis]))
            )
        for axis in range(2):
            lines[axis].sort()

        areas = sorted(
            (
                (self._area(points[i], points[j]), i, j)
                for i in range(len(points))
                for j in range(i)
            ),
            reverse=True,
        )
        for area, i, j in areas:
            if self._are_all_lines_outside_the_rectangle(lines, points[i], points[j]):
                return area

        return 0
