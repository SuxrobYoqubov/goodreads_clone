from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


# Create your tests here.

class BockTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found")


    def test_books_list(self):
        book1 = Book.objects.create(title="Books1", description="Description1", isbn="111111")
        book2 = Book.objects.create(title="Books2", description="Description2", isbn="111121")
        book3 = Book.objects.create(title="Books3", description="Description3", isbn="111131")

        response = self.client.get(reverse("books:list")+"?page_size=2")

        books = Book.objects.all()

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list")+"?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Books1", description="Description1", isbn="111111")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        book2 = Book.objects.create(title="Super Car", description="Description2", isbn="111121")
        book3 = Book.objects.create(title="Microsoft", description="Description3", isbn="111131")

        response = self.client.get(reverse("books:list")+"?q=Sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Car")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse("books:list") + "?q=Microsoft")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        user = CustomUser.objects.create(
            username="suxrob", first_name="Alibek", last_name='Yoqubov', email='suxrob@gmail.com'
        )
        user.set_password('admin2')
        user.save()
        self.client.login(username='suxrob', password='admin2')

        response = self.client.post(reverse("books:reviews", kwargs={"id":book.id}), data={
            "stars_given":3,
            "comment":"Nice book",
        })

        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)