# Generated by Django 4.2.1 on 2023-07-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_remove_balance_document_remove_documents_contract_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='documents_approve',
            field=models.BooleanField(default=False, verbose_name='KYC верификация'),
        ),
    ]
