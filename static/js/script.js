document.addEventListener('DOMContentLoaded', function() {
    const patternSelect = document.getElementById('shift-pattern');
    const startDateInput = document.getElementById('start-date');
    const shiftTypeRadios = document.querySelectorAll('input[name="shift-type"]');
    const calendarGrid = document.getElementById('calendar-grid');
    const currentMonthYearDisplay = document.getElementById('current-month-year');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const errorMessageDiv = document.getElementById('error-message');

    let currentDisplayedDate = new Date();

    // Set default start date to today
    const today = new Date();
    startDateInput.value = today.toISOString().split('T')[0];

    /**
     * Gets the currently selected shift type from the radio buttons.
     * @returns {string} The selected shift type ('day' or 'night').
     */
    function getSelectedShiftType() {
        for (const radio of shiftTypeRadios) {
            if (radio.checked) {
                return radio.value;
            }
        }
        return 'day'; // Default
    }

    /**
     * Fetches shift data from the API based on current form inputs
     * and then calls renderCalendar to display it.
     * Handles errors and updates the error message display.
     */
    async function fetchAndDisplayShifts() {
        const pattern = patternSelect.value;
        const startDate = startDateInput.value;
        const shiftType = getSelectedShiftType();
        const year = currentDisplayedDate.getFullYear();
        const month = currentDisplayedDate.getMonth() + 1; // Month is 1-indexed for API

        errorMessageDiv.textContent = ''; // Clear previous errors

        if (!startDate) {
            errorMessageDiv.textContent = 'Please select a cycle start date.';
            calendarGrid.innerHTML = ''; // Clear calendar
            currentMonthYearDisplay.textContent = '';
            return;
        }

        try {
            const response = await fetch(`/api/shifts?pattern=${pattern}&start_date=${startDate}&shift_type=${shiftType}&year=${year}&month=${month}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            const shifts = await response.json();
            renderCalendar(year, month, shifts);
        } catch (error) {
            console.error('Error fetching shifts:', error);
            errorMessageDiv.textContent = `Error loading shifts: ${error.message}`;
            calendarGrid.innerHTML = ''; // Clear calendar on error
            currentMonthYearDisplay.textContent = `Displaying: ${currentDisplayedDate.toLocaleString('default', { month: 'long' })} ${year}`;
        }
    }

    /**
     * Renders the calendar grid for the given year and month with the provided shift data.
     * @param {number} year - The full year (e.g., 2024).
     * @param {number} month - The month (1-12).
     * @param {Array} shifts - An array of shift objects from the API.
     */
    function renderCalendar(year, month, shifts) {
        calendarGrid.innerHTML = ''; // Clear previous calendar
        currentMonthYearDisplay.textContent = `${currentDisplayedDate.toLocaleString('default', { month: 'long' })} ${year}`;

        const firstDayOfMonth = new Date(year, month - 1, 1);
        const daysInMonth = new Date(year, month, 0).getDate(); // Month is 0-indexed for Date object
        const startingDayOfWeek = firstDayOfMonth.getDay(); // 0 for Sunday, 1 for Monday, etc.

        // Create header for days of the week
        const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        daysOfWeek.forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.classList.add('calendar-header');
            dayHeader.textContent = day;
            calendarGrid.appendChild(dayHeader);
        });

        // Create empty cells for days before the first of the month
        for (let i = 0; i < startingDayOfWeek; i++) {
            const emptyCell = document.createElement('div');
            calendarGrid.appendChild(emptyCell);
        }

        // Create cells for each day of the month
        for (let dayNum = 1; dayNum <= daysInMonth; dayNum++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('calendar-day');
            dayCell.textContent = dayNum;

            const currentDateStr = `${year}-${String(month).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
            const shiftInfo = shifts.find(s => s.date === currentDateStr);

            if (shiftInfo) {
                if (shiftInfo.is_workday) {
                    dayCell.classList.add('work-day');
                    if (shiftInfo.shift_type === 'night') {
                        dayCell.classList.add('night-shift');
                    } else {
                        dayCell.classList.add('day-shift');
                    }
                    dayCell.title = `Work (${shiftInfo.shift_type})`;
                } else {
                    dayCell.classList.add('off-day');
                    dayCell.title = 'Off Day';
                }
            }
            calendarGrid.appendChild(dayCell);
        }
    }

    prevMonthButton.addEventListener('click', () => {
        currentDisplayedDate.setMonth(currentDisplayedDate.getMonth() - 1);
        fetchAndDisplayShifts();
    });

    nextMonthButton.addEventListener('click', () => {
        currentDisplayedDate.setMonth(currentDisplayedDate.getMonth() + 1);
        fetchAndDisplayShifts();
    });

    patternSelect.addEventListener('change', fetchAndDisplayShifts);
    startDateInput.addEventListener('change', fetchAndDisplayShifts);
    shiftTypeRadios.forEach(radio => radio.addEventListener('change', fetchAndDisplayShifts));

    // Initial load
    fetchAndDisplayShifts();
});
