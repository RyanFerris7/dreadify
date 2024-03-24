# Generated by Django 4.2.11 on 2024-03-22 17:18

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comments_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='comments',
            name='content',
            field=django_quill.fields.QuillField(max_length=250),
        ),
    ]