# Generated by Django 4.1.4 on 2022-12-31 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]