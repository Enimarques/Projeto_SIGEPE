from django.db import migrations

def clean_visitas_sem_visitante(apps, schema_editor):
    Visita = apps.get_model('main', 'Visita')
    # Atualiza o status de visitas sem visitante para cancelada
    Visita.objects.filter(visitante__isnull=True).update(status='cancelada')

def reverse_clean_visitas(apps, schema_editor):
    # Não precisa fazer nada na reversão
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clean_visitas_sem_visitante, reverse_clean_visitas),
    ]
