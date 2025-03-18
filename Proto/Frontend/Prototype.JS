const calendar = document.getElementById("calendar");
const calendarHeader = document.getElementById("calendar-header");
const monthYear = document.getElementById("monthYear");
const yearSelect = document.getElementById("yearSelect");
let currentDate = new Date();

function renderCalendar() {
    calendar.innerHTML = "";
    calendarHeader.innerHTML = "";
    let year = currentDate.getFullYear();
    let month = currentDate.getMonth();
    monthYear.innerText = new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric" }).format(currentDate);
    
    const weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
    weekdays.forEach(day => {
        let dayHeader = document.createElement("div");
        dayHeader.classList.add("weekday");
        dayHeader.innerText = day;
        calendarHeader.appendChild(dayHeader);
    });

    let firstDay = new Date(year, month, 1).getDay();
    let daysInMonth = new Date(year, month + 1, 0).getDate();
    
    for (let i = 0; i < firstDay; i++) {
        let emptyCell = document.createElement("div");
        calendar.appendChild(emptyCell);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        let dayCell = document.createElement("div");
        dayCell.classList.add("day");
        dayCell.innerText = day;
        dayCell.onclick = () => alert("Selecionado: " + day + "/" + (month + 1) + "/" + year);
        calendar.appendChild(dayCell);
    }
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
}

function populateYears() {
    let currentYear = new Date().getFullYear();
    for (let i = currentYear - 10; i <= currentYear + 10; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        if (i === currentYear) option.selected = true;
        yearSelect.appendChild(option);
    }
}

function changeYear() {
    currentDate.setFullYear(yearSelect.value);
    renderCalendar();
}

populateYears();
renderCalendar();
