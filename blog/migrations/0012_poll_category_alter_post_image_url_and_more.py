# Generated by Django 4.2.11 on 2024-03-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_poll_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='category',
            field=models.CharField(choices=[('gaming', 'Gaming'), ('film', 'Film'), ('books', 'Books')], default='gaming', max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='vote',
            name='thumbs_up',
            field=models.BooleanField(default=False),
        ),
    ]