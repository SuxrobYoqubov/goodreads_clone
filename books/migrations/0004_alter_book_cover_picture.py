# Generated by Django 4.2.14 on 2024-07-19 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='default_cover.jpg', upload_to=''),
        ),
    ]
