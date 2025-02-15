# Generated by Django 5.1.4 on 2025-01-06 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_alter_entry_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='charge',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='condition',
            field=models.PositiveSmallIntegerField(choices=[(0, 'N/A'), (3, 'Good'), (2, 'Fair'), (1, 'Poor')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='memo',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='ready',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='rint',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True),
        ),
    ]
