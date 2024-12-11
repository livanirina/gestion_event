from django.shortcuts import render, get_object_or_404, redirect
from .models import Evenement, Reservation, Commentaire
from .forms import InscriptionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .forms import EvenementForm

def liste_evenements(request):
    evenements = Evenement.objects.all()
    return render(request, 'evenements/liste_evenements.html', {'evenements': evenements})

from django.contrib import messages  # Pour gérer les messages flash

def evenement_detail(request, evenement_id):
    evenement = get_object_or_404(Evenement, pk=evenement_id)
    commentaires = Commentaire.objects.filter(evenement=evenement).order_by('-date_creation')

    if request.method == 'POST':
        if request.user.is_authenticated:
            contenu = request.POST.get('contenu', '').strip()
            if contenu:
                commentaire = Commentaire(
                    contenu=contenu,
                    evenement=evenement,
                    utilisateur=request.user
                )
                commentaire.save()
                messages.success(request, "Commentaire ajouté avec succès.")
                return redirect('evenement_detail', evenement_id=evenement.id)
            else:
                messages.error(request, "Le commentaire ne peut pas être vide.")
        else:
            return redirect('connexion')

    return render(request, 'evenements/evenement_detail.html', {
        'evenement': evenement,
        'commentaires': commentaires
    })


def reserver_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, pk=evenement_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            reservation = Reservation(
                evenement=evenement,
                utilisateur=request.user,
                nom=request.POST['nom'],
                telephone=request.POST['telephone'],
                email=request.POST['email'],
                mode_payment=request.POST['mode_payment']
            )
            reservation.save()
            return render(request, 'evenements/facture.html', {'reservation': reservation})
        else:
            return redirect('connexion')
    return render(request, 'evenements/reserver_evenement.html', {'evenement': evenement})

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'evenements/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('liste_evenements')
    return render(request, 'evenements/connexion.html')
from django.contrib.auth import logout

def deconnexion(request):
    logout(request)
    return redirect('connexion')

# Vérification si l'utilisateur est super-utilisateur
def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def admin_dashboard(request):
    evenements = Evenement.objects.all()
    reservations = Reservation.objects.all()
    return render(request, 'admin/dashboard.html', {
        'evenements': evenements,
        'reservations': reservations
    })

@user_passes_test(superuser_required)
def ajouter_evenement(request):
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Événement ajouté avec succès!"}, status=200)
        return JsonResponse({"errors": form.errors}, status=400)

@user_passes_test(superuser_required)
def modifier_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES, instance=evenement)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Événement modifié avec succès!"}, status=200)
        return JsonResponse({"errors": form.errors}, status=400)

@user_passes_test(superuser_required)
def supprimer_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    evenement.delete()
    return JsonResponse({"message": "Événement supprimé avec succès!"}, status=200)
