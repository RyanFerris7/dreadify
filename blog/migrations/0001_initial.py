# Generated by Django 4.2.11 on 2024-03-20 16:13

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('excerpt', models.TextField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('category', models.CharField(choices=[('gaming', 'Gaming'), ('film', 'Film'), ('books', 'Books')], default='gaming', max_length=250)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish')], default='publish', max_length=10)),
                ('article_image_url', models.URLField()),
                ('article_image', models.ImageField(default=blog.models.Default_Image, null=True, upload_to='article_images')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('category', models.CharField(choices=[('gaming', 'Gaming'), ('film', 'Film'), ('books', 'Books')], default='gaming', max_length=250)),
                ('thumbs_up_count', models.IntegerField(default=0)),
                ('thumbs_down_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuillPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', django_quill.fields.QuillField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbs_up', models.BooleanField(default=False)),
                ('thumbs_down', models.BooleanField(default=False)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('excerpt', models.TextField(max_length=250, null=True)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('category', models.CharField(choices=[('gaming', 'Gaming'), ('film', 'Film'), ('books', 'Books')], default='gaming', max_length=250)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', django_quill.fields.QuillField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish')], default='publish', max_length=10)),
                ('image_url', models.URLField()),
                ('image', models.ImageField(default=blog.models.Default_Image, null=True, upload_to='article_images')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=250)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('article', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'ordering': ('-created', '-updated'),
            },
        ),
    ]
