# Generated by Django 4.2.11 on 2024-03-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_excerpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='article_images'),
        ),
    ]
