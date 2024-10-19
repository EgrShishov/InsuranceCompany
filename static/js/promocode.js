let promoCode = localStorage.getItem('promo');

const promoCodes = {
    'SAVE10': 0.9,
    'HELLOWORLD': 0.95,
    'MEGAJOPA': 0.6
};


//for promocodes
export function applyPromocode() {
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

export function cancelPromocode() {
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