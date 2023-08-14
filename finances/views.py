from decimal import Decimal
from datetime import date, timedelta, datetime
from .utils import definir_date_fin_pret

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Actionnaire,Depense, Echeancier, Statuts, Utilisateurs, Clients, CompteEpargnes, ComptePrets,TransactionEpargne, TransactionPret, Genres, Matrimoniales, Typeprets, Agent
from .forms import ActionnaireForm,ClientForm, CompteEpargneForm, ComptePretForm, DepenseForm, TransactionEpargneForm, GenreForm, MatrimonialeForm, TransactionPretForm, TypePretForm, TypepretForm, AgentForm
from django.contrib.auth import login , logout , authenticate
from django.views.generic import ListView
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.utils import timezone
import pandas as pd


def menu(request):
    context = {
    }  
    return render(request, 'Pages/Log/menu.html', context)




class CandidateListView(ListView):
    model = Clients
    template_name = 'Pages/Client/liste_candidates.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Clients.objects.filter(nom__icontains=query)
        return Clients.objects.all()

# GENRES--------------------------------------------------------------------------------------------
# Vue pour la liste des genres
@login_required(login_url='/accounts/')
def liste_genres(request):
    genres = Genres.objects.all()
    return render(request, 'Pages/Genre/liste_genres.html', {'genres': genres})

# Vue pour créer un genre
@login_required(login_url='/accounts/')
def creer_genre(request):
    if request.method == 'POST':
        genre_form = GenreForm(request.POST)
        if genre_form.is_valid():
            genre_form.save()
            return redirect('liste_genres')
    else:
        genre_form = GenreForm()
    return render(request, 'Pages/Genre/creer_genre.html', {'genre_form': genre_form})

# Vue pour modifier un genre
def modifier_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    if request.method == 'POST':
        genre_form = GenreForm(request.POST, instance=genre)
        if genre_form.is_valid():
            genre_form.save()
            return redirect('liste_genres')
    else:
        genre_form = GenreForm(instance=genre)
    return render(request, 'Pages/Genre/modifier_genre.html', {'genre_form': genre_form, 'genre': genre})

# Vue pour supprimer un genre
def supprimer_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    if request.method == 'POST':
        genre.delete()
        return redirect('liste_genres')
    return render(request, 'Pages/Genre/supprimer_genre.html', {'genre': genre})

# MATRIMONIALES--------------------------------------------------------------------------------------------
# Vue pour la liste des matrimoniales
def liste_matrimoniales(request):
    matrimoniales = Matrimoniales.objects.all()
    return render(request, 'Pages/Matrimoniale/liste_matrimoniales.html', {'matrimoniales': matrimoniales})

# Vue pour créer une matrimoniale
def creer_matrimoniale(request):
    if request.method == 'POST':
        matrimoniale_form = MatrimonialeForm(request.POST)
        if matrimoniale_form.is_valid():
            matrimoniale_form.save()
            return redirect('liste_matrimoniales')
    else:
        matrimoniale_form = MatrimonialeForm()
    return render(request, 'Pages/Matrimoniale/creer_matrimoniale.html', {'matrimoniale_form': matrimoniale_form})

# Vue pour modifier une matrimoniale
def modifier_matrimoniale(request, pk):
    matrimoniale = get_object_or_404(Matrimoniales, pk=pk)
    if request.method == 'POST':
        matrimoniale_form = MatrimonialeForm(request.POST, instance=matrimoniale)
        if matrimoniale_form.is_valid():
            matrimoniale_form.save()
            return redirect('liste_matrimoniales')
    else:
        matrimoniale_form = MatrimonialeForm(instance=matrimoniale)
    return render(request, 'Pages/Matrimoniale/modifier_matrimoniale.html', {'matrimoniale_form': matrimoniale_form, 'matrimoniale': matrimoniale})

# Vue pour supprimer une matrimoniale
def supprimer_matrimoniale(request, pk):
    matrimoniale = get_object_or_404(Matrimoniales, pk=pk)
    if request.method == 'POST':
        matrimoniale.delete()
        return redirect('liste_matrimoniales')
    return render(request, 'Pages/Matrimoniale/supprimer_matrimoniale.html', {'matrimoniale': matrimoniale})

# TYPEPRETS--------------------------------------------------------------------------------------------
# Vue pour la liste des types de prêts
def liste_typeprets(request):
    typeprets = Typeprets.objects.all()
    return render(request, 'liste_typeprets.html', {'typeprets': typeprets})

# Vue pour créer un type de prêt
def creer_typepret(request):
    if request.method == 'POST':
        typepret_form = TypepretForm(request.POST)
        if typepret_form.is_valid():
            typepret_form.save()
            return redirect('liste_typeprets')
    else:
        typepret_form = TypepretForm()
    return render(request, 'creer_typepret.html', {'typepret_form': typepret_form})

# Vue pour modifier un type de prêt
def modifier_typepret(request, pk):
    typepret = get_object_or_404(Typeprets, pk=pk)
    if request.method == 'POST':
        typepret_form = TypepretForm(request.POST, instance=typepret)
        if typepret_form.is_valid():
            typepret_form.save()
            return redirect('liste_typeprets')
    else:
        typepret_form = TypepretForm(instance=typepret)
    return render(request, 'modifier_typepret.html', {'typepret_form': typepret_form, 'typepret': typepret})

# Vue pour supprimer un type de prêt
def supprimer_typepret(request, pk):
    typepret = get_object_or_404(Typeprets, pk=pk)
    if request.method == 'POST':
        typepret.delete()
        return redirect('liste_typeprets')
    return render(request, 'supprimer_typepret.html', {'typepret': typepret})

# AGENTS--------------------------------------------------------------------------------------------
def liste_agents(request):
    agents = Agent.objects.all()
    return render(request, 'Pages/Agent/liste_agents.html', {'agents': agents})

def ajouter_agent(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        if agent_form.is_valid():
            # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'étudiant
            userna = agent_form.cleaned_data['nom']
            usernam = agent_form.cleaned_data['prenom']
            FString = userna + " " + usernam
            username = FString
            role = "ACADEMIQUE"
            statu = 'NON ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = agent_form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu,username=username,last_name=usernam,first_name=userna, password=encoded_password, email=email,role=role)
            agent = agent_form.save(commit=False)
            agent.user = user
            agent.save()
            return redirect('liste_agents')
    else:
        agent_form = AgentForm()
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})

def modifier_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, instance=agent)
        if agent_form.is_valid():
            agent = agent_form.save()
            return redirect('liste_agents')
    else:
        agent_form = AgentForm(instance=agent)
    return render(request, 'Pages/Agent/modifier_agent.html', {'agent_form': agent_form})

def supprimer_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.user.delete()  # Supprimer l'utilisateur associé
        agent.delete()
        return redirect('liste_agents')
    return render(request, 'Pages/Agent/supprimer_agent.html', {'agent': agent})

# CLIENTS--------------------------------------------------------------------------------------------
# Vue pour la liste des clients
@login_required(login_url='/accounts/')
def liste_clients(request):
    clients = Clients.objects.all()
    return render(request, 'Pages/Client/liste_clients.html', {'clients': clients})

def detail_clients(request, client_id):
    client = Clients.objects.get(pk=client_id)
    comptes_prets = ComptePrets.objects.filter(client=client)
    comptes_epargnes = CompteEpargnes.objects.filter(client=client)
    comptes_epargne = CompteEpargnes.objects.filter(client=client)
    return render(request, 'Pages/Client/detail_clients.html', {'client': client, 'comptes_prets': comptes_prets, 'comptes_epargnes': comptes_epargnes,'comptes_epargne': comptes_epargne})

# Vue pour créer un client et son compte épargne
def creer_client(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)
        if client_form.is_valid():
            statut_actif = Statuts.objects.get(statut='Actif')
            client_form.instance.statut = statut_actif
            client = client_form.save()
            CompteEpargnes.objects.create(client=client,solde=0, numero_compte='EP' + str(client.id), statut=statut_actif)
            return redirect('liste_clients')
    else:
        client_form = ClientForm()
    return render(request, 'Pages/Client/creer_client.html', {'form': client_form})

# Vue pour modifier un client
def modifier_client(request, pk):
    client = get_object_or_404(Clients, pk=pk)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect('liste_clients')
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'modifier_client.html', {'client_form': client_form, 'client': client})

# Vue pour supprimer un client
def supprimer_client(request, pk):
    client = get_object_or_404(Clients, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'supprimer_client.html', {'client': client})



# COMPTEEPARGNE--------------------------------------------------------------------------------------------
# Vue pour la liste des comptes épargne
def liste_comptes_epargne(request):
    comptes_epargne = CompteEpargnes.objects.all()
    return render(request, 'Pages/Compteepargne/liste_comptes_epargne.html', {'comptes_epargne': comptes_epargne})

def detail_compte_epargne(request, compte_epargne_id):
    # Récupérer le compte d'épargne en fonction de l'ID passé en paramètre
    compte_epargne = get_object_or_404(CompteEpargnes, id=compte_epargne_id)

    context = {
        'compte_epargne': compte_epargne,
    }

    return render(request, 'Pages/Compteepargne/detail_compte_epargne.html', context)

# Vue pour créer un compte épargne
def creer_compte_epargne(request):
    if request.method == 'POST':
        compte_epargne_form = CompteEpargneForm(request.POST)
        if compte_epargne_form.is_valid():
            compte_epargne_form.save()
            return redirect('liste_comptes_epargne')
    else:
        compte_epargne_form = CompteEpargneForm()
    return render(request, 'creer_compte_epargne.html', {'compte_epargne_form': compte_epargne_form})

# Vue pour modifier un compte épargne
def modifier_compte_epargne(request, pk):
    compte_epargne = get_object_or_404(CompteEpargnes, pk=pk)
    if request.method == 'POST':
        compte_epargne_form = CompteEpargneForm(request.POST, instance=compte_epargne)
        if compte_epargne_form.is_valid():
            compte_epargne_form.save()
            return redirect('liste_comptes_epargne')
    else:
        compte_epargne_form = CompteEpargneForm(instance=compte_epargne)
    return render(request, 'modifier_compte_epargne.html', {'compte_epargne_form': compte_epargne_form, 'compte_epargne': compte_epargne})

# Vue pour supprimer un compte épargne
def supprimer_compte_epargne(request, pk):
    compte_epargne = get_object_or_404(CompteEpargnes, pk=pk)
    if request.method == 'POST':
        compte_epargne.delete()
        return redirect('liste_comptes_epargne')
    return render(request, 'supprimer_compte_epargne.html', {'compte_epargne': compte_epargne})

# COMPTEPRET--------------------------------------------------------------------------------------------

def liste_comptes_prets(request):
    comptes_prets = ComptePrets.objects.all()
    return render(request, 'Pages/Comptepret/liste_comptes_prets.html', {'comptes_prets': comptes_prets})


def detail_compte_pret(request, compte_pret_id):
    compte_pret = get_object_or_404(ComptePrets, id=compte_pret_id)
    echeanciers = Echeancier.objects.filter(compte_pret=compte_pret)

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Comptepret/detail_compte_pret.html', context)


def modifier_compte_pret(request, pk):
    compte_pret = get_object_or_404(ComptePrets, pk=pk)
    if request.method == 'POST':
        compte_pret_form = ComptePretForm(request.POST, instance=compte_pret)
        if compte_pret_form.is_valid():
            compte_pret = compte_pret_form.save()
            return redirect('liste_comptes_prets')
    else:
        compte_pret_form = ComptePretForm(instance=compte_pret)
    return render(request, 'modifier_compte_pret.html', {'compte_pret_form': compte_pret_form})

def supprimer_compte_pret(request, pk):
    compte_pret = get_object_or_404(ComptePrets, pk=pk)
    if request.method == 'POST':
        compte_pret.delete()
        return redirect('liste_comptes_prets')
    return render(request, 'supprimer_compte_pret.html', {'compte_pret': compte_pret})


def ajouter_compte_pret(request, client_id):
    etud = Clients.objects.filter(id=client_id)
    nombre = ComptePrets.objects.count()
    if request.method == 'POST':
        form = ComptePretForm(request.POST)
        if form.is_valid():
            statut_actif = Statuts.objects.get(statut='Actif')
            form.instance.statut = statut_actif
            compte_pret = form.save(commit=False)
            compte_pret.client_id = client_id  # Associer le compte prêt au client spécifié par l'ID
            compte_pret.date_demande = date.today()
            compte_pret.numero_compte='HP' + str(nombre+1)
            
            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            duree_en_mois = compte_pret.duree_en_mois

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale *Decimal(taux_garantie))+somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets
            compte_pret.save()

            return redirect('liste_comptes_prets')

    else:
        form = ComptePretForm(initial={'client': client_id})

    context = {
        'form': form,
        'client': client_id,  # Passer l'ID du client dans le contexte pour l'utiliser dans le formulaire
        'etud':etud
    }
    return render(request, 'Pages/Comptepret/ajouter_compte_pret.html', context)




@receiver(post_save, sender=ComptePrets)
def create_echeanciers(sender, instance, created, **kwargs):
    if created:
        # Calculer les intérêts en fonction du type de prêt
        somme_initiale = instance.somme_initiale
        taux_interet = instance.taux_interet / 100
        taux_garantie = 15 / 100
        duree_en_mois = instance.duree_en_mois

        if instance.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
            interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
        elif instance.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
            interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
        elif instance.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
            interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
        else:
            interets = 0

        # Calculer le montant de l'échéance en fonction du solde du prêt (somme initiale + intérêts) et de la durée du prêt
        montant_echeance = (somme_initiale + interets) / duree_en_mois
        montant_interet = (interets) / duree_en_mois

        instance.solde = somme_initiale + interets
        instance.save()

        # Calculer la date de la première échéance (un mois après la date de début du prêt)
        date_echeance = instance.date_debut_pret + relativedelta(months=1)
        
        # Tant que la date d'échéance est antérieure à la date de fin du prêt, créer une échéance pour chaque mois
        while date_echeance <= instance.date_fin_pret:
            # Créer une échéance pour le mois en cours
            echeance = Echeancier.objects.create(
                compte_pret=instance,
                date_echeance=date_echeance,
                montant_echeance=montant_echeance,
                montant_interet=montant_interet
            )
            
            # Ajouter un mois à la date d'échéance pour passer au mois suivant
            date_echeance += relativedelta(months=1)

def clients_proche_echeance(request):
    date_actuelle = date.today()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=7)

    clients_proche_echeance = Echeancier.objects.filter(date_echeance__gte=date_actuelle, date_echeance__lte=date_une_semaine_plus_tard,est_paye=False).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'id'
    )

    context = {
        'clients': clients_proche_echeance
    }

    return render(request, 'Pages/Comptepret/listeecheance.html', context)

def liste_echeances_non_payees(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)

    context = {
        'echeances_non_payees': echeances_non_payees
    }

    return render(request, 'Pages/Comptepret/listeecheancenon.html', context)

def modifier_est_paye(request, actionnaire_id):
    echance = Echeancier.objects.get(pk=actionnaire_id)
    echance.est_paye = 1
    echance.save()

    # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

    transaction_pret = TransactionPret.objects.create(
        compte_pret=echance.compte_pret,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pret
    dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
    return redirect('clients_proche_echeance')

def modifier_est_payere(request, actionnaire_id):
    echance = Echeancier.objects.get(pk=actionnaire_id)
    echance.est_paye = 1
    echance.save()

    # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

    transaction_pret = TransactionPret.objects.create(
        compte_pret=echance.compte_pret,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pret
    dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
    return redirect('liste_echeances_non_payees')

# TRANSACTIONS--------------------------------------------------------------------------------------------
# Vue pour la liste des transactions
def liste_transactions(request):
    transactions = TransactionEpargne.objects.all()
    return render(request, 'Pages/Transactionepargne/liste_transactions.html', {'transactions': transactions})

# Vue pour créer une transaction d'épargne
def creer_transaction_epargne(request,id):
    if request.method == 'POST':
        transaction_form = TransactionEpargneForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions d'épargne
            # Vérifier si l'utilisateur est un agent avant de l'attribuer à la transaction
            if request.user.is_authenticated and isinstance(request.user, Agent):
                transaction.agent = request.user

            montant = transaction.montant
            if transaction.type_transaction == 'Depot':
                transaction.compte_epargne.solde += montant
            elif transaction.type_transaction == 'Retrait':
                transaction.compte_epargne.solde -= montant
            transaction.compte_epargne.save()
            transaction.save()
            return redirect('liste_transactions')
    else:
        transaction_form = TransactionEpargneForm(initial={'compte_epargne': id})
    context = {
        'transaction_form': transaction_form,
        'id': id,
    }

    return render(request, 'Pages/Transactionepargne/creer_transaction_epargne.html', context)

# Vue pour créer une transaction de prêt
def creer_transaction_pret(request,id):
    if request.method == 'POST':
        transaction_form = TransactionPretForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions de prêt
            montant = transaction.montant
            if transaction.type_transaction == 'Depot':
                transaction.compte_pret.solde += montant
            elif transaction.type_transaction == 'Retrait':
                transaction.compte_pret.solde -= montant
            transaction.compte_pret.save()
            transaction.save()
            return redirect('liste_transactions')
    else:
        transaction_form = TransactionPretForm(initial={'compte_epargne': id})

    context = {
        'transaction_form': transaction_form,
        'id': id,
    }

    return render(request, 'creer_transaction_pret.html', context)

# Vue pour modifier une transaction d'épargne
def modifier_transaction_epargne(request, pk):
    transaction = get_object_or_404(TransactionEpargne, pk=pk)
    if request.method == 'POST':
        transaction_form = TransactionEpargneForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions d'épargne
            old_type_transaction = TransactionEpargne.objects.get(pk=transaction.pk).type_transaction
            if transaction.type_transaction == 'Depot':
                # Effectuer les opérations spécifiques au dépôt
                pass
            elif transaction.type_transaction == 'Retrait':
                # Effectuer les opérations spécifiques au retrait
                pass
            elif transaction.type_transaction == 'Virement':
                # Effectuer les opérations spécifiques au virement
                pass
            transaction.save()
            return redirect('liste_transactions')
    else:
        transaction_form = TransactionEpargneForm(instance=transaction)
    
    return render(request, 'modifier_transaction_epargne.html', {'transaction_form': transaction_form})

# Vue pour modifier une transaction de prêt
def modifier_transaction_pret(request, pk):
    transaction = get_object_or_404(TransactionPret, pk=pk)
    if request.method == 'POST':
        transaction_form = TransactionPretForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions de prêt
            old_type_transaction = TransactionPret.objects.get(pk=transaction.pk).type_transaction
            if transaction.type_transaction == 'Depot':
                # Effectuer les opérations spécifiques au dépôt
                pass
            elif transaction.type_transaction == 'Retrait':
                # Effectuer les opérations spécifiques au retrait
                pass
            elif transaction.type_transaction == 'Virement':
                # Effectuer les opérations spécifiques au virement
                pass
            transaction.save()
            return redirect('liste_transactions')
    else:
        transaction_form = TransactionPretForm(instance=transaction)
    
    return render(request, 'modifier_transaction_pret.html', {'transaction_form': transaction_form})

# Vue pour supprimer une transaction
def supprimer_transactionEpargne(request, pk):
    transaction = get_object_or_404(TransactionEpargne, pk=pk)

    # Vérifier si la requête est de type POST
    if request.method == 'POST':
        # Supprimer la transaction
        transaction.delete()
        # Rediriger vers la page souhaitée après la suppression
        return redirect('liste_transactions')  # Remplacez 'liste_transactions' par le nom de la vue où vous souhaitez rediriger l'utilisateur après la suppression

    # Si la requête n'est pas de type POST, afficher la page de confirmation de suppression
    return render(request, 'deleteconfirmation.html', {'transaction': transaction})

# DEPENSES--------------------------------------------------------------------------------------------
def liste_depenses(request):
    depenses = Depense.objects.all()
    return render(request, 'Pages/Depense/liste_depenses.html', {'depenses': depenses})

def ajouter_depense(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST)
        if form.is_valid():
            #if request.user.is_agent:
            #    form.agent = request.user
            form.save()
            return redirect('liste_depenses')
    else:
        form = DepenseForm()
    return render(request, 'Pages/Depense/ajouter_depense.html', {'form': form})

def modifier_depense(request, depense_id):
    depense = Depense.objects.get(pk=depense_id)
    if request.method == 'POST':
        form = DepenseForm(request.POST, instance=depense)
        if form.is_valid():
            form.save()
            return redirect('liste_depenses')
    else:
        form = DepenseForm(instance=depense)
    return render(request, 'Pages/Depense/modifier_depense.html', {'form': form})

def supprimer_depense(request, depense_id):
    depense = Depense.objects.get(pk=depense_id)
    if request.method == 'POST':
        depense.delete()
        return redirect('liste_depenses')
    return render(request, 'Pages/Depense/supprimer_depense.html', {'depense': depense})




#CALCUL BENEFICES ACTIONNAIRES -----------------------------------------------------------------------
def afficher_resultats(request):
    

    # Récupérer les actionnaires et leurs informations
    actionnaires = Actionnaire.objects.all()

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Calculer les parts de chaque actionnaire en pourcentage
    total_apport = sum(actionnaire.apport for actionnaire in actionnaires)
    for actionnaire in actionnaires:
        actionnaire.part = round((actionnaire.apport / total_apport) * 100,2)

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital
    for actionnaire in actionnaires:
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir)

    # Passer les données au template
    context = {
        
        'actionnaires': actionnaires,
        'benefice_mois': benefice_mois,
        'depenses_mois': depenses_mois,
        'montant_a_repartir': montant_a_repartir,
    }

    return render(request, 'Pages/Actionnaire/resultats.html', context)

def afficher_dashboard(request):
    
    # Récupérer les actionnaires et leurs informations
    actionnaires = Actionnaire.objects.all()

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Calculer les parts de chaque actionnaire en pourcentage
    total_apport = sum(actionnaire.apport for actionnaire in actionnaires)
    for actionnaire in actionnaires:
        actionnaire.part = round((actionnaire.apport / total_apport) * 100,2)

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital
    for actionnaire in actionnaires:
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir)

    # Récupérer les décomptes du nombre d'enseignants de chaque genre depuis la base de données-------------
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Récupérer
    date_today = datetime.now().date()
    date_un_mois_avant = date_today - timedelta(days=30)

    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees


    # Calculer le montant total des prêts actifs avec une durée prévisionnelle--------------
    statut_actif = Statuts.objects.get(statut='Actif')
    total_montant_pret_previsionnel = sum((pret.solde-pret.somme_initiale) for pret in ComptePrets.objects.filter(statut=statut_actif, duree_en_mois__gt=0))

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital et des prêts prévisionnels
    for action in actionnaires:
        action.montant_a_paye = round((action.part / 100) * total_montant_pret_previsionnel)


    # Obtenez la date d'aujourd'hui---------------------------------------------------------------
    # Récupérer le nombre de transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()
    
    # Récupérer les montants des transactions par type-------------------------------
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    
        
    
    # Passer les données au template
    context = {
        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,

        'total_montant_pret_previsionnel': total_montant_pret_previsionnel,  # Ajoutez cette variable au contexte
        'action': action,

        'actionnaires': actionnaires,
        'benefice_mois': benefice_mois,
        'depenses_mois': depenses_mois,
        'montant_a_repartir': montant_a_repartir,

        'male_countens': male_countens,
        'female_countens': female_countens,

        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,


        'depot_amount': depot_amount,
        'retrait_amount': retrait_amount,
        'virement_amount': virement_amount,

    }

    return render(request, 'Pages/Actionnaire/dashboardact.html', context)

def liste_actionnaires(request):
    actionnaires = Actionnaire.objects.all()
    return render(request, 'Pages/Actionnaire/liste_actionnaires.html', {'actionnaires': actionnaires})

def detail_actionnaire(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)
    return render(request, 'Pages/Actionnaire/detail_actionnaire.html', {'actionnaire': actionnaire})

def ajouter_actionnaire(request):
    if request.method == 'POST':
        form = ActionnaireForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = form.cleaned_data['nom']
            usernam = form.cleaned_data['prenom']
            FString = userna + " " + usernam
            username = FString
            role = "ACTIONNAIRE"
            statu = 'NON ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=userna, password=encoded_password, email=email, role=role)
            
            actionnaire = form.save(commit=False)
            actionnaire.user = user
            actionnaire.save()
            
            return redirect('liste_actionnaires')
    else:
        form = ActionnaireForm()

    return render(request, 'Pages/Actionnaire/ajouter_actionnaire.html', {'form': form})


def modifier_actionnaire(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)

    if request.method == 'POST':
        form = ActionnaireForm(request.POST, instance=actionnaire)
        if form.is_valid():
            form.save()
            return redirect('liste_actionnaires')
    else:
        form = ActionnaireForm(instance=actionnaire)

    return render(request, 'Pages/Actionnaire/modifier_actionnaire.html', {'form': form})


def supprimer_actionnaire(request, actionnaire_id):
    agent = get_object_or_404(Actionnaire, pk=actionnaire_id)
    if request.method == 'POST':
        agent.user.delete()  # Supprimer l'utilisateur associé
        agent.delete()
        return redirect('liste_actionnaires')
    return render(request, 'Pages/Actionnaire/supprimer_actionnaire.html', {'agent': agent})

from django.db.models import Sum

def courbe_transactions(request):
    # Récupérer les décomptes du nombre d'enseignants de chaque genre depuis la base de données-------------
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Récupérer
    date_today = datetime.now().date()
    date_un_mois_avant = date_today - timedelta(days=30)

    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees

     # Récupérer le nombre de transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()
    
    # Récupérer les montants des transactions par type-------------------------------
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    # Récupérer les données des transactions d'épargne------------------------------------
    # Calculer la date de début et la date de fin pour l'intervalle d'un mois
    aujourd_hui = datetime.today()
    mois_precedent = aujourd_hui - timedelta(days=30)  # Interval d'un mois environ

    # Récupérer les transactions d'épargne pour l'intervalle d'un mois
    transactions = TransactionEpargne.objects.filter(date_transaction__gte=mois_precedent)

    # Préparer les données pour le graphique à barres
    transactions_data = {}
    for transaction in transactions:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_data:
            transactions_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_data[date][transaction.type_transaction] += float(transaction.montant)

    # Calculer la date de début et la date de fin pour l'intervalle d'un mois-------------------------
    aujourdhui = datetime.today()
    mois_precedent = aujourdhui - timedelta(days=30)

    # Récupérer les transactions de prêt pour l'intervalle d'un mois
    transactions_pret = TransactionPret.objects.filter(date_transaction__gte=mois_precedent)

    # Préparer les données pour le graphique à barres
    transactions_pret_data = {}
    for transaction in transactions_pret:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_pret_data:
            transactions_pret_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_pret_data[date][transaction.type_transaction] += float(transaction.montant)

    # Récupérer-------------

    context = {
        'male_countens': male_countens,
        'female_countens': female_countens,

        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,

        'depot_amount': depot_amount,
        'retrait_amount': retrait_amount,
        'virement_amount': virement_amount,

        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,

        'transactions_data': transactions_data,

        'transactions_pret_data': transactions_pret_data,
    }
    
    return render(request, 'Pages/Dashboard/dashboard.html',context)

