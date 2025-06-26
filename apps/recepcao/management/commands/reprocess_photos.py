from django.core.management.base import BaseCommand
from apps.recepcao.models import Visitante
from apps.recepcao.utils.image_utils import process_image
from django.core.cache import cache
import os

class Command(BaseCommand):
    help = 'Reprocessa todas as fotos dos visitantes'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando reprocessamento de fotos...')
        
        visitantes = Visitante.objects.filter(foto__isnull=False)
        total = visitantes.count()
        processados = 0
        erros = 0
        
        for visitante in visitantes:
            try:
                self.stdout.write(f'Processando visitante: {visitante.nome_completo} (ID: {visitante.id})')
                
                # Verificar se a foto original existe
                if not os.path.exists(visitante.foto.path):
                    self.stdout.write(self.style.WARNING(f'  Foto original não encontrada: {visitante.foto.path}'))
                    continue
                
                # Processar a imagem
                processed_images = process_image(visitante.foto)
                
                # Salvar as versões processadas
                if 'thumbnail' in processed_images:
                    visitante.foto_thumbnail.save(
                        processed_images['thumbnail'].name, 
                        processed_images['thumbnail'], 
                        save=False
                    )
                
                if 'medium' in processed_images:
                    visitante.foto_medium.save(
                        processed_images['medium'].name, 
                        processed_images['medium'], 
                        save=False
                    )
                
                if 'large' in processed_images:
                    visitante.foto_large.save(
                        processed_images['large'].name, 
                        processed_images['large'], 
                        save=False
                    )
                
                # Salvar o visitante
                visitante.save()
                
                # Limpar cache
                for size in ['thumbnail', 'medium', 'large']:
                    cache_key = f'visitante_foto_{visitante.id}_{size}'
                    cache.delete(cache_key)
                
                processados += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Processado com sucesso'))
                
            except Exception as e:
                erros += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Erro: {str(e)}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Total de visitantes: {total}')
        self.stdout.write(f'Processados com sucesso: {processados}')
        self.stdout.write(f'Erros: {erros}')
        self.stdout.write('Reprocessamento concluído!') 