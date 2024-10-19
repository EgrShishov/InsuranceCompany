export default class Slider {
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