# Generated by Django 5.0.4 on 2024-05-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='static_files/images/student_image.jpeg', upload_to='images/user_profile_Pic'),
        ),
    ]
