# Generated by Django 4.1.5 on 2023-03-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_columnitem_csvfile_remove_schema_data_types_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('link', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CsvFile',
        ),
    ]
