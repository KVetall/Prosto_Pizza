# Generated by Django 4.1.7 on 2023-02-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20230218_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('name', models.CharField(max_length=70, verbose_name='Имя')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('date_review', models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-date_review'],
            },
        ),
    ]