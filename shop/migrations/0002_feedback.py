# Generated by Django 3.1.7 on 2023-01-21 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('date_feedback', models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')),
                ('status', models.CharField(choices=[('PR', 'Обработан'), ('NPR', 'Не обработан')], default='NPR', max_length=3, verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['-date_feedback'],
            },
        ),
    ]
