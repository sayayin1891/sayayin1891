import unittest
from datetime import date
import sys
import os

# Add the parent directory to sys.path to allow importing 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import calculate_shifts # Assuming app.py is in the parent directory

class TestShiftCalculation(unittest.TestCase):

    def test_7x7_pattern_start_of_month(self):
        # Cycle starts on 2024-03-01, 7 days on, 7 days off
        shifts = calculate_shifts("7x7", "2024-03-01", "day", 2024, 3)
        self.assertEqual(len(shifts), 31) # March has 31 days
        # First 7 days should be work days
        for i in range(7):
            self.assertTrue(shifts[i]['is_workday'])
            self.assertEqual(shifts[i]['shift_type'], 'day')
            self.assertEqual(shifts[i]['date'], f"2024-03-{str(i+1).zfill(2)}")
        # Next 7 days should be off days
        for i in range(7, 14):
            self.assertFalse(shifts[i]['is_workday'])
        # Next 7 days should be work days again
        for i in range(14, 21):
            self.assertTrue(shifts[i]['is_workday'])
        # ... and so on

    def test_10x10_pattern_mid_month_start(self):
        # Cycle starts on 2024-04-15, 10 days on, 10 days off
        shifts = calculate_shifts("10x10", "2024-04-15", "night", 2024, 4)
        self.assertEqual(len(shifts), 30) # April has 30 days

        # Day 1 to 14 should be off (or based on cycle before 15th) -> Corrected: Apr 1-4 WORK, Apr 5-14 OFF
        # Day 15 to 24 should be work days -> Correct
        # Day 25 to 30 should be off days (start of 10 off days) -> Correct

        # Expected workdays in April for this cycle: Apr 1-4 and Apr 15-24
        for i in range(30):
            day_num = i + 1
            current_date_str = f"2024-04-{str(day_num).zfill(2)}"
            shift_day = next(s for s in shifts if s['date'] == current_date_str)

            # Cycle: Work Apr 1-4, Off Apr 5-14, Work Apr 15-24, Off Apr 25-30 (and into May)
            if (1 <= day_num <= 4) or (15 <= day_num <= 24):
                self.assertTrue(shift_day['is_workday'], f"Day {day_num} (date: {current_date_str}) should be a work day.")
                self.assertEqual(shift_day['shift_type'], 'night')
            else:
                self.assertFalse(shift_day['is_workday'], f"Day {day_num} (date: {current_date_str}) should be an off day.")

    def test_14x14_pattern_spanning_new_year(self):
        # Cycle starts 2023-12-20 (14 on, 14 off)
        # Test for Jan 2024
        shifts = calculate_shifts("14x14", "2023-12-20", "day", 2024, 1) # January 2024
        self.assertEqual(len(shifts), 31)

        # 2023-12-20 to 2024-01-02 (inclusive) are work days (14 days)
        # 2024-01-03 to 2024-01-16 (inclusive) are off days (14 days)
        # 2024-01-17 to 2024-01-30 (inclusive) are work days (14 days)

        for i in range(31):
            day_num = i + 1
            current_date_str = f"2024-01-{str(day_num).zfill(2)}"
            shift_day = next(s for s in shifts if s['date'] == current_date_str)

            if (1 <= day_num <= 2) or (17 <= day_num <= 30):
                self.assertTrue(shift_day['is_workday'], f"Day {day_num} should be work day")
                self.assertEqual(shift_day['shift_type'], 'day')
            else: # Days 3-16 and 31st
                self.assertFalse(shift_day['is_workday'], f"Day {day_num} should be off day")

    def test_start_date_after_displayed_month(self):
        # Cycle starts 2024-05-10. Displaying April 2024.
        # All days in April should reflect the cycle projected backwards.
        # 7x7 pattern, start 2024-05-10 (work)
        # Cycle: May 10-16 (Work), May 3-9 (Off), Apr 26 - May 2 (Work), Apr 19-25 (Off)
        shifts = calculate_shifts("7x7", "2024-05-10", "day", 2024, 4) # April 2024
        self.assertEqual(len(shifts), 30)

        # Expected workdays in April: 1-2 (from previous cycle), 9-15, 23-29
        # Based on 2024-05-10 being day 0 of work:
        # May 10 is day 0. May 9 is day -1 (cycle day 13). May 2 is day -8 (cycle day 6)
        # Apr 30 is day -10 (cycle day 4 - work)
        # Apr 29 is day -11 (cycle day 3 - work)
        # Apr 26 is day -14 (cycle day 0 - work)
        # Apr 25 is day -15 (cycle day 13 - off)
        # Apr 19 is day -21 (cycle day 7 - off)
        # Apr 18 is day -22 (cycle day 6 - work)


        # Let's manually check a few dates based on backward projection
        # Date: 2024-04-30. Delta from 2024-05-10 is -10 days.
        # Position in 14-day cycle: -10 % 14 = 4. Day 4 is a workday.
        self.assertTrue(shifts[29]['is_workday']) # April 30th
        self.assertEqual(shifts[29]['date'], "2024-04-30")

        # Date: 2024-04-25. Delta from 2024-05-10 is -15 days.
        # Position in 14-day cycle: -15 % 14 = 13. Day 13 is an off-day.
        self.assertFalse(shifts[24]['is_workday']) # April 25th
        self.assertEqual(shifts[24]['date'], "2024-04-25")

    def test_invalid_pattern_format(self):
        with self.assertRaisesRegex(ValueError, "Invalid pattern format. Expected 'NxN', e.g., '7x7'."):
            calculate_shifts("7-7", "2024-03-01", "day", 2024, 3)

    def test_invalid_date_format(self):
        with self.assertRaisesRegex(ValueError, "Invalid start_date format. Expected 'YYYY-MM-DD'."):
            calculate_shifts("7x7", "01/03/2024", "day", 2024, 3)

if __name__ == '__main__':
    unittest.main()
