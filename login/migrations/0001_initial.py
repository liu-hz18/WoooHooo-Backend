# Generated by Django 3.1.2 on 2020-11-11 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('pwhash', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('mail', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=30, unique=True)),
                ('user', models.ManyToManyField(to='login.User')),
            ],
        ),
        migrations.CreateModel(
            name='BrowseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=500)),
                ('imgurl', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=100)),
                ('browse_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
        ),
    ]