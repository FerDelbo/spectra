from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
            
        # Busca o usuário pelo Username OU pelo E-mail
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        
        # Se achou o usuário e a senha estiver correta, autoriza
        if user and user.check_password(password):
            return user
        return None