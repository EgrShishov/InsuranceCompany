
export function checkAge() {
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('age-checker').style.display = 'block';

    const ageConfirmed = localStorage.getItem('ageConfirmed');
    if (ageConfirmed === 'true') {
        showMainContent();
    } else {
        document.getElementById('age-checker').style.display = 'flex';
        document.getElementById('main-content').style.display = 'none';
    }
}

export function validateAge() {
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

export function showMainContent() {
    document.getElementById('main-content').style.display = 'block';
    document.getElementById('age-checker').style.display = 'none';
}