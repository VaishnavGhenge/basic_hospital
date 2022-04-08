# Generated by Django 4.0.3 on 2022-04-06 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.TextField()),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('pincode', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('profilepic', models.ImageField(default='user/default.png', upload_to='user/patient/profile/')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginapp.address')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('profilepic', models.ImageField(default='user/defualt.png', upload_to='user/doctor/profile/')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginapp.address')),
            ],
        ),
    ]