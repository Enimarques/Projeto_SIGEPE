"""
Serviço para autenticação e verificação de permissões.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.utils import timezone

class AuthenticationService:
    """
    Serviço para autenticação de usuários e verificação de permissões.
    Centraliza a lógica de autenticação separada das views.
    """
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica um usuário com base no nome de usuário e senha.
        
        Args:
            username (str): Nome de usuário
            password (str): Senha do usuário
            
        Returns:
            User: Objeto de usuário autenticado ou None se a autenticação falhar
        """
        return authenticate(username=username, password=password)
    
    @staticmethod
    def is_admin(user):
        """
        Verifica se o usuário é um administrador.
        
        Args:
            user (User): Objeto de usuário para verificar
            
        Returns:
            bool: True se o usuário é administrador, False caso contrário
        """
        return user.is_superuser or user.groups.filter(name='Administradores').exists()
    
    @staticmethod
    def is_assessor(user):
        """
        Verifica se o usuário é um assessor ativo.
        
        Args:
            user (User): Objeto de usuário para verificar
            
        Returns:
            bool: True se o usuário é um assessor ativo, False caso contrário
        """
        try:
            return hasattr(user, 'assessor') and user.assessor.ativo
        except:
            return False
    
    @staticmethod
    def get_assessor_departamento(user):
        """
        Obtém o departamento de um usuário assessor.
        
        Args:
            user (User): Objeto de usuário assessor
            
        Returns:
            Setor: Objeto de departamento ou None se o usuário não for assessor
        """
        try:
            if hasattr(user, 'assessor') and user.assessor.departamento:
                return user.assessor.departamento
            return None
        except:
            return None
    
    @staticmethod
    def assessor_can_access_gabinete(user, gabinete_id):
        """
        Verifica se um assessor pode acessar um determinado gabinete.
        
        Args:
            user (User): Objeto de usuário assessor
            gabinete_id (int): ID do gabinete a ser verificado
            
        Returns:
            bool: True se o assessor pode acessar o gabinete, False caso contrário
        """
        try:
            if not AuthenticationService.is_assessor(user):
                return False
                
            return int(gabinete_id) == user.assessor.departamento.id
        except:
            return False
    
    @staticmethod
    def update_last_login(user):
        """
        Atualiza o timestamp do último login do usuário.
        
        Args:
            user (User): Objeto de usuário para atualizar
        """
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
    @staticmethod
    def get_user_permissions(user):
        """
        Obtém uma lista de permissões do usuário com base no seu tipo.
        
        Args:
            user (User): Objeto de usuário
            
        Returns:
            dict: Dicionário de permissões do usuário
        """
        permissions = {
            'can_manage_users': False,
            'can_view_reports': False,
            'can_manage_departamentos': False,
            'can_manage_visitors': False,
            'can_manage_vehicles': False,
        }
        
        # Administradores têm todas as permissões
        if AuthenticationService.is_admin(user):
            return {k: True for k in permissions}
            
        # Assessores têm permissões limitadas
        if AuthenticationService.is_assessor(user):
            permissions['can_view_reports'] = True
            permissions['can_manage_visitors'] = True
            
        return permissions 

    @staticmethod
    def is_recepcionista(user):
        """
        Verifica se o usuário pertence ao grupo Recepcionista.
        """
        return user.groups.filter(name='Recepcionista').exists() 