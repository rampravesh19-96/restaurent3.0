# Generated by Django 4.0.5 on 2022-07-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_rename_product_quantity_cart_product_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_list',
            field=models.TextField(),
        ),
    ]
