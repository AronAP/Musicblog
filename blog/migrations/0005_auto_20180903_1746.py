# Generated by Django 2.1 on 2018-09-03 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='post',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.User'),
        ),
    ]
