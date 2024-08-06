from django.urls import path
from books.views import BooksView, BooksDetailView, AddReviewView, EditReviewView,ConfirmDeleteReviewView,DeleteReviewView

app_name = 'books'

urlpatterns = [
    path("", BooksView.as_view(), name = 'list'),
    path("<int:id>/", BooksDetailView.as_view(), name = "detail"),
    path("<int:id>/review/", AddReviewView.as_view(), name = "reviews"),
    path("<int:book_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name = "review-edit"),
    path("<int:book_id>/reviews/<int:review_id>/confirm/delete/", ConfirmDeleteReviewView.as_view(), name = "confirm-review-delete"),
    path("<int:book_id>/reviews/<int:review_id>/delete/", DeleteReviewView.as_view(), name = "review-delete"),
]