# Generated by Django 4.2.13 on 2024-06-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wanbuffer_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(default='azad', max_length=120),
            preserve_default=False,
        ),
    ]
