from django.urls import reverse

from books.models import Book, BookReview
from books.tests import BockTestCase
from users.models import CustomUser


class HomePageTestCase(BockTestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Books1", description="Description1", isbn="111111")
        user = CustomUser.objects.create(
            username="suxrob", first_name="Alibek", last_name='Yoqubov', email='suxrob@gmail.com'
        )
        user.set_password('admin2')
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given = 3, comment = "Nice book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Nice books")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=2, comment="Nice book2")

        response = self.client.get(reverse("home_page")+"?page_size=2")

        self.assertContains(response, review1.comment)
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
