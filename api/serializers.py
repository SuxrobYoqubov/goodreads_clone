from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "isbn")

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id',"first_name", "last_name", "username", "email")

class BookReviewSerializers(serializers.ModelSerializer):
    book = BookSerializers(read_only=True)
    user = UserSerializers(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ("id", "stars_given", "comment", "book", "user", "user_id", "book_id")
    # stars_given = serializers.IntegerField(min_value=1, max_value=5)
    # comment = serializers.CharField()
