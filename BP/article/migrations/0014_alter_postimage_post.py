# Generated by Django 3.2 on 2022-12-13 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_rename_post_id_postimage_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='Post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.post'),
        ),
    ]
