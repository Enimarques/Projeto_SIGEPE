# Generated by Django 5.1.6 on 2025-03-06 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_visita_data_saida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_visitante/'),
        ),
    ]
