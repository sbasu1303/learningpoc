# Generated by Django 3.1.5 on 2021-01-15 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(db_index=True, max_length=254)),
                ('courseDescription', models.TextField(db_index=True, verbose_name='Course Description')),
                ('contentHash', models.CharField(max_length=128)),
                ('courseS3Key', models.CharField(max_length=254)),
                ('approvedAt', models.DateTimeField(blank=True, null=True, verbose_name='Course approval date time')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('UNDER_REVIEW', 'Under Review'), ('CREATED', 'Created'), ('REJECTED', 'Rejected'), ('DELETED', 'Deleted')], max_length=50)),
                ('quiz', models.JSONField(verbose_name='Quiz content with multi-choice with answers')),
                ('adminApprover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver', to='user_management.lappuser')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='user_management.lappuser')),
            ],
        ),
    ]
