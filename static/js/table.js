let table = [];
// generating random table with given sizes
export function generateTable() {
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

export function transposeTable() {
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

export function printTable(table) {
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

export function markCell(td, row, col) {
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

export function isNeighboursSelected(rowCells, col) {
    const canMarkNeighbours = document.getElementById('can').checked;
    console.log(canMarkNeighbours);
    if (canMarkNeighbours) return false;
    if (col > 0 && rowCells[col - 1].classList.contains('selected')) return true;
    if (col < rowCells.length - 1 && rowCells[col + 1].classList.contains('selected')) return true;
    return false;
}

export function addNewColumn() {
    let newColumn = [];
    let cols = table[0].length;

    for (let i = 0; i < cols; i++) {
       newColumn.push(getRandomInt(1, 100));
    }

    table.push(newColumn);
    printTable(table);
}

export function addNewRow() {
    for (let i = 0; i < table.length; i++) {
        table[i].push(getRandomInt(1, 100));
    }
    printTable(table);
}

export function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}