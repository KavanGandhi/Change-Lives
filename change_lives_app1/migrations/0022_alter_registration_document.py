# Generated by Django 4.1.5 on 2023-03-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_lives_app1', '0021_alter_registration_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='document',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
