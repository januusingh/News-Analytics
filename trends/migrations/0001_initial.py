# Generated by Django 2.0.6 on 2018-07-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.TextField()),
                ('author', models.TextField()),
                ('website', models.TextField()),
                ('published', models.DateTimeField()),
                ('topics', models.TextField()),
            ],
        ),
    ]
