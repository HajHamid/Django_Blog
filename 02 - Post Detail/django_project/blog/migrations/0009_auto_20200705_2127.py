# Generated by Django 3.0.8 on 2020-07-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('info', 'تالیفی'), ('success', 'ترجمه ای'), ('warning', 'کاربران')], default='info', max_length=20),
        ),
    ]
