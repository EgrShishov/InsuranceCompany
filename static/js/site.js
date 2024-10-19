import Slider from './slider.js';
import Pagination from './pagination.js';
import { Person, Student, StudentsTask } from './task.js';
import { generateTable, transposeTable, printTable, markCell, isNeighboursSelected,
            addNewColumn, addNewRow, getRandomInt } from './table.js';
import { applyPromocode, cancelPromocode } from './promocode.js';
import { updateCountdown } from './countdown.js';
import { checkAge, validateAge, showMainContent } from './agecheck.js';
import { displayDetails, sortColumn, filterTable, addEmployee, hideForm, updateSortSymbol, handleInputValidation,
            addNewEmployee, rewardEmployee, validatePhone, validateUrl} from './contacts.js';
import { plot, taylorSeries, arcsinFunc } from './charts.js';
/*
window.addEmployee = addEmployee;
window.hideForm = hideForm;
window.handleInputValidation = handleInputValidation;
window.addNewEmployee = addNewEmployee;
window.rewardEmployee = rewardEmployee;
window.validatePhone = validatePhone;
window.validateUrl = validateUrl;

window.generateTable = generateTable;
window.transposeTable = transposeTable;
window.printTable = printTable;
window.markCell = markCell;
window.isNeighboursSelected = isNeighboursSelected;
window.addNewColumn = addNewColumn;
window.addNewRow = addNewRow;
window.getRandomInt = getRandomInt;

window.applyPromocode = applyPromocode;
window.cancelPromocode = cancelPromocode;

window.updateCountdown = updateCountdown;
*/

window.checkAge = checkAge;
window.validateAge = validateAge;
window.showMainContent = showMainContent;

window.displayDetails = displayDetails;
window.sortColumn = sortColumn;
window.filterTable = filterTable;

window.plot = plot;
window.taylorSeries = taylorSeries;
window.arcsinFunc = arcsinFunc;

// preloader
window.addEventListener('load', function() {
    const loader = document.getElementById('preloader');
    loader.style.display = 'none';
});

//parallax
window.addEventListener('scroll',() => {
    const money_left = document.getElementById('money_left');
    const money_right = document.getElementById('money_right');
    const text = document.getElementById('text');
    let value = scrollY;
    money_left.style.left = `-${value/0.7}px`
    money_right.style.left = `${value/0.7}px`
    text.style.bottom = `-${value}px`;
})

window.moveToNext = function moveToNext(current, nextFieldId) {
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

window.moveToPrev = function moveToPrev(current, prevFieldId) {
    if (current.value.length === 0 && event.key === 'Backspace') {
        document.getElementById(prevFieldId).focus();
    }
}

window.updateStyles = function updateStyles() {
    console.log('c');
    if (applySettingsCheckbox.checked) {
        console.log('checked');
        document.body.style.fontSize = fontSizeSelector.value;
        document.body.style.color = textColorInput.value;
        document.body.style.backgroundColor = bgColorInput.value;
    }
}

let fontSizeSelector = null;
let textColorInput = null;
let bgColorInput = null;
let applySettingsCheckbox = null;

document.addEventListener('DOMContentLoaded', () => {
    checkAge();
    const countdownElement = document.getElementById('counter');

    const slider = new Slider('#slider', '#banner_form');
    slider.startBannerRotation();

    if (!endTime) {
       endTime = now + oneHour;
       localStorage.setItem('endTime', endTime);
    }
    const interval = setInterval(updateCountdown, 1000);

    promoCode = localStorage.getItem('promo');
    applyPromocode();
});

document.addEventListener('DOMContentLoaded', () => {
    fontSizeSelector = document.getElementById('fontSize');
    textColorInput = document.getElementById('textColor');
    bgColorInput = document.getElementById('bgColor');
    applySettingsCheckbox = document.getElementById('applySettings');

    console.log(applySettingsCheckbox);
    console.log('mama');

    fontSizeSelector.addEventListener('change', () => updateStyles());
    textColorInput.addEventListener('input', () => updateStyles());
    bgColorInput.addEventListener('input', () => updateStyles());
    applySettingsCheckbox.addEventListener('change', () => updateStyles());

    updateStyles();
});

//map with openmapapi
let map, marker, accuracyCircle;

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
    window.copyToClipBoard = function copyToClipBoard() {
        const textToCopy = document.querySelector('#editor').value;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert('Скопировано в буфер обмена');
        }).catch(err => {
             console.error('Ошибка копирования текста: ', err);
        });
    }

    window.pasteFromClipboard = function pasteFromClipboard() {
        navigator.clipboard.readText().then((clipText) => {
            document.querySelector('#second-editor').value += clipText;
        }).catch(err => {
            console.error('Ошибка вставки текста: ', err);
        });
    }
})

document.addEventListener('DOMContentLoaded', () => {
    const pagination = new Pagination('pagination', 3, '.employee-card');
});

document.addEventListener('DOMContentLoaded', () => {
    const types_pagination = new Pagination('types-pagination', 3, '.grid-item');

    const cards = document.querySelectorAll('.grid-item');
    cards.forEach(card => {
         card.addEventListener('mousemove', e => {
           const [x, y] = [e.offsetX, e.offsetY];
           const rect = card.getBoundingClientRect();
           const [width, height] = [rect.width, rect.height];
           const middleX = width / 2;
           const middleY = height / 2;
           const offsetX = ((x - middleX) / middleX) * 25;
           const offsetY = ((y - middleY) / middleY) * 25;
           const offX = 50 + ((x - middleX) / middleX) * 25;
           const offY = 50 - ((y - middleY) / middleY) * 20;

           card.style.setProperty('--rotateX', 1 * offsetX + 'deg');
           card.style.setProperty('--rotateY', -1 * offsetY + 'deg');
           card.style.setProperty('--posx', offX + '%');
           card.style.setProperty('--posy', offY + '%');

           const color1 = `rgb(${Math.min(255, Math.abs(x - middleX) * 2)}, ${Math.max(100, 255 - x)}, ${Math.max(150, 255 - y)})`;
           const color2 = `rgb(${Math.max(100, x)}, ${Math.min(255, Math.abs(y - middleY) * 2)}, ${Math.max(150, 255 - x)})`;
           card.style.setProperty('--gradientColor1', color1);
           card.style.setProperty('--gradientColor2', color2);

           console.log('mousemoved');
          });

         card.addEventListener('mouseleave', e => {
            card.style.animation = 'reset-card 1s ease';
            card.addEventListener("animationend", e => {
                card.style.animation = 'unset';
                card.style.setProperty('--rotateX', '0deg');
                card.style.setProperty('--rotateY', '0deg');
                card.style.setProperty('--posx', '50%');
                card.style.setProperty('--posy', '50%');
                card.style.setProperty('--gradientColor1', 'lightblue');
                card.style.setProperty('--gradientColor2', 'white');
              console.log('mouseleaved');
            }, { once: true });
          });
      });
});

let currentSortDirection = {};

document.addEventListener('DOMContentLoaded', () => {
    console.log(document.querySelectorAll('.sort-btn'));
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
});

document.addEventListener('DOMContentLoaded', () => {
    const employeeForm = document.getElementById('newEmployeeForm');
    employeeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addNewEmployee();
    });

    const requireFields = Array.from(employeeForm.querySelectorAll('input[required]'));

    function checkFormCompletion() {
        const allFilled = requireFields.every(input => input.value.trim() !== "");
        document.getElementById('employeeSubmitBtn').disabled = !allFilled;
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

    displayDetails();
    const openBtn = document.getElementById('addEmployeeBtn');
    openBtn.addEventListener('click', () => addEmployee());

    const hideBtn = document.getElementById('hide-btn');
    hideBtn.addEventListener('click', () => hideForm());

    const rewardBtn = document.getElementById('premiateBtn');
    rewardBtn.addEventListener('click', () => rewardEmployee());
});

let studentTask = null;

document.addEventListener('DOMContentLoaded', () => {
    studentTask = new StudentsTask();

    const studentForm = document.getElementById('studentsForm');
    studentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        console.log('submitted');
        studentTask.addStudent();
    });

    document.getElementById('calculate').addEventListener('click', (e) => {
        e.preventDefault();
        studentTask.calculateMaxMalePercentage();
    });
});
