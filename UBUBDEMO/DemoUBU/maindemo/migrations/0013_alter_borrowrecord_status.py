# Generated by Django 4.1.13 on 2024-02-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindemo', '0012_alter_borrowrecord_borrower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrecord',
            name='status',
            field=models.CharField(choices=[('waiting', 'รออนุมัติ'), ('borrowing', 'กำลังยืม'), ('returned', 'คืนแล้ว')], default='pending', max_length=10, verbose_name='สถานะ'),
        ),
    ]
