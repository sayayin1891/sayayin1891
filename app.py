from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date

app = Flask(__name__)

def calculate_shifts(pattern: str, start_date_str: str, shift_type: str, year: int, month: int):
    '''
    Calculates the shift days for a given month based on a pattern and start date.

    Args:
        pattern (str): e.g., "7x7", "10x10", "14x14".
        start_date_str (str): The start date of the first work period in "YYYY-MM-DD" format.
        shift_type (str): "day" or "night".
        year (int): The year of the month to display.
        month (int): The month to display (1-12).

    Returns:
        list: A list of dictionaries, where each dictionary represents a day
              and has keys: 'date' (YYYY-MM-DD), 'is_workday' (bool),
              'shift_type' (str, if workday).
    '''
    try:
        days_on, days_off = map(int, pattern.split('x'))
    except ValueError:
        # Return a user-friendly error for the API
        raise ValueError("Invalid pattern format. Expected 'NxN', e.g., '7x7'.")

    cycle_length = days_on + days_off

    try:
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid start_date format. Expected 'YYYY-MM-DD'.")

    # Determine the first day of the month for calculation
    first_day_of_month = date(year, month, 1)
    # Determine the number of days in the month
    if month == 12:
        # For December, the first day of the next month is Jan 1 of the next year
        last_day_of_month = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        # For other months, it's the first day of the next month in the same year
        last_day_of_month = date(year, month + 1, 1) - timedelta(days=1)

    num_days_in_month = last_day_of_month.day

    shifts_for_month = []

    for day_num in range(1, num_days_in_month + 1):
        current_date = date(year, month, day_num)

        delta_days = (current_date - start_date_obj).days
        position_in_cycle = delta_days % cycle_length

        is_workday = False
        # Work period is from day 0 to days_on-1 in the cycle
        if position_in_cycle >= 0 and position_in_cycle < days_on:
            is_workday = True

        day_info = {
            "date": current_date.strftime("%Y-%m-%d"),
            "is_workday": is_workday,
        }
        if is_workday:
            day_info["shift_type"] = shift_type

        shifts_for_month.append(day_info)

    return shifts_for_month

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shifts', methods=['GET'])
def get_shifts():
    """
    API endpoint to get shift data.
    Expects 'pattern', 'start_date', 'shift_type', 'year', and 'month' as query parameters.
    Returns a JSON list of shift information for the specified month or an error message.
    """
    try:
        pattern = request.args.get('pattern', type=str)
        start_date_str = request.args.get('start_date', type=str)
        shift_type = request.args.get('shift_type', type=str)
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        if not all([pattern, start_date_str, shift_type, year, month]):
            return jsonify({"error": "Missing one or more required parameters: pattern, start_date, shift_type, year, month"}), 400

        # Validate shift_type
        if shift_type.lower() not in ['day', 'night']:
            return jsonify({"error": "Invalid shift_type. Expected 'day' or 'night'."}), 400

        shifts_data = calculate_shifts(pattern, start_date_str, shift_type, year, month)
        return jsonify(shifts_data)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Log the exception e for debugging
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


if __name__ == '__main__':
    app.run(debug=True)
