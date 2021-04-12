# Generated by Django 3.1.7 on 2021-04-08 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20210407_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brokermodel',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='broker', to='game.playermodel'),
        ),
        migrations.AlterField(
            model_name='producermodel',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='game.playermodel'),
        ),
        migrations.AlterField(
            model_name='sessionmodel',
            name='turn_phase',
            field=models.CharField(choices=[('negotiation', 'Этап переговоров'), ('transaction', 'Этап заключения сделок')], default='negotiation', max_length=20),
        ),
    ]