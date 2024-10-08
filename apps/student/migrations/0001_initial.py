# Generated by Django 4.0.5 on 2024-08-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestResponseLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=100)),
                ('request_body', models.TextField(blank=True, null=True)),
                ('response_body', models.TextField(blank=True, null=True)),
                ('status_code', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('enrollment_date', models.DateField()),
                ('father_name', models.CharField(max_length=40)),
                ('mother_name', models.CharField(max_length=40)),
            ],
        ),
    ]
