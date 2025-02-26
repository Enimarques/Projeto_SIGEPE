# Generated by Django 5.1.6 on 2025-02-25 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_localizacao_setor_localização_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='username',
            new_name='usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AddField(
            model_name='usuario',
            name='senha',
            field=models.CharField(default='cmp@2025', max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('ADMIN', 'Administrador'), ('RECEP', 'Recepcionista')], default='RECEP', max_length=10),
        ),
    ]
