let table = [];
let promoCode = localStorage.getItem('promo');

const oneHour = 1000 * 60 * 60;
let now = new Date().getTime();
let endTime = localStorage.getItem('endTime');

const promoCodes = {
    'SAVE10': 0.9,
    'HELLOWORLD': 0.95,
    'MEGAJOPA': 0.6
};

// preloader
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    preloader.style.display = 'none';

    const content = document.getElementById('main-content');
    content.style.display = 'block';
});

window.addEventListener('scroll',() => {
    const money_left = document.getElementById('money_left');
    const money_right = document.getElementById('money_right');
    const text = document.getElementById('text');
    let value = scrollY;
    money_left.style.left = `-${value/0.7}px`
    money_right.style.left = `${value/0.7}px`
    text.style.bottom = `-${value}px`;
})

function checkAge() {
    document.getElementById('age-checker').style.display = 'none';
    const ageConfirmed = localStorage.getItem('ageConfirmed');
    if (ageConfirmed === 'true') {
        showMainContent();
    } else {
        document.getElementById('age-checker').style.display = 'flex';
        document.getElementById('main-content').style.display = 'none';
    }
}

function validateAge() {
    const month = parseInt(document.getElementById('birthMonth').value);
    const day = parseInt(document.getElementById('birthDay').value);
    const year = parseInt(document.getElementById('birthYear').value);

    const birthDate = new Date(year, month, day);
    const today = new Date();

    let age = parseInt(today.getFullYear() - birthDate.getFullYear());
    const monthDiff = parseInt(today.getMonth() - birthDate.getMonth());

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    console.log(age, birthDate, month, day, year);
    if (isNaN(birthDate) || age < 0) {
        document.getElementById('underBox').classList.remove('hidden');
        return;
    }

    const daysOfWeek = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    const dayOfWeek = daysOfWeek[birthDate.getDay()];

    if (age >= 18) {
        localStorage.setItem('ageConfirmed', 'true');
        alert('Вы родились в день недели: ${dayOfWeek}');
        showMainContent();
    } else {
        alert('Извините, вам должно быть 18 лет или старше для просмотра этого сайта. Вам ${age} лет.');
    }
}

function showMainContent() {
    document.getElementById('main-content').style.display = 'block';
    document.getElementById('age-checker').style.display = 'none';
}

function moveToNext(current, nextFieldId) {
    if (current.id === 'number') {
        let formattedValue = current.value.replace(/\D/g, '');
        if (formattedValue.length > 0) {
            formattedValue = formattedValue.match(/.{1,4}/g).join('-');
        }
        current.value = formattedValue;
        if (formattedValue.replace(/[^0-9]/g, '').length === 16) {
            document.getElementById(nextFieldId).focus();
        }
    } else if (current.id === 'date') {
        let formattedValue = current.value.replace(/\D/g, '');
        if (formattedValue.length > 2) {
            formattedValue = formattedValue.slice(0, 2) + '/' + formattedValue.slice(2);
        }
        current.value = formattedValue;

        if (formattedValue.replace(/[^0-9]/g, '').length === 4) {
            document.getElementById(nextFieldId).focus();
        }
    } else {
        if (current.value.length === current.maxLength) {
            document.getElementById(nextFieldId).focus();
        }
    }
}

function moveToPrev(current, prevFieldId) {
    if (current.value.length === 0 && event.key === 'Backspace') {
        document.getElementById(prevFieldId).focus();
    }
}

function updateStyles() {
    if (applySettingsCheckbox.checked) {
        document.body.style.fontSize = fontSizeSelector.value;
        document.body.style.color = textColorInput.value;
        document.body.style.backgroundColor = bgColorInput.value;
    }
}

//for promocodes
function applyPromocode() {
    const totalElement = document.getElementById('total');
    const promoCodeInput = document.getElementById('promo_code');
    const checkoutTotal = document.getElementById('checkout-total');

    if (!promoCode) {
        promoCode = promoCodeInput.value;
        localStorage.setItem('promo', promoCode);
    }
    let total = parseFloat(totalElement.innerText);
    console.log(localStorage.getItem('promo'));

    if (promoCodes[promoCode]) {
        total *= promoCodes[promoCode];
        totalElement.innerText = total.toFixed(2);
        checkoutTotal.innerText += ` (Применен купон ${promoCode})`;

    } else {
        alert('Invalid promocode');
    }
}

function cancelPromocode() {
    const totalElement = document.getElementById('total'); //doesnt work, is null
    let total = parseFloat(totalElement.innerText);

    const promoCode = localStorage.getItem('promo');

    if (promoCode && promoCodes[promoCode]) {
        const discount = promoCodes[promoCode];
        total = total / (1 - discount);
        totalElement.innerText = total.toFixed(2);
    }
    localStorage.removeItem('promo');
}

function formatTime(time) {
    const hours = Math.floor(time / (1000 * 60 * 60));
    const minutes = Math.floor(time % (1000 * 60 * 60) / (1000 * 60));
    const seconds = Math.floor((time % (1000 * 60)) / 1000);
    return `${hours < 10 ? '0' : ''}${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

function updateCountdown() {
    now = new Date().getTime();
    const timeLeft = endTime - now;

    countdownElement = document.getElementById('counter');
    if (timeLeft > 0) {
        countdownElement.textContent = formatTime(timeLeft);
        console.log(countdownElement.textContext);
    } else {
        countdownElement.textContent = `Ka-boom`;
        localStorage.removeItem('endTime');
        clearInterval(interval);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const countdownElement = document.getElementById('counter');

    const slider = new Slider('#slider', '#banner_form');
    slider.startBannerRotation();

    if (!endTime) {
       endTime = now + oneHour;
       localStorage.setItem('endTime', endTime);
    }
    const interval = setInterval(updateCountdown, 1000);

    fontSizeSelector = document.getElementById('fontSize');
    textColorInput = document.getElementById('textColor');
    bgColorInput = document.getElementById('bgColor');
    applySettingsCheckbox = document.getElementById('applySettings');

    promoCode = localStorage.getItem('promo');
    applyPromocode();

    fontSizeSelector.addEventListener('change', () => updateStyles());
    textColorInput.addEventListener('input', () => updateStyles());
    bgColorInput.addEventListener('input', () => updateStyles());
    applySettingsCheckbox.addEventListener('change', () => updateStyles());

    updateStyles();
});

class Slider {
    #currentIndex;
    #totalSlides;
    #banners = [];
    #intervalTime;
    #intervalId;
    #loop;
    #showNavs;
    #showPags;
    #auto;
    #stopOnHover;

    constructor(sliderSelector, formSelector) {
        this.slider = document.querySelector(sliderSelector);
        this.#banners = document.querySelectorAll(`${sliderSelector} .banner`);

        console.log(this.#banners);
        this.#totalSlides = this.#banners.length;
        this.#currentIndex = 0;
        this.#intervalTime = 5000;
        this.#intervalId = null;

        const form = document.querySelector(formSelector);

        if (form) {
            this.loadSettings(form);

            form.addEventListener('submit', e => {
                e.preventDefault();
                this.updateSettings(form);
                alert('Banner settings updated');
            });

            form.auto.addEventListener('change', () => {
                form.interval.disabled = form.auto.checked;
            });
        }

        if (this.#showNavs) this.addNavigationButtons();
        if (this.#showPags) this.addPagination();
        if (this.#auto) this.startBannerRotation();
        if (this.#stopOnHover && this.#auto) {
            this.#banners.forEach(banner => {
                banner.addEventListener('mouseenter', () => this.stopBannerRotation());
                banner.addEventListener('mouseleave', () => this.startBannerRotation());
            });
        }

        this.updateCaptionAndSlideNumber();
    }

    loadSettings(form) {
        const settings = JSON.parse(localStorage.getItem('bannerSettings')) || {};

        this.#loop = settings.loop !== undefined ? settings.loop : true;
        this.#showNavs = settings.showNavs !== undefined ? settings.showNavs : true;
        this.#showPags = settings.showPags !== undefined ? settings.showPags : true;
        this.#auto = settings.auto !== undefined ? settings.auto : true;
        this.#stopOnHover = settings.stopOnHover !== undefined ? settings.stopOnHover : false;
        this.#intervalTime = settings.intervalTime !== undefined ? settings.intervalTime : 3000;

        if (form) {
            form.loop.checked = this.#loop;
            form.navs.checked = this.#showNavs;
            form.pags.checked = this.#showPags;
            form.auto.checked = this.#auto;
            form.stopMouseHover.checked = this.#stopOnHover;
            form.interval.value = this.#intervalTime;
        }

        this.updateSettings(form);
    }

    updateSettings(form) {
        this.#loop = form.loop.checked;
        this.#showNavs = form.navs.checked;
        this.#showPags = form.pags.checked;
        this.#auto = form.auto.checked;
        this.#stopOnHover = form.stopMouseHover.checked;
        this.#intervalTime = form.interval.value ? parseInt(form.interval.value, 10) : 5000;

        localStorage.setItem('bannerSettings', JSON.stringify({
            loop: this.#loop,
            showNavs: this.#showNavs,
            showPags: this.#showPags,
            auto: this.#auto,
            stopOnHover: this.#stopOnHover,
            intervalTime: this.#intervalTime
        }));

        if (this.#showNavs) this.addNavigationButtons();
        else this.removeNavigationButtons();

        if (this.#showPags) this.addPagination()
        else this.removePagination();

        if (this.#auto) this.startBannerRotation();
        else this.stopBannerRotation();

        if (this.#stopOnHover && this.#auto) {
            this.#banners.forEach(banner => {
                banner.addEventListener('mouseenter', () => this.stopBannerRotation());
                banner.addEventListener('mouseleave', () => this.startBannerRotation());
            });
        }
    }

    addNavigationButtons() {
        const prevButton = document.createElement('button');
        const nextButton = document.createElement('button');

        prevButton.classList.add('prev-btn');
        nextButton.classList.add('next-btn');

        prevButton.innerText = '←';
        nextButton.innerText = '→';

        prevButton.addEventListener('click', () => this.showPrevBanner());
        nextButton.addEventListener('click', () => this.showNextBanner());

        this.slider.appendChild(prevButton);
        this.slider.appendChild(nextButton);
    }

    removeNavigationButtons() {
        const prevButton = this.slider.querySelector('.prev-btn');
        const nextButton = this.slider.querySelector('.next-btn');

        if (prevButton) prevButton.remove();
        if (nextButton) nextButton.remove();
    }

    addPagination() {
        const pagination = document.createElement('div');
        pagination.classList.add('pagination');

        for (let i = 0; i < this.#totalSlides; i++) {
            const pagButton = document.createElement('button');
            pagButton.classList.add('pag-btn');
            pagButton.dataset.index = i;
            pagButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.goToBanner(i);
            });
            pagination.appendChild(pagButton);
        }

        this.slider.appendChild(pagination);
        this.updatePagination();
    }

    updatePagination() {
        const paginationButtons = this.slider.querySelectorAll('.pag-btn');
        paginationButtons.forEach(btn => btn.classList.remove('active'));
        paginationButtons[this.#currentIndex].classList.add('active');
    }

    removePagination() {
        const pagination = this.slider.querySelector('.pagination');
        if (pagination) pagination.remove();
    }

    showNextBanner() {
        if (!this.#loop && this.#currentIndex + 1 === this.#banners.length) return;

        this.#banners[this.#currentIndex].classList.remove('active');
        this.#currentIndex = (this.#currentIndex + 1) % this.#banners.length;
        this.#banners[this.#currentIndex].classList.add('active');

        this.updatePagination();
        this.updateCaptionAndSlideNumber();
    }

    showPrevBanner() {
        if (!this.#loop && this.#currentIndex === 0) return;

        this.#banners[this.#currentIndex].classList.remove('active');
        this.#currentIndex = (this.#currentIndex - 1 + this.#banners.length) % this.#banners.length;
        this.#banners[this.#currentIndex].classList.add('active');

        this.updatePagination();
        this.updateCaptionAndSlideNumber();
    }

    goToBanner(index) {
        this.#banners[this.#currentIndex].classList.remove('active');
        this.#currentIndex = index;
        this.#banners[this.#currentIndex].classList.add('active');

        this.updatePagination();
        this.updateCaptionAndSlideNumber();
    }

    startBannerRotation() {
        clearInterval(this.#intervalId);
        this.#intervalId = setInterval(() => this.showNextBanner(), this.#intervalTime);
    }

    stopBannerRotation() {
        if (this.#intervalId) {
            clearInterval(this.#intervalId);
            this.#intervalId = null;
        }
    }

    get interval() {
        return this.#intervalTime;
    }

    set interval(value) {
        if (typeof value === 'number' && value >= 0) {
            this.#intervalTime = value;
        } else {
            console.error('Invalid value. Must be a non-negative number.');
        }
    }

    get totalSlides() {
        return this.#totalSlides;
    }

    updateCaptionAndSlideNumber() {
        const caption = this.slider.querySelector('.caption');
        const slideNumber = this.slider.querySelector('.slide-number');

        if (slideNumber && caption) {
            slideNumber.innerText = `${this.#currentIndex + 1}/${this.#totalSlides}`;
            const currentCaption = this.#banners[this.#currentIndex].querySelector('.caption');
            caption.innerText = currentCaption ? currentCaption.innerText : '';
        }
    }
}

class Person {
    constructor(surname, name, second_name, gender, age) {
        this.surname = surname;
        this.name = name;
        this.second_name = second_name;
        this.gender = gender;
        this.age = age;
    }

    getFullName() {
        return `${this.surname} ${this.name} ${this.second_name}`;
    }
}

class Student extends Person {
    constructor(surname, name, second_name, gender, age, course) {
        super(surname, name, second_name, gender, age);
        this.course = course;
    }

    getStudentInfo() {
        return `${super.getFullName()} ${course}`;
    }
}

//alternate
/*
function Person(surname, name, second_name, gender, age) {
    this.surname = surname;
    this.name = name;
    this.second_name = second_name;
    this.gender = gender;
    this.age = age;
}

Person.prototype.getFullName = function() {
    return `${this.surname} ${this.name} ${this.patronymic}`;
};


//extends
function Student(surname, name, second_name, gender, age, course) {
    Person.call(this, surname, name, second_name, gender, age);
    this.course = course;
}

Student.prototype = Object.Create(Person.prototype);
Student.prototype.constructor = Student;
*/

class StudentsTask {
    students;
    studentsCount;

    constructor() {
        this.studentsCount = 0;
        this.students = localStorage.getItem('students') || [];

        document.getElementById('studentsForm').addEventListener('submit', (e) => {
            console.log('mama');
            this.addStudent();
        });

        document.getElementById('calculate').addEventListener('click', (e) => {
            e.preventDefault();
            this.calculateMaxMalePercentage();
        });
    }

    addStudent() {
        const surname = document.getElementById('surname').value;
        const name = document.getElementById('name').value;
        const second_name = document.getElementById('second_name').value;
        const sex = document.getElementById('sex').value;
        const age = document.getElementById('age').value;
        const course = document.getElementById('course').value;

        const student = new Student(surname, name, patronymic, gender, parseInt(age), parseInt(course));
        this.students.push(student);

        localStorage.setItem('students', this.students);

        this.displayStudents();
        this.calculateMaxMalePercentage();
    }

    displayStudents() {
        const studentsList = document.getElementById('students');
        console.log(this.students);
        this.students.forEach((student, index) => {
            const studentDiv = document.createElement('div');
            studentDiv.classList.add('student');
            studentsDiv.innerHTML += `<p>${index + 1}. ${student.getFullName()}, Пол: ${student.gender}, Возраст: ${student.age}, Курс: ${student.course}</p>`;
            studentsList.appendChild(studentDiv);
        });
    }

    calculateMaxMalePercentage() {
        const courses = {};
        let maxCourse = null;
        let maxPercentage = 0;

        this.students.forEach(student => {
            if (!courses[student.course]) {
                courses[student.course] = { males: 0, females: 0 };
            }
            if (student.gender === 'М') {
                courses[student.course].males++;
            } else {
                courses[student.course].females++;
            }
        });

        for (let course in courses) {
            const total = courses[course].males + courses[course].females;
            const malePercentage = (courses[course].males / total) * 100;
            if (malePercentage > maxPercentage) {
                maxPercentage = malePercentage;
                maxCourse = course;
            }
        }

        const result = document.getElementById('top-course');
        if (maxCourse !== null) {
            result.innerHTML = `На курсе ${maxCourse} самый высокий процент мужчин: ${maxPercentage.toFixed(2)}%`;
        } else {
            result.innerHTML = 'Нет данных для расчета.';
        }
    }
}

// generating random table with given sizes
function generateTable() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const min = parseInt(document.getElementById('min').value);
    const max = parseInt(document.getElementById('max').value);

    for (let i = 0; i < rows; ++i) {
        table[i] = [];
        for (let j = 0; j < cols; ++j) {
            table[i][j] = getRandomInt(min, max);
        }
    }

    printTable(table);
    console.log(table);
}

function transposeTable() {
    if (!table.length) {
        generateTable(getRandomInt(1, 100), getRandomInt(1, 100), getRandomInt(1, 100), getRandomInt(1, 100));
    }

    let transposed = []; // m * n;
    for (let i = 0; i < table[0].length; ++i) {
        transposed[i] = [];
        for (let j = 0 ; j < table.length; ++j) {
            transposed[i][j] = table[j][i];
        }
    }
    table = transposed
    printTable(transposed);
}

function printTable(table) {
    const tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = ``;
    let htmlTable = document.createElement('table');
    htmlTable.id = `table`;
    for (let i = 0; i < table.length; ++i) {
        const row = document.createElement('tr');
        for (let j = 0; j < table[i].length; ++j) {
            const cell = document.createElement('td');
            cell.textContent = table[i][j];
            cell.addEventListener('click', () => markCell(cell, i, j));
            row.appendChild(cell);
        }
        htmlTable.appendChild(row);
    }
    tableContainer.appendChild(htmlTable);
}

let totalSelectedCount = 0;

function markCell(td, row, col) {
    const maxSelections = parseInt(document.getElementById('num').value);
    const rowCells = document.querySelectorAll(`#table tr:nth-child(${row + 1}) td`);

    if (totalSelectedCount >= maxSelections && !td.classList.contains('selected')) {
        alert(`Максимальное количество выделенных ячеек в строке: ${maxSelections}`);
        return;
    }

    if (isNeighboursSelected(rowCells, col)) {
        alert('Нельзя выделить ячейку, так как соседние уже выделены.');
        return;
    }

    if (td.classList.contains('selected')) {
        td.classList.remove('selected');
        totalSelectedCount--;
        td.classList.toggle(td.textContent % 2 === 0 ? 'even' : 'odd', false);
    } else {
        td.classList.add('selected');
        totalSelectedCount++;
        td.classList.toggle(td.textContent % 2 === 0 ? 'even' : 'odd', true);
    }
}

function isNeighboursSelected(rowCells, col) {
    const canMarkNeighbours = document.getElementById('can').checked;
    console.log(canMarkNeighbours);
    if (canMarkNeighbours) return false;
    if (col > 0 && rowCells[col - 1].classList.contains('selected')) return true;
    if (col < rowCells.length - 1 && rowCells[col + 1].classList.contains('selected')) return true;
    return false;
}

function addNewColumn() {
    let newColumn = [];
    let cols = table[0].length;

    for (let i = 0; i < cols; i++) {
       newColumn.push(getRandomInt(1, 100));
    }

    table.push(newColumn);
    printTable(table);
}

function addNewRow() {
    for (let i = 0; i < table.length; i++) {
        table[i].push(getRandomInt(1, 100));
    }
    printTable(table);
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

//geolocation api
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('getLocation').addEventListener('click', () => {
        if (navigator.geolocation) {
            trackPosition();
        } else {
            document.getElementById('locationInfo').textContent = "Геолокация не поддерживается в вашем браузере.";
        }
    });

    document.getElementById('copyToClipboard').addEventListener('click', () => {
        copyToClipBoard();
    });

    document.getElementById('pasteFromClipboard').addEventListener('click', () => {
        pasteFromClipboard();
    });
})

//map with openmapapi
let map, marker, accuracyCircle;

function initMap(lat, lon) {
    map = L.map('map').setView([lat, lon], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    marker = L.marker([lat, lon]).addTo(map);
    accuracyCircle = L.circle([lat, lon], { radius: 0 }).addTo(map);
}

function updatePosition(lat, lon, ) {
    marker.setLatLng([lat, lon]);
    map.setView([lat, lon], 13);

    accuracyCircle.setLatLng([lat, lon]);
}

function trackPosition() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition((position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById('locationInfo').textContent = `Широта: ${lat}, долгота: ${lon}`;

            if (!map) initMap(lat, lon);
            else updatePosition(lat, lon);
        }, (error) => {
            document.getElementById('locationInfo').textContent = "невозможно получить координаты.";
        }, {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 10000
        });
    } else document.getElementById('status').textContent = "геолокация не поддерживается в вашем браузере.";
}

// clipboardApi
function copyToClipBoard() {
    const textToCopy = document.querySelector('#editor').value;
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Скопировано в буфер обмена');
    }).catch(err => {
         console.error('Ошибка копирования текста: ', err);
    });
}

function pasteFromClipboard() {
    navigator.clipboard.readText().then((clipText) => {
        document.querySelector('#second-editor').value += clipText;
    }).catch(err => {
        console.error('Ошибка вставки текста: ', err);
    });
}

class Pagination {
    constructor(paginationId, itemsPerPage, listSelector){
        this.pagination = document.getElementById(paginationId);
        this.itemsPerPage = itemsPerPage;
        this.items = document.querySelectorAll(listSelector);
        this.totalItems = this.items.length;
        this.currentPage = 1;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);

        this.changePage(this.currentPage)
    }

    renderPagination() {
        this.pagination.innerHTML = '';

        const prevButton = document.createElement('button');
        prevButton.classList.add('pagination-btn');
        prevButton.innerText = '←';
        if (this.currentPage === 1) prevButton.disabled = true;
        prevButton.addEventListener('click', () => this.changePage(this.currentPage - 1));
        this.pagination.appendChild(prevButton);

        for (let i = 1; i <= this.totalPages; i++) {
            const pageBtn = document.createElement('button');

            pageBtn.innerText = i;
            pageBtn.classList.add('pagination-btn');
            if (this.currentPage === i) pageBtn.classList.add('active');
            pageBtn.addEventListener('click', () => this.changePage(i));

            this.pagination.appendChild(pageBtn);
        }

        const nextButton = document.createElement('button');
        nextButton.classList.add('pagination-btn');
        nextButton.innerText = '→';
        if (this.currentPage === this.totalPages) nextButton.disabled = true;
        nextButton.addEventListener('click', () => this.changePage(this.currentPage + 1));
        this.pagination.appendChild(nextButton);
    }

    changePage(page) {
        if (page < 1) this.currentPage = 1;
        else if (page > this.totalPages) this.currentPage = totalPages;
        else this.currentPage = page;

        this.items.forEach((item, index) => {
            item.style.display = 'none';
        });

        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        this.items.forEach((item, index) => {
            if (index >= start && index < end) {
                item.style.display = 'block';
            }
        });

        this.renderPagination();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const pagination = new Pagination('pagination', 3, '.employee-card');
});

function displayDetails() {
    const table = document.getElementById('employeeTable');
    const details = document.getElementById('employeeDetails');

    table.addEventListener('click', (e) => {
        let row = e.target.closest('tr');
        if (row) {
            const name = row.cells[1].innerText;
            const job_position = row.cells[2].innerText;
            const age = row.cells[3].innerText;
            const phone = row.cells[4].innerText;
            const email = row.cells[5].innerText;

            document.getElementById('detailsName').innerText = name;
            document.getElementById('detailsPosition').innerText = job_position;
            document.getElementById('detailsAge').innerText = age;
            document.getElementById('detailsPhone').innerText = phone;
            document.getElementById('detailsEmail').innerText = email;

            details.style.display = 'block';
        }
    });
}

let currentSortDirection = {};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('clicked');
            const column = parseInt(this.dataset.column, 10);
            const sortDirection = currentSortDirection[column] === 'asc' ? 'desc' : 'asc';

            sortColumn(column, sortDirection);
            currentSortDirection[column] = sortDirection;

            updateSortSymbol(btn, sortDirection);
        });
    });

    displayDetails();
});

function sortColumn(column, sortDirection) {
    const tableRows = Array.from(document.querySelectorAll('#employeeTable tbody tr'));
    const sortedRows = tableRows.sort((a, b) => {
        const cellA = a.cells[column].innerText;
        const cellB = b.cells[column].innerText;
        return ( sortDirection === 'asc') ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    const tBody = document.querySelector('#employeeTable tbody');
    tBody.innerHTML = '';
    sortedRows.forEach(row => tBody.appendChild(row));
}

function updateSortSymbol(button, sortDirection) {
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.textContent = '⇅';
    });

    if (sortDirection === 'asc') button.textContent = '▲';
    else button.textContent = '▼';
}

//searchInput
function filterTable() {
    const input = document.querySelector('#searchInput');
    const searchText = input.value.toLowerCase();
    const tableBody = document.querySelector('#employeeTable tbody');
    const rows = tableBody.getElementsByTagName('tr');
    const searchWords = searchText.split(' ').filter(w => w !== '');
    let hasResult = false;

    if (searchText !== '') {
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let rowContainsData = false;

            for (let j = 0; j < cells.length; j++) {
                const cellText = cells[j].innerText.toLowerCase();
                const allWordsFound = searchWords.some(w => cellText.includes(w));
                if (allWordsFound) {
                    rowContainsData = true;
                    break;
                }
            }

            if (rowContainsData) {
                rows[i].style.display = '';
                hasResult = true;
            } else {
                rows[i].style.display = 'none';
            }
        }
    } else {
        for (let i = 0; i < rows.length; i++) {
            rows[i].style.display = '';
            hasResult = false;
        }
    }

    if (!hasResult) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td><p>Не удалось найти работников соответствующим критериям поиска</p></td>`;
        tr.style.display = '';

    }
}

function addEmployee() {
    const form = document.querySelector('#newEmployeeForm');
    if (form) form.style.display = 'block';
}

function hideForm() {
    const form = document.querySelector('#newEmployeeForm');
    if (form) form.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const employeeForm = document.getElementById('newEmployeeForm');
    employeeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addNewEmployee();
    });

    const submitBtn = document.getElementById('employeeSubmitBtn');

    const requireFields = Array.from(employeeForm.querySelectorAll('input[required]'));

    function checkFormCompletion() {
        const allFilled = requireFields.every(input => input.value.trim() !== "");
        submitBtn.disabled = !allFilled;
    }

    requireFields.forEach(input => {
        input.addEventListener('input', checkFormCompletion);
    });

    document.getElementById('url').addEventListener('input', handleInputValidation);
    document.getElementById('phone').addEventListener('input', handleInputValidation);

    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        console.log('filtering');
        filterTable();
    });
});

function handleInputValidation() {
    const phoneNumberInput = document.getElementById('phone');
    const urlInput = document.getElementById('url');
    const phoneNumber = phoneNumberInput.value;
    const url = urlInput.value;

    if (phoneNumber !== '' && !validatePhone(phoneNumber)) {
        phoneNumberInput.classList.add('input-error');
    } else {
        phoneNumberInput.classList.remove('input-error');
    }

    if (url !== '' && !validateUrl(url)) {
        urlInput.classList.add('input-error');
    } else {
        urlInput.classList.remove('input-error');
    }
}

function addNewEmployee() {
    const name = document.getElementById('name').value;
    const surname = document.getElementById('surname').value;
    const second_name = document.getElementById('second_name').value;
    const age = parseInt(document.getElementById('age').value);
    const job_position = document.getElementById('job_position').value;
    const photo = document.getElementById('photo').value;
    const email = document.getElementById('email').value;
    const phoneNumber = document.getElementById('phone').value;
    const url = document.getElementById('url').value;

    if (!validatePhone(phoneNumber) || !validateUrl(url)) {
        return
    }

    const employee = {
        name: name,
        surname: surname,
        second_name: second_name,
        age: age,
        job_position: job_position,
        photo: photo,
        email: email,
        phoneNumber: phoneNumber,
        url: url
    };


    // TODO: preloader + adding logic
    console.log('added');
}

function rewardEmployee() {
    const checkedCheckboxes = document.querySelectorAll('.select-checkbox:checked');
    const selectedEmployees = [];
    const rewardText = document.getElementById('reward-text');
    const reward = document.getElementById('reward').value;

    if (checkedCheckboxes) {
        checkedCheckboxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            const fullNameCell = row.querySelectorAll('td')[1];
            const fullName = fullNameCell.textContent;
            selectedEmployees.push(fullName);
        });
    }

    rewardText.innerHTML = ``;
    if (selectedEmployees.length > 0) {
        const employeeList = selectedEmployees.join(', ');
        rewardText.innerHTML += `<p>Премировать сотрудников баксами $ ${reward}: <strong>${employeeList}</strong></p>`;
    } else {
        rewardText.innerHTML += `<p>Не выбрано сотрудников для премирования</p>`;
    }
}

function validatePhone(phoneNumber) {
    const pattern = /^(\+375|8)?[\s-]?\(?\d{2,3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    return pattern.test(phoneNumber);
}

function validateUrl(url) {
    const pattern = /^(https?:\/\/).+(\.php|\.html)$/;
    return pattern.test(url);
}

//charts
function arcsinFunc(x) {
    return math.asin(x);
}

function taylorSeries(x, terms) {
    let sum = 0;
    if (math.abs(x) < 1) {
        for (let n = 0; n < terms; n++) {
            let coef = (n % 2 === 0) ? 1 : -1;
            let term = coef * math.pow(x, 2*n + 1) / ((2*n + 1) * math.factorial(n));
            sum += term;
        }
    }
    return sum;
}

function plot() {
    const xValues = [];
    const realFunctionValues = [];
    const seriesValues = [];

    const minX = -1, maxX = 1;

    const terms = parseInt(document.getElementById('terms').value);
    const step = parseFloat(document.getElementById('step').value);
    const duration = parseFloat(document.getElementById('duration').value);
    const animate = document.getElementById('animate').checked;

    //if (document.getElementById('resultTable').tBodies.length) document.getElementById('resultTable').tBodies; //clear table before writting
    const tableBody = document.getElementById('resultTable').tBodies[0];
    tableBody.innerHtml = '';

    for (let x = minX; x < maxX; x += step) {
        let realValue = arcsinFunc(x);
        let seriesValue = taylorSeries(x, terms);

        xValues.push(x);
        realFunctionValues.push(realValue);
        seriesValues.push(seriesValue);
        const eps = Math.abs(realValue - seriesValue);

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${x.toFixed(2)}</td>
            <td>${terms}</td>
            <td>${realValue.toFixed(5)}</td>
            <td>${seriesValue.toFixed(5)}</td>
            <td>${eps.toFixed(5)}</td>
        `;
        tableBody.appendChild(row);
    }

    const ctx = document.getElementById('fourierChart').getContext('2d');

    if (Chart.getChart('fourierChart')) {
        Chart.getChart('fourierChart')?.destroy(); //cleaning charts;
        console.log('exists');
    }

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [
                {
                    label: 'arcsin(x)',
                    data: realFunctionValues,
                    borderColor: 'rgba(75,192,192,1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'taylor',
                    data: seriesValues,
                    borderColor: 'rgba(255,99,132,1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            animations: animate ? {
                tension: {
                    duration: duration ? parseInt(duration) : 2000,
                    easing: 'linear',
                    from: 0,
                    to: 1,
                    loop: true
                },
            } : false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'x',
                        color: '#911',
                        font: {
                            family: 'Comic Sans MS',
                            size: 20,
                            weight: 'bold',
                            lineHeight: 1.2
                        },
                        padding: {top: 20, left: 0, right: 0, bottom: 0}
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'f(x)',
                        color: '#191',
                        font: {
                            family: 'Times',
                            size: 20,
                            style: 'italic',
                            lineHeight: 1.2
                        },
                        padding: {top: 30, left: 0, right: 0, bottom: 0}
                    }
                },
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: 'rgb(255, 99, 132)',
                    },
                    title: {
                        display: true,
                        text: 'comparsion of arcsin(x) and taylor',
                    }
                }
            }
        },
    });
}