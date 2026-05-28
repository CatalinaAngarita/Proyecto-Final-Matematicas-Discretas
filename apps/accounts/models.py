from django.db import models
from django.contrib.auth.models import User
from apps.core.models import BaseModel


class UserProfile(BaseModel):
    """
    Perfil extendido del usuario del sistema.
    Django ya tiene auth.User con username, email, password, etc.
    Acá agregamos los campos específicos del negocio.

    Relación: OneToOneField con User
    - Un usuario TIENE UN perfil
    - Un perfil PERTENECE A un usuario
    - on_delete=CASCADE: si se elimina el User, se elimina su perfil
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    phone = models.CharField(
        'Teléfono',
        max_length=20,
        blank=True,
        help_text='Número de contacto del administrador'
    )
    avatar = models.ImageField(
        'Foto de perfil',
        upload_to='avatars/',
        blank=True
    )

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'
