# Generated by Django 5.0.4 on 2024-04-11 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_date_orderd_order_dateorderd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.png', null=True, upload_to=''),
        ),
    ]
