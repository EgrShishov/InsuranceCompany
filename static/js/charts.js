//charts
export function arcsinFunc(x) {
    return math.asin(x);
}

export function taylorSeries(x, terms) {
    let sum = 0;
    if (math.abs(x) < 1) {
        for (let n = 0; n < terms; n++) {
            let term = math.factorial(2*n) * math.pow(x, 2*n + 1) / (math.pow(4, n) * (2*n + 1) * math.pow(math.factorial(n), 2));
            sum += term;
        }
    }
    return sum;
}

export function plot() {
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