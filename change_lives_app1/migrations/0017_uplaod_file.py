# Generated by Django 4.1.5 on 2023-03-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_lives_app1', '0016_remove_registration_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='uplaod_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdfs/')),
            ],
        ),
    ]
