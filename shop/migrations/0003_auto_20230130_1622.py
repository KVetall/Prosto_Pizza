# Generated by Django 3.1.7 on 2023-01-30 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.discount', verbose_name='Скидка'),
        ),
    ]
