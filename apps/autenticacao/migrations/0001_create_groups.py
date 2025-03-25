from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    # Cria o grupo de Administradores se não existir
    admin_group, created = Group.objects.get_or_create(name='Administradores')
    
    # Garante que o grupo de Assessores existe
    assessor_group, created = Group.objects.get_or_create(name='Assessores')

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]