# Generated by Django 4.1.7 on 2023-03-23 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leadconversion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='leadconversion.userrole'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='leadconversion.userrole'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(choices=[('lead-creator', 'Lead Creator'), ('customer-creator', 'Customer Creator')], max_length=255),
        ),
    ]
