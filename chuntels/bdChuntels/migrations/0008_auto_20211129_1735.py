# Generated by Django 3.2.7 on 2021-11-29 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdChuntels', '0007_comentsworks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AlterField(
            model_name='message',
            name='state',
            field=models.CharField(default='1', max_length=1),
        ),
        migrations.DeleteModel(
            name='stateMessage',
        ),
    ]
