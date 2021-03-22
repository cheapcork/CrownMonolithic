# Generated by Django 3.1.7 on 2021-03-18 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20210317_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermodel',
            name='session',
        ),
        migrations.AddField(
            model_name='brokermodel',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker', to='game.sessionmodel', verbose_name='Сессия'),
        ),
        migrations.AddField(
            model_name='producermodel',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='game.sessionmodel', verbose_name='Сессия'),
        ),
        migrations.AlterField(
            model_name='brokermodel',
            name='player',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'broker'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker', to='game.playermodel'),
        ),
        migrations.AlterField(
            model_name='producermodel',
            name='player',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'producer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='game.playermodel'),
        ),
        migrations.AlterField(
            model_name='sessionmodel',
            name='crown_balance',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]