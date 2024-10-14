let currentIndex = 0;
let banners = [];
let intervalTime = 3000;
let intervalId;
let table = [];
let promoCode = localStorage.getItem('promo');

const oneHour = 1000 * 60 * 60;
let now = new Date().getTime();
let endTime = localStorage.getItem('endTime');

let fontSizeSelector;
let textColorInput;
let bgColorInput;
let applySettingsCheckbox;

const promoCodes = {
    'SAVE10': 0.9,
    'HELLOWORLD': 0.95,
    'MEGAJOPA': 0.6
};

document.addEventListener('DOMContentLoaded', () => {
    banners = document.querySelectorAll('.banner');
    const countdownElement = document.getElementById('counter');

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

    fontSizeSelector.addEventListener('change', updateStyles);
    textColorInput.addEventListener('input', updateStyles);
    bgColorInput.addEventListener('input', updateStyles);
    applySettingsCheckbox.addEventListener('change', updateStyles);

    document.getElementById('banner_form').addEventListener('submit', function(e) {
        e.preventDefault();
        const newInterval = document.getElementById('interval').value;
        console.log(newInterval);
        intervalTime = parseInt(newInterval, 10);
        startBannerRotation();
    });
});

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

function showNextBanner() {
    banners[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1 ) % banners.length;
    banners[currentIndex].classList.add('active');
}

function startBannerRotation() {
    clearInterval(intervalId);
    intervalId = setInterval(showNextBanner, intervalTime);
}

window.addEventListener('focus', function() {
    startBannerRotation();
});

window.addEventListener('blur', function() {
    clearInterval(intervalId);
});

startBannerRotation();

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
    console.log(2);
    console.log(applySettingsCheckbox.checked);
    if (applySettingsCheckbox.checked) {
        console.log(1);
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

let students = new Map();
let studentsCount = 0;

function addStudent() {
    const surname = document.getElementById('surname').value;
    const name = document.getElementById('name').value;
    const second_name = document.getElementById('second_name').value;
    const sex = document.getElementById('sex').value;
    const age = document.getElementById('age').value;
    const course = document.getElementById('course').value;

    const student = {
        surname: surname,
        name: name,
        age: age,
        sex: sex,
        course: course
    };

    students[studentsCount] = student; // or students.set

    const studentsList = document.getElementById('students');
    const ul = document.createElement('ul');
    ul.innerHTML = '';

    const li = document.createElement('li');
    li.textContent = `Фамилия: ${student.surname}, Имя: ${student.name}, Возраст: ${student.age}, Пол: ${student.sex}, Курс: ${student.course}`;
    studentsList.appendChild(li);
    studentsList.appendChild(ul);

    document.getElementById('studentForm').reset();
    studentsCount++;
}

function calculate() {
    const courseData = {};
    let topCourse = null;
    let maxPercentage = 0;
    const topCourseElement = document.getElementById('top-course');

    for (const id in students) {
        const student = students[id];
        const course = student.course;
        const isMale = student.sex === 'М';

        if (!courseData[course]) {
            courseData[course] = {males: 0, total: 0};
        }

        courseData[course].total++;

        if (isMale) {
            courseData[course].males++;
        }
    }

    for (const course in courseData) {
        const data = courseData[course];
        const malePercentage = (data.males / data.total) * 100;

        if (malePercentage > maxPercentage) {
            maxPercentage = malePercentage;
            topCourse = course;
        }
    }

    topCourseElement.textContext = `Курс ${topCourse}: ${maxPercentage.toFixed(2)}% мужчин`;
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
            cell.addEventListener('click', () => markCell(tableContainer, i, j));
            row.appendChild(cell);
        }
        htmlTable.appendChild(row);
    }
    tableContainer.appendChild(htmlTable);
}

function markCell(td, row, col) {
    const maxSelections = parseInt(document.getElementById('num'));
    const canMarkNeighbours = document.getElementById('can');
    const rowCells = document.querySelectorAll(`#table tr:nth-child(${row + 1}) td`);
    const selectedCount = Array.from(rowCells).filter(c => c.classList.contains('selected')).length;

    if (selectedCount >= maxSelections && !td.classList.contains('selected')) {
        alert(`Максимальное количество выделенных ячеек в строке: ${maxSelections}`);
        return;
    }

    if (isNeighboursSelected(rowCells, col)) {
        alert('Нельзя выделить ячейку, так как соседние уже выделены.');
        return;
    }

     td.classList.toggle('selected');
     td.classList.toggle(td.textContent % 2 === 0 ? 'even' : 'odd');
}

function isNeighboursSelected(rowCells, col) {
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

// class example
class InsuranceType {
    constructor(id, typeName) {
        this.id = id;
        this.typeName = typeName;
    }
}

class CompanyBranch {
    constructor(id, branchName) {
        this.id = id;
        this.branchName = branchName;
    }
}

class InsuranceObject {
    constructor(id, objectName) {
        this.id = id;
        this.objectName = objectName;
    }
}

class InsuranceAgent {
    constructor(id, agentName) {
        this.id = id;
        this.agentName = agentName;
    }
}

class InsuranceClient {
    constructor(id, clientName) {
        this.id = id;
        this.clientName = clientName;
    }
}

class InsuranceContract {
    #moneyLimit = 100;
    static #privateStaticField = 'This is a private static field';

    constructor(date, insuranceSum, insuranceType, tariffRate, branchName, insuranceObject, agent, client) {
        this.date = new Date(date);
        this.insuranceSum = insuranceSum;
        this.insuranceType = insuranceType;
        this.tariffRate = tariffRate;
        this.branchName = branchName;
        this.insuranceObject = insuranceObject;
        this.agent = agent;
        this.client = client;
    }

    getTotalAmount() {
        return this.insuranceSum * (1 + this.tariffRate);
    }

    #privateMethod() {
        console.log('this is a private method');
    }

    get sum() {
        return this.insuranceSum;
    }

    set sum(value) {
        if (value < 0) {
            throw new Error('Sum cannot be negative');
        }
        this._sum = value;
    }
}
// wrapper
function wrapper(a, b, c) {
    //return function(a, b) + c; // todo
}

function sum(a, b) {
    return a + b;
}
// extends class example
class InsuranceContractFormatter extends InsuranceContract {
    getFormattedInsuranceContract() {
        return `Date:${this.date.toLocaleDateString()}\nSum:${this.insuranceSum}\ntype:${this.insuranceType.typeName}`;
    }
}

// another way to extends
/*class AnotherContractFormatter<A extends InsuranceContract = InsuranceContract> {

}*/

const lifeInsurance = new InsuranceType(1, 'Life Insurance');
const healthInsurance = new InsuranceType(2, 'Health Insurance');

const branchNY = new CompanyBranch(1, 'New York Branch');
const branchLA = new CompanyBranch(2, 'Los Angeles Branch');

const house = new InsuranceObject(1, 'House');
const car = new InsuranceObject(2, 'Car');

const agentJohn = new InsuranceAgent(1, 'John Doe');
const agentJane = new InsuranceAgent(2, 'Jane Smith');

const clientAlice = new InsuranceClient(1, 'Alice Johnson');
const clientBob = new InsuranceClient(2, 'Bob Smith');

const contract1 = new InsuranceContract(
    '2024-10-14',
    100000,
    lifeInsurance,
    0.05,
    branchNY,
    house,
    agentJohn,
    clientAlice
);

console.log(new InsuranceContractFormatter(contract1).getFormattedInsuranceContract());