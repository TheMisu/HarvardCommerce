# Generated by Django 4.2.5 on 2023-09-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid_comment_rename_price_listing_starting_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
