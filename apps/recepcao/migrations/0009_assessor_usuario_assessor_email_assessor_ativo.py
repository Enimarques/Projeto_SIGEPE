# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recepcao', '0008_assessor'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessor',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assessor', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AddField(
            model_name='assessor',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='assessor',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]