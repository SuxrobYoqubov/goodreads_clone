from django import forms
from django.core.mail import send_mail

from users.models import CustomUser


class CustomUserCreateForm(forms.ModelForm):
    # qisqa kod yozilgan usuli

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # email jo'natish------------------------------------
        # if user.email:
        #     send_mail(
        #         "Welcome to Goodreads Clone",
        #         f"Hi, {user.username}. Welcome to Goodreads clone. Enjoy the books and reviews.",
        #         "yoqubovasevinch2005@gmail.com",
        #         [user.email],
        #
        #     )
        # ------------------


        return user

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', "profile_picture")





# class CustomUserLoginForm(forms.Form):
#     CustomUsername = forms.CharField(max_length=150)
#     password = forms.CharField(max_length=128)
#
#     def clean(self):
#         CustomUsername = self.cleaned_data['CustomUsername']
#         password = self.cleaned_data['password']




    # Qo'lda yozilgan usuli

    # CustomUsername = forms.CharField(max_length=150)
    # email = forms.EmailField()
    # first_name = forms.CharField(max_length=150)
    # last_name = forms.CharField(max_length=150)
    # password = forms.CharField(max_length=128)
    #
    # def save(self):
    #     CustomUsername = self.cleaned_data.POST['CustomUsername']
    #     first_name = self.cleaned_data.POST['first_name']
    #     last_name = self.cleaned_data.POST['last_name']
    #     email = self.cleaned_data.POST['email']
    #     password = self.cleaned_data.POST['password']
    #
    #     CustomUser = CustomUser.objects.create(
    #         CustomUsername=CustomUsername,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email,
    #     )
    #
    #     # passwordni hash kurinishini o'zgartirib beradi
    #     CustomUser.set_password(password)
    #
    #     CustomUser.save()
    #
    #     return CustomUser