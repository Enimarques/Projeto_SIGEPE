"""
Serviço para gerenciamento de usuários.
"""
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..forms.user_forms import UserProfileForm, UsuarioForm
from apps.recepcao.models import Assessor

class Result:
    """Classe para representar o resultado de uma operação."""
    
    def __init__(self, success=True, message="", data=None):
        self.success = success
        self.message = message
        self.data = data or {}

class UserService:
    """
    Serviço para gerenciamento de usuários.
    Centraliza a lógica de negócio relacionada a usuários.
    """
    
    @staticmethod
    def get_all_users():
        """
        Obtém todos os usuários ordenados por nome de usuário.
        
        Returns:
            QuerySet: QuerySet com todos os usuários ordenados
        """
        return User.objects.all().order_by('username')
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtém um usuário pelo ID.
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            User: Objeto de usuário ou 404 se não encontrado
        """
        return get_object_or_404(User, pk=user_id)
    
    @staticmethod
    def get_user_form(user=None, data=None):
        """
        Obtém um formulário de usuário.
        
        Args:
            user (User, optional): Usuário para edição. Defaults to None.
            data (dict, optional): Dados para o formulário. Defaults to None.
            
        Returns:
            UsuarioForm: Formulário de usuário
        """
        if data:
            if user:
                return UsuarioForm(data, instance=user)
            return UsuarioForm(data)
        if user:
            return UsuarioForm(instance=user)
        return UsuarioForm()
    
    @staticmethod
    def create_user(form_data):
        """
        Cria um novo usuário com base nos dados do formulário.
        
        Args:
            form_data (dict): Dados do formulário
            
        Returns:
            Result: Resultado da operação com sucesso e mensagem
        """
        form = UsuarioForm(form_data)
        
        if not form.is_valid():
            return Result(False, "Dados inválidos para criação do usuário", {'form': form})
            
        try:
            with transaction.atomic():
                user = form.save()
                return Result(True, "Usuário criado com sucesso", {'user': user})
        except Exception as e:
            return Result(False, f"Erro ao criar usuário: {str(e)}")
    
    @staticmethod
    def update_user(user_id, form_data):
        """
        Atualiza um usuário existente.
        
        Args:
            user_id (int): ID do usuário a ser atualizado
            form_data (dict): Dados do formulário
            
        Returns:
            Result: Resultado da operação com sucesso e mensagem
        """
        user = UserService.get_user_by_id(user_id)
        form = UsuarioForm(form_data, instance=user)
        
        if not form.is_valid():
            return Result(False, "Dados inválidos para atualização do usuário", {'form': form})
            
        try:
            with transaction.atomic():
                user = form.save()
                return Result(True, "Usuário atualizado com sucesso", {'user': user})
        except Exception as e:
            return Result(False, f"Erro ao atualizar usuário: {str(e)}")
    
    @staticmethod
    def delete_user(user_id):
        """
        Exclui um usuário.
        
        Args:
            user_id (int): ID do usuário a ser excluído
            
        Returns:
            Result: Resultado da operação com sucesso e mensagem
        """
        user = UserService.get_user_by_id(user_id)
        
        try:
            # Desvincular assessor se existir
            try:
                if hasattr(user, 'assessor'):
                    assessor = user.assessor
                    assessor.usuario = None
                    assessor.save()
            except:
                pass
                
            username = user.username
            user.delete()
            return Result(True, f"Usuário {username} excluído com sucesso")
        except Exception as e:
            return Result(False, f"Erro ao excluir usuário: {str(e)}")
    
    @staticmethod
    def get_available_assessores():
        """
        Obtém assessores disponíveis para vinculação com usuários.
        
        Returns:
            QuerySet: QuerySet com assessores disponíveis
        """
        return Assessor.objects.filter(usuario__isnull=True, ativo=True)
    
    @staticmethod
    def get_user_profile_form(user, data=None):
        """
        Obtém o formulário de perfil do usuário.
        
        Args:
            user (User): Usuário para obter o formulário de perfil
            data (dict, optional): Dados para o formulário. Defaults to None.
            
        Returns:
            UserProfileForm: Formulário de perfil do usuário
        """
        if data:
            return UserProfileForm(data, instance=user)
        return UserProfileForm(instance=user)
    
    @staticmethod
    def update_user_profile(user, form_data):
        """
        Atualiza o perfil do usuário.
        
        Args:
            user (User): Usuário para atualizar o perfil
            form_data (dict): Dados do formulário
            
        Returns:
            Result: Resultado da operação com sucesso e mensagem
        """
        form = UserProfileForm(form_data, instance=user)
        
        if not form.is_valid():
            return Result(False, "Dados inválidos para atualização do perfil", {'form': form})
            
        try:
            user = form.save()
            return Result(True, "Perfil atualizado com sucesso", {'user': user})
        except Exception as e:
            return Result(False, f"Erro ao atualizar perfil: {str(e)}") 