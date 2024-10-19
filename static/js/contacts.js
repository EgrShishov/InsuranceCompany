export function displayDetails() {
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

export function sortColumn(column, sortDirection) {
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

export function updateSortSymbol(button, sortDirection) {
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.textContent = '⇅';
    });

    if (sortDirection === 'asc') button.textContent = '▲';
    else button.textContent = '▼';
}

//searchInput
export function filterTable() {
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

export function addEmployee() {
    const form = document.querySelector('#newEmployeeForm');
    if (form) form.style.display = 'block';
}

export function hideForm() {
    const form = document.querySelector('#newEmployeeForm');
    if (form) form.style.display = 'none';
}

export function handleInputValidation() {
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

export function addNewEmployee() {
    const phoneNumber = document.getElementById('phone').value;
    const url = document.getElementById('url').value;

    if (!validatePhone(phoneNumber) || !validateUrl(url)) {
        return
    }

    document.getElementById('newEmployeeForm').addEventListener('click', (e) => {
        e.preventDefault();
        const preloader = document.getElementById('preloader');
        preloader.style.display = 'flex';

        const data = {
            name: document.getElementById('name').value,
            second_name: document.getElementById('second_name').value,
            surname: document.getElementById('surname').value,
            age: document.getElementById('age').value,
            email: document.getElementById('email').value,
            branch_name: document.getElementById('branch_name').value,
            phone_number: document.getElementById('phone').value,
            position: document.getElementById('job_position').value,
            photo: document.getElementById('photo').value
        };

        fetch('/create_agent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка отправки данных');
            }
        })
        .then(data => {
            console.log('Успешно добавлено!', data);
            const tBody = document.querySelector('#employeeTable tbody');
            const agent = JSON.parse(data.message);
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    ${agent.photo ?
                        `<img src="${agent.photo}" alt="${agent.name} Photo" width="100" height="100" style="object-fit:cover;">` :
                        `<img src="/static/images/default_profile.svg" alt="Default Photo" width="100" height="100" style="object-fit:cover;">`
                    }
                </td>
                <td>${agent.surname} ${agent.name} ${agent.second_name}</td>
                <td>${agent.position}</td>
                <td>${agent.age}</td>
                <td>${agent.phone}</td>
                <td>${agent.email}</td>
                <td><input type="checkbox" class="select-checkbox" data-id="${agent.id}"></td>
            `;
            tBody.appendChild(tr);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            preloader.style.display = 'none';
            alert('Ошибка при добавлении сотрудника.');
        })
        .finally(() => {
            preloader.style.display = 'none';

        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function rewardEmployee() {
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

export function validatePhone(phoneNumber) {
    const pattern = /^(\+375|8)?[\s-]?\(?\d{2,3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    return pattern.test(phoneNumber);
}

export function validateUrl(url) {
    const pattern = /^(https?:\/\/).+(\.php|\.html)$/;
    return pattern.test(url);
}
