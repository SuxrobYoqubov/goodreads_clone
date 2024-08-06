from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"suxrob",
                "first_name":"Suxrob",
                "last_name":"Yoqubov",
                "email":"yoqubovsuxrob1999@gmail.com",
                "password":"somepassword",

            }
        )

        user = CustomUser.objects.get(username = "suxrob")

        self.assertEqual(user.first_name, "Suxrob")
        self.assertEqual(user.last_name, "Yoqubov")
        self.assertEqual(user.email, "yoqubovsuxrob1999@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data = {
                'first_name':"Suxrob",
                'email' : "yoqubovsuxrob1999@gmail.com",
            }
        )

        CustomUser_count = CustomUser.objects.count()

        self.assertEqual(CustomUser_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "CustomUsername": "suxrob",
                "first_name": "Suxrob",
                "last_name": "Yoqubov",
                "email": "invalid-email",
                "password": "somepassword",

            }
        )
        CustomUser_count = CustomUser.objects.count()

        self.assertEqual(CustomUser_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_CustomUsername(self):
        # 1. create a CustomUser
        user = CustomUser.objects.create(username = "suxrob", first_name = "Suxrob")
        user.set_password("somepass")
        user.save()
        # 2. try to create another CustomUser with that same CustomUsername
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "suxrob",
                "first_name": "Suxrob",
                "last_name": "Yoqubov",
                "email": "invalid-email",
                "password": "somepassword",

            }
        )
        # 3. check that the second CustomUser was not created
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response, 'form', 'username', "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_CustomUser = CustomUser.objects.create(username="suxrob", first_name="Suxrob")
        self.db_CustomUser.set_password("somepass")
        self.db_CustomUser.save()

    def test_successful_login(self):

        self.client.post(
            reverse("users:login"),
            data = {
                "username": "suxrob",
                "password": "somepass"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_username",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username = 'suxrob', password = "somepass")
        self.client.get(reverse("users:logout"))
        CustomUser = get_user(self.client)
        self.assertFalse(CustomUser.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login")+"?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username = "suxrob", first_name = "Alibek", last_name = 'Yoqubov', email = 'suxrob@gmail.com'
        )
        user.set_password('admin2')
        user.save()

        self.client.login(username = 'suxrob', password = 'admin2')

        response = self.client.get(reverse("users:profile"))


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_profile_update(self):
        user = CustomUser.objects.create(
            username="suxrob", first_name="Alibek", last_name='Yoqubov', email='suxrob@gmail.com'
        )
        user.set_password('admin2')
        user.save()

        self.client.login(username='suxrob', password='admin2')

        response= self.client.post(
            reverse("users:profile-edit"),
            data = {
                "username":"Suxrob",
                "first_name":"Suxrob",
                "last_name":"Yoqubov",
                "email":"Suxrob@gmail.com"
            }
        )

        user.refresh_from_db() #ikkala kod bir xil vazifa bajaradi  user = CustomUser.objects.get(pk=CustomUser.pk)

        self.assertEqual(user.username, "Suxrob")
        self.assertEqual(user.last_name, "Yoqubov")
        self.assertEqual(response.url, reverse("users:profile"))