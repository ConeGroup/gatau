        async function getBooks() {
            return fetch("{% url 'reviews:get_book_json' %}").then((res) => res.json())
        }
        async function getReviews() {
            return fetch("{% url 'reviews:get_review_json' %}").then((res) => res.json())
        }

        async function getBookById(idBuku) {
            const url = "/reviews/get-book-by-id/" + idBuku; 
            return fetch(`/reviews/get-book-by-id/${idBuku}`).then((res) => res.json());
        }


    async function openReviewModalWithBookData(bookTitle, bookAuthor, bookYear, bookISBN, bookCoverURL, bookId) {
        document.getElementById('reviewModalBookId').value = bookId;
        document.getElementById('reviewModalTitle').textContent = bookTitle;
        document.getElementById('reviewModalCover').src = bookCoverURL;
        document.getElementById('reviewModalAuthor').textContent = bookAuthor;
        document.getElementById('reviewModalYear').textContent = bookYear;
        document.getElementById('reviewModalISBN').textContent = "ISBN : " + bookISBN;
        $('#reviewModal').modal('show');
    }

    const placeholderImageUrl = "{% static 'BLANK.png' %}";

    async function refreshBookReviewCards() {
        document.getElementById("book_card").innerHTML = "";
        const books = await getBooks();
        const reviews = await getReviews();
        let htmlString = ` <div class="row row-cols-1 row-cols-md-2 mb-3 text-center">`;

        books.forEach((book) => {
            const bookImageUrl = getBookImageUrl(book);
            htmlString += `
                <div class="col mb-4">
                    <div class="shadow mb-3 bg-body">
                        <div class="card">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-sm-4">
                                        <div class="image-container ">
                                            <img src="${bookImageUrl}" alt="Book Cover" style="width: 106px; height: 160px;">
                                        </div>
                                    </div>
                                    <div class="col-sm-8 align-self-center">
                                        <h5 class="card-title font-weight-bold" style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">${book.fields.title}</h5>
                                        <p class="card-text">by ${book.fields.author}</p>

                                    </div>
                                </div>
                                <div class="card-footer mt-3">
                                    <div class='row' data-base-url="{% url 'reviews:book_details' 0 %}">
                                        <button type="button" class="detail-button btn btn-primary" data-book-id="${book.pk}">View Book Details</button>
                                    </div>
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

            $('.detail-button').on('click', function() {
                const bookId = this.getAttribute('data-book-id');
                const baseUrl = $('div[data-base-url]').data('base-url');
                const url = baseUrl.replace('0', bookId);
                window.location.href = url;
        });


    }
    refreshBookReviewCards()


async function refreshUserReviewCards() {
    const userReviewsContainer = document.getElementById('user_reviews');
    userReviewsContainer.innerHTML = ''; 

    try {
        const response = await fetch("{% url 'reviews:get_review_by_user_json' %}");
        if (response.ok) {
            const data = await response.json();
            if (data.reviews.length === 0) {
                userReviewsContainer.innerHTML = "<p>You haven't write any review, yet. </p>";
            } else {

                let htmlString = `<div class="row row-cols-1 row-cols-md-3 mb-3 text-center">`;
                data.reviews.forEach((review) => {
                    let desc = review.book_review_desc

                    htmlString += `
                        <div class="col mb-3 ml-7">
                            <div class="shadow mb-3 bg-body">
                                <div class="card">
                                    <div class="card-body">
                                        <h4 class="card-title font-weight-bold">${review.book_title}</h4>
                                        <p class="card-text">Rating: ${review.rating}</p>

                                        
                                        <p class="card-text">
                                            <span class="book-description">
                                                ${desc.slice(0, 200)}
                                                ${desc.length > 200 ?
                                                    `<p><a href="#" class="show-more-link" data-bs-toggle="collapse" data-bs-target="#collapseDesc${review.id}">Show more</a><p>` :
                                                    ''
                                                }
                                            </span>
                                        </p>
                                        <div id="collapseDesc${review.id}" class="collapse">
                                            <p class="card-text">${review.book_review_desc}</p>
                                        </div>

                                        <p class="card-text">You ${review.is_recommended ? 'recommend' : 'did not recommend'} this</p>                                        
                                        <nav aria-label="..." class="pag-1">
                                            <div class="row">
                                                <div class="div-rm col">
                                                    <button type="button" class="btn btn-success" id="update-card" data-bs-toggle="modal" data-bs-target="#editReviewModal">Edit</button>
                                                </div>
                                                <div class="div-rm col">
                                                    <button class="btn btn-danger" id="rm-btn" onclick="deleteReview(${review.id})">Delete</button>
                                                </div>
                                            </div>
                                        </nav>
                                        <div class="card-footer mt-3">
                                            <small class="text-muted">Date Added ${review.date_added}</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal" id="editReviewModal" tabindex="-1" role="dialog" aria-labelledby="editReviewModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="editReviewModalLabel">Edit Review</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <form id="editReviewForm" method="post">
                                        {% csrf_token %}
                                        <div class="form-group">
                                            <label for="editRating">Rating:</label>
                                            <input type="number" name="editRating" id="editRating" value="{{ review.rating }}">
                                        </div>
                                        <div class="form-group">
                                            <label for="book_review_desc">Review:</label>
                                            <textarea name="editDeskripsi" id="editDeskripsi"></textarea>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" name="edit_is_recommended" id="edit_is_recommended" {% if review.is_recommended %}checked{% endif %}>
                                            <label class="form-check-label" for="edit_is_recommended">I recommend this book</label>
                                        </div>
                                    </form>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" id="button_edit${review.pk}" data-bs-toggle="modal" data-bs-target="#exampleModal" onclick="updateReview(${review.pk})">Save Changes</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    `;
                });
                htmlString += `</div>`;
                userReviewsContainer.innerHTML = htmlString;

                const editReviewButtons = document.querySelectorAll('.edit-review');

                editReviewButtons.forEach(button => {
                    button.addEventListener('click', async () => {
                        const reviewId = button.getAttribute('data-review-id');

                        const response = await fetch(`/reviews/get_review_by_id/${reviewId}/`);
                        if (response.ok) {
                            const review = await response.json();
                            document.getElementById('editRating').value = review.rating;
                            document.getElementById('editDeskripsi').value = review.book_review_desc; 
                            document.getElementById('edit_is_recommended').value = review.is_recommended; 

                            $('#editReviewModal').modal('show');
                        } else {
                            console.error('Failed to fetch review data for editing.');
                        }
                    });
                });
                const showMoreLinks = document.querySelectorAll('.show-more-link');
                showMoreLinks.forEach(link => {
                    link.addEventListener('click', (event) => {
                        event.preventDefault();
                    });
                });
            }
        } else {
            console.error('Failed to fetch user reviews.');
        }
    } catch (error) {
        console.error('An error occurred while fetching user reviews:', error);
    }
}

refreshUserReviewCards();

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

    function displayNotification(message) {
        const notificationMessage = document.getElementById('notificationMessage');
        notificationMessage.textContent = message;
        $('#notificationModal').modal('show');
    }
    
    function handleSaveChanges(reviewId) {
        const editReviewForm = document.getElementById('editReviewForm');
        const formData = new FormData(editReviewForm);

        fetch(`/reviews/update-review/${reviewId}/`, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                $('#editReviewModal').modal('hide');
                refreshUserReviewCards(); 
            } else {
                console.error('Failed to update the review.');
            }
        })
        .catch(error => {
            console.error('An error occurred while updating the review:', error);
        });
    }

    const saveEditReviewButton = document.getElementById('saveEditReviewButton');
    saveEditReviewButton.addEventListener('click', () => {
        const reviewId = this.getAttribute('data-review-id');
        handleSaveChanges(reviewId);
    });


    async function updateReview(id) {
        let url="{% url 'reviews:edit_review' '0' %}";
        url= url.replace('0',id);
        const response = await fetch(url,{
            method: "POST",
            body: new FormData(document.querySelector('#form')),
        }).then(refreshUserReviewCards(id))
        resetForm()
    }
        
    function resetForm() {
        document.getElementById("form").reset()
    }
    async function deleteReview(id) {
        let url="{% url 'reviews:delete_review' '0' %}";
        let count = 0
        url=url.replace('0',id);
        const response = await fetch(url,{
            method: "DELETE",
        }).then(refreshUserReviewCards)
    }
