# Work Shift Calendar Application

This is a simple web application to display work shift schedules based on user-defined patterns (e.g., 7x7, 10x10, 14x14), a cycle start date, and shift type (day/night).

## Features

*   Selectable shift patterns: 7x7, 10x10, 14x14.
*   User-defined start date for the work cycle.
*   Selection of day or night shift.
*   Interactive calendar display showing workdays, off-days, and shift types.
*   Month navigation.

## Technology Stack

*   **Backend:** Python (Flask)
*   **Frontend:** HTML, CSS, JavaScript
*   **API:** JSON-based for communication between frontend and backend.

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   `pip` (Python package installer) installed.

2.  **Clone the repository (if applicable) or download the files.**

3.  **Navigate to the project directory:**
    ```bash
    cd path/to/your/project-directory
    ```

4.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   Windows: `venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

5.  **Install dependencies:**
    The only external dependency is Flask.
    ```bash
    pip install Flask
    ```

6.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` in your web browser.

## How to Use

1.  Open the application in your web browser.
2.  Select your desired **Shift Pattern** (e.g., 7x7).
3.  Choose your **Cycle Start Date** using the date picker. This is the first day of your work period.
4.  Select whether your shifts are **Day** or **Night**.
5.  The calendar will display your work schedule for the current month.
6.  Use the "Previous Month" and "Next Month" buttons to navigate.

## Project Structure

*   `app.py`: Main Flask application file, contains backend logic and API endpoints.
*   `static/`: Contains static assets.
    *   `css/style.css`: Stylesheets for the application.
    *   `js/script.js`: JavaScript for frontend interactivity and calendar generation.
*   `templates/index.html`: HTML template for the main calendar page.
*   `tests/`: Contains unit tests for the backend logic.
    *   `test_app.py`: Unit tests for `app.py`.
*   `README.md`: This file.
