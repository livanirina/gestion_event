from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    is_admin = models.BooleanField(default=False)  # Champ personnalisé
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='evenements_utilisateur_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='evenements_utilisateur_permissions_set',
        blank=True
    )

class Evenement(models.Model):
    titre = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/evenements/', blank=True)
    description = models.TextField()
    lieu = models.CharField(max_length=255)
    date = models.DateTimeField()
    capacite = models.IntegerField()
    programme = models.TextField()

    def __str__(self):
        return self.titre

class Reservation(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('airtel', 'Airtel'),
        ('orange', 'Orange'),
        ('yas', 'Yas'),
    ]

    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    mode_payment = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)

    def __str__(self):
        return f"{self.nom} - {self.evenement.titre}"

class Commentaire(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur} sur {self.evenement.titre}"
