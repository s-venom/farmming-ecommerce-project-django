# Generated by Django 5.0.2 on 2024-03-27 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_product_description_product_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='store.category'),
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
