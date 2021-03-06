# Generated by Django 3.1.4 on 2021-01-07 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('card_image', models.ImageField(upload_to='cardimages')),
                ('explanation', models.CharField(max_length=1000)),
                ('inverted_explanation', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('explanation', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tarotuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=500)),
                ('profile_image', models.ImageField(upload_to='profileimages')),
                ('card_of_day_inverted', models.BooleanField()),
                ('astrology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arcanaapi.sign')),
                ('card_of_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_of_day', to='arcanaapi.card')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='arcanaapi.tarotuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='arcanaapi.tarotuser')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=50)),
                ('shared', models.BooleanField(default=False)),
                ('notes', models.CharField(max_length=2000)),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arcanaapi.layout')),
                ('tarotuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='arcanaapi.tarotuser')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('explanation', models.CharField(max_length=1000)),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arcanaapi.layout')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.CharField(max_length=2000)),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='arcanaapi.reading')),
                ('tarotuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarotuser', to='arcanaapi.tarotuser')),
            ],
        ),
        migrations.CreateModel(
            name='Cardreading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inverted', models.BooleanField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cardreadings', to='arcanaapi.card')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arcanaapi.position')),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cardreadings', to='arcanaapi.reading')),
            ],
        ),
    ]
