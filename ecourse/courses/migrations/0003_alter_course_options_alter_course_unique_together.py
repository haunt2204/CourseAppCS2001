# Generated by Django 5.0.3 on 2024-03-17 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_tag_alter_course_description_lesson_course_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('subject', 'category')},
        ),
    ]
