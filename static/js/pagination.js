export default class Pagination {
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
        else if (page > this.totalPages) this.currentPage = this.totalPages;
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