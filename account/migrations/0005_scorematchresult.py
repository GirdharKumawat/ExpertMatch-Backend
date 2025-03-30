# Generated by Django 5.1.5 on 2025-03-30 06:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreMatchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_score', models.FloatField()),
                ('skills_score', models.FloatField()),
                ('experience_score', models.FloatField()),
                ('project_score', models.FloatField()),
                ('total_score', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_results', to=settings.AUTH_USER_MODEL)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expert_scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('candidate', 'expert')},
            },
        ),
    ]
