# Generated by Django 3.0.3 on 2020-04-22 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matchmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myself', models.TextField(blank=True, max_length=200)),
                ('another_user', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Requestmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_send', models.TextField(blank=True, max_length=200)),
                ('request_message', models.TextField(blank=True, max_length=600)),
                ('who_recive', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.TextField(blank=True, max_length=200)),
                ('keyword_subject', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=200)),
                ('firstname', models.TextField(blank=True, max_length=200)),
                ('lastname', models.TextField(blank=True, max_length=200)),
                ('age', models.TextField(blank=True, max_length=10)),
                ('school', models.TextField(blank=True, max_length=200)),
                ('school_keyword', models.TextField(blank=True, max_length=200)),
                ('gender', models.TextField(blank=True)),
                ('fb_link', models.TextField(null=True)),
                ('match_request', models.IntegerField(default=0)),
                ('message_list', models.IntegerField(default=0)),
                ('birthday', models.DateTimeField(blank=True)),
                ('expertise', models.ManyToManyField(blank=True, related_name='Userinfos', to='tinderforeduapp.Subject')),
                ('match', models.ManyToManyField(blank=True, to='tinderforeduapp.Matchmodel')),
                ('request', models.ManyToManyField(blank=True, to='tinderforeduapp.Requestmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Profilepicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='default.png', upload_to='media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tinderforeduapp.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('college', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('age', models.TextField(blank=True, max_length=10)),
                ('bio', models.TextField()),
                ('birthday', models.DateTimeField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, null=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('star', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tinderforeduapp.UserInfo')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
