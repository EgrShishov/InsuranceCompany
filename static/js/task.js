export class Person {
    constructor(surname, name, second_name, gender, age) {
        this.surname = surname;
        this.name = name;
        this.second_name = second_name;
        this.gender = gender;
        this.age = age;
    }

    get age() {
        console.log('mama');
    }

    set age(value) {
        if (value > 150 || value < 0) {
            alert('incorrect age bounds');
            return;
        }
    }

    getFullName() {
        return `${this.surname} ${this.name} ${this.second_name}`;
    }
}

export class Student extends Person {
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
export function Person(surname, name, second_name, gender, age) {
    this.surname = surname;
    this.name = name;
    this.second_name = second_name;
    this.gender = gender;
    this.age = age;

    this.setAge = function(value) {
        if (age < 0 || age > 150) {
            alert('incorrect age bounds');
            return;
        }
    }

    this.getAge = function() {
        return this.age;
    }
}

Person.prototype.getFullName = function() {
    return `${this.surname} ${this.name} ${this.patronymic}`;
};


//extends
export function Student(surname, name, second_name, gender, age, course) {
    Person.call(this, surname, name, second_name, gender, age);
    this.course = course;

    this.getCourse = function() {
        return this.course;
    }

    this.setCourse = function(value) {
        if (value < 1 || value > 5) {
            alert('incorrect course bounds');
            return;
        }
    }
}

Student.prototype = Object.Create(Person.prototype);
Student.prototype.constructor = Student;
*/

export class StudentsTask {
    constructor() {
        this.studentsCount = 0;
        this.students = JSON.parse(localStorage.getItem('students')) || [];
    }

    addStudent() {
        const surname = document.getElementById('surname').value;
        const name = document.getElementById('name').value;
        const second_name = document.getElementById('second_name').value;
        const sex = document.getElementById('sex').value;
        const age = document.getElementById('age').value;
        const course = document.getElementById('course').value;

        const student = new Student(surname, name, second_name, sex, parseInt(age), parseInt(course));
        this.students.push(student);

        localStorage.setItem('students', JSON.stringify(this.students));

        this.displayStudents();
        this.calculateMaxMalePercentage();
    }

    displayStudents() {
        const studentsList = document.getElementById('students');
        studentsList.innerHtml = '';

        this.students.forEach((student, index) => {
            const studentDiv = document.createElement('div');
            studentDiv.classList.add('student');
            studentDiv.innerHTML += `<p>${index + 1}. ${student.surname} ${student.name} ${student.second_name}, Пол: ${student.gender}, Возраст: ${student.age}, Курс: ${student.course}</p>`;
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
};
