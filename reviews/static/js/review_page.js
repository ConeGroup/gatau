async function getBooks() {
    return fetch("{% url 'reviews:get_book_json' %}").then((res) => res.json())
}

async function openReviewModalWithBookData(bookTitle, bookAuthor, bookYear, bookISBN, bookCoverURL, bookId) {
document.getElementById('reviewModalBookId').value = bookId;
document.getElementById('reviewModalTitle').textContent = bookTitle;
document.getElementById('reviewModalCover').src = bookCoverURL;
document.getElementById('reviewModalAuthor').textContent = bookAuthor;
document.getElementById('reviewModalYear').textContent = bookYear;
document.getElementById('reviewModalISBN').textContent = bookISBN;
$('#reviewModal').modal('show');
}

const placeholderImageUrl = "{% static 'BLANK.png' %}";

async function refreshBookCards() {
document.getElementById("book_card").innerHTML = "";
const books = await getBooks();
let htmlString = ` <div class="row row-cols-1 row-cols-md-4 mb-3 text-center">`;

books.forEach((book) => {
    const bookImageUrl = getBookImageUrl(book);
    htmlString += `
        <div class="col mb-4">
            <div class="shadow mb-3 bg-body">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title font-weight-bold" style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">${book.fields.title}</h5>
                        <div class="image-container ">
                            <img src="${bookImageUrl}" alt="Book Cover" style="width: 106px; height: 160px;">
                        </div>
                        <p></p>
                        <h6 class="card-text">${book.fields.author}</h6>
                        <p>${book.fields.year}</p>

                        <button
                            type="button"
                            class="btn btn-primary review-button"
                            data-bs-toggle="modal"
                            data-bs-target="#reviewModal"
                            data-book-title="${book.fields.title}"
                            data-book-cover="${bookImageUrl}"
                            data-book-author="${book.fields.author}"
                            data-book-year="${book.fields.year}"
                            data-book-ISBN="${book.fields.ISBN}"
                            data-book-id="${book.pk}"
                        >
                            Review this Book
                        </button>
                        <p></p>

                        <div class="card-footer">
                            <small class="text-muted">ISBN ${book.fields.ISBN}</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
});

htmlString += `</div>`;
document.getElementById("book_card").innerHTML = htmlString;

const reviewButtons = document.querySelectorAll('.review-button');
reviewButtons.forEach((button) => {
    button.addEventListener('click', function () {
        const bookTitle = this.getAttribute('data-book-title');
        const bookCoverURL = this.getAttribute('data-book-cover');
        const bookAuthor = this.getAttribute('data-book-author');
        const bookYear = this.getAttribute('data-book-year');
        const bookISBN = this.getAttribute('data-book-ISBN');
        const bookId = this.getAttribute('data-book-id');

        openReviewModalWithBookData(bookTitle, bookAuthor, bookYear, bookISBN, bookCoverURL, bookId);
    });
});
}
refreshBookCards()

function getBookImageUrl(book) {

const imageUrl = book.fields.image_m;

const img = new Image();

img.src = imageUrl;

img.onload = function () {
    if (img.width <= 5 || img.height <= 5) {
        img.src = placeholderImageUrl;
    }
 };

return img.src;
}

async function addReview() {
const bookId = document.getElementById('reviewModalBookId').value;
const data = new FormData(document.querySelector('#form'));
data.append('book_id', bookId); 

fetch("{% url 'reviews:add_review_ajax' %}", {
        method: "POST",
        body: data
    }).then((response) => {
        if (response.status === 201) {
            displayNotification('Your review has been successfully added!');
            refreshBookCards();
            document.getElementById("form").reset();
        } else {
            displayNotification('Failed to add review :( Please try again.');
        }
        })
        .catch((error) => {
            displayNotification('An error occurred. Please try again.');
        });
    return false
}

document.getElementById("add_review_btn").onclick = addReview


function displayNotification(message) {
    const notificationMessage = document.getElementById('notificationMessage');
    notificationMessage.textContent = message;
    $('#notificationModal').modal('show');
}
