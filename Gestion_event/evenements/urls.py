from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_evenements, name='liste_evenements'),
    path('evenement/<int:evenement_id>/', views.evenement_detail, name='evenement_detail'),
    path('reserver/<int:evenement_id>/', views.reserver_evenement, name='reserver_evenement'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/ajouter-evenement/', views.ajouter_evenement, name='ajouter_evenement'),
    path('admin/modifier-evenement/<int:evenement_id>/', views.modifier_evenement, name='modifier_evenement'),
    path('admin/supprimer-evenement/<int:evenement_id>/', views.supprimer_evenement, name='supprimer_evenement'),
    
]
