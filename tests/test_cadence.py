import unittest
from datetime import date, timedelta

from cadence import should_run


class CadenceTests(unittest.TestCase):
    def test_first_two_cycles(self):
        for day, expected in [
            (date(2026, 9, 14), False),
            (date(2026, 9, 21), True),
            (date(2026, 9, 22), True),
            (date(2026, 9, 28), False),
            (date(2026, 9, 29), False),
            (date(2026, 10, 5), True),
            (date(2026, 10, 6), True),
        ]:
            with self.subTest(day=day):
                self.assertEqual(should_run(day, "schedule"), expected)

    def test_writer_and_reviewer_remain_aligned_for_two_years(self):
        monday = date(2026, 9, 21)
        active_dates = []
        for _ in range(104):
            active = should_run(monday, "schedule")
            self.assertEqual(active, should_run(monday + timedelta(days=1), "schedule"))
            if active:
                active_dates.append(monday)
            monday += timedelta(days=7)
        self.assertEqual(len(active_dates), 52)
        for previous, following in zip(active_dates, active_dates[1:]):
            self.assertEqual(following - previous, timedelta(days=14))

    def test_manual_runs_bypass_the_schedule(self):
        for day in [date(2026, 9, 16), date(2026, 9, 21), date(2026, 9, 28)]:
            with self.subTest(day=day):
                self.assertTrue(should_run(day, "workflow_dispatch"))


if __name__ == "__main__":
    unittest.main()
