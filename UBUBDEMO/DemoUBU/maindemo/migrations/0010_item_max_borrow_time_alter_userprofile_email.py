# Generated by Django 4.1.13 on 2024-02-09 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindemo', '0009_alter_item_created_at_alter_item_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='max_borrow_time',
            field=models.PositiveIntegerField(default=60, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='user@ubu.ac.th', max_length=50, null=True),
        ),
    ]
