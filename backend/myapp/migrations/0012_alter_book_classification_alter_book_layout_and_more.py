# Generated by Django 4.1.4 on 2023-01-02 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_book_tag_book_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classification_book', to='myapp.classification'),
        ),
        migrations.AlterField(
            model_name='book',
            name='layout',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='tag_book', to='myapp.tag'),
        ),
    ]