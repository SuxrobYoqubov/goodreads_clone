from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="suxrob", first_name="Suxrob")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username = 'suxrob', password = 'somepass')

    def test_book_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        br =BookReview.objects.create(book=book, user=self.user, stars_given = 5, comment = "Nice book")

        response = self.client.get(reverse("api:review-detail", kwargs={"id":br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Nice book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Sport')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], '111111')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'Suxrob')
        self.assertEqual(response.data['user']['username'], 'suxrob')




    def test_book_review_list(self):
        user2 = CustomUser.objects.create(username="somebody", first_name="Sombody")
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")
        br2 = BookReview.objects.create(book=book, user=user2, stars_given=5, comment="Nice book")

        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data["count"], 2)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        # self.assertEqual(response.data["results"][0]['id'], br2.id)
        self.assertEqual(response.data["results"][0]['stars_given'], 5)
        self.assertEqual(response.data["results"][0]['comment'], 'Nice book')
        # self.assertEqual(response.data["results"][1]['id'], br.id)
        self.assertEqual(response.data["results"][1]['stars_given'], 5)
        self.assertEqual(response.data["results"][1]['comment'], 'Nice book')


    def test_delete_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.delete(reverse("api:review-detail", kwargs={"id":br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.patch(reverse("api:review-detail", kwargs={"id": br.id}), data={"stars_given":3})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 3)

    def test_put_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.put(
            reverse("api:review-detail", kwargs={"id": br.id}),
            data={"stars_given":3, "comment": "Nice book", "user_id":self.user.id, "book_id":book.id})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, "Nice book")

    def test_create_review(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        data = {
            "stars_given":2,
            "comment":"Ok",
            "user_id":self.user.id,
            "book_id":book.id
        }
        response = self.client.post(reverse("api:review-list"), data=data)
        br = BookReview.objects.get(book = book)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 2),
        self.assertEqual(br.comment, "Ok")