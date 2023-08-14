"""Prologicielsucces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from finances import views
from accounts.views import login_user,logout_user


urlpatterns = [
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    
    path("admin/", admin.site.urls),
    path('accounts/', login_user, name='login'),
    path('accounts/log', logout_user, name='signup'),
    path('administration/menu', views.menu, name='menu'),
    path('actionnaire/menu', views.afficher_dashboard, name='menuact'),

    
# URL pour la liste des genres
    path('genres/', views.liste_genres, name='liste_genres'),
    # URL pour ajouter un genre
    path('genres/ajouter/', views.creer_genre, name='ajouter_genre'),
    # URL pour modifier un genre
    path('genres/modifier/<int:pk>/', views.modifier_genre, name='modifier_genre'),
    # URL pour supprimer un genre
    path('genres/supprimer/<int:pk>/', views.supprimer_genre, name='supprimer_genre'),
    
    # URL pour la liste des matrimoniales
    path('matrimoniales/', views.liste_matrimoniales, name='liste_matrimoniales'),
    # URL pour ajouter une matrimoniales
    path('matrimoniales/ajouter/', views.creer_matrimoniale, name='ajouter_matrimoniales'),
    # URL pour modifier une matrimoniales
    path('matrimoniales/modifier/<int:pk>/', views.modifier_matrimoniale, name='modifier_matrimoniales'),
    # URL pour supprimer une matrimoniales
    path('matrimoniales/supprimer/<int:pk>/', views.supprimer_matrimoniale, name='supprimer_matrimoniales'),
    
    # URL pour la liste des types de prêts
    path('typeprets/', views.liste_typeprets, name='liste_typeprets'),
    # URL pour ajouter un type de prêt
    path('typeprets/ajouter/', views.creer_typepret, name='ajouter_typeprets'),
    # URL pour modifier un type de prêt
    path('typeprets/modifier/<int:pk>/', views.modifier_typepret, name='modifier_typeprets'),
    # URL pour supprimer un type de prêt
    path('typeprets/supprimer/<int:pk>/', views.supprimer_typepret, name='supprimer_typeprets'),
# URL pour la liste des clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/<int:client_id>/detail', views.detail_clients, name='detail_clients'),
    # URL pour ajouter un client
    path('clients/ajouter/', views.creer_client, name='ajouter_client'),
    # URL pour modifier un client
    path('clients/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    # URL pour supprimer un client
    path('clients/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
    
    # URL pour la liste des comptes épargnes
    path('comptes_epargnes/', views.liste_comptes_epargne, name='liste_comptes_epargnes'),
    path('comptes_epargne/<int:compte_epargne_id>/', views.detail_compte_epargne, name='detail_compte_epargne'),
    # URL pour ajouter un compte épargne
    path('comptes_epargnes/ajouter/', views.creer_compte_epargne, name='ajouter_compte_epargne'),
    # URL pour modifier un compte épargne
    path('comptes_epargnes/modifier/<int:pk>/', views.modifier_compte_epargne, name='modifier_compte_epargne'),
    # URL pour supprimer un compte épargne
    path('comptes_epargnes/supprimer/<int:pk>/', views.supprimer_compte_epargne, name='supprimer_compte_epargne'),
    
    # URL pour la liste des comptes prêts
    path('comptes_prets/', views.liste_comptes_prets, name='liste_comptes_prets'),
    path('compte_pret/<int:compte_pret_id>/', views.detail_compte_pret, name='detail_compte_pret'),
    # URL pour la liste des comptes prêts
    path('comptes_prets/echeances', views.clients_proche_echeance, name='clients_proche_echeance'),
    # URL pour la liste des comptes prêts
    path('comptes_prets/echeancesnon', views.liste_echeances_non_payees, name='liste_echeances_non_payees'),
    # URL pour ajouter un compte prêt
    path('comptes_prets/<int:client_id>/ajouter/', views.ajouter_compte_pret, name='ajouter_compte_pret'),
    # URL pour modifier un compte prêt
    path('comptes_prets/modifier/<int:pk>/', views.modifier_compte_pret, name='modifier_compte_pret'),
    # URL pour supprimer un compte prêt
    path('comptes_prets/supprimer/<int:pk>/', views.supprimer_compte_pret, name='supprimer_compte_pret'),
    path('comptes_prets/modifier/<int:pk>/', views.modifier_compte_pret, name='modifier_compte_pret'),
    # URL pour la liste des agents
    path('agents/', views.liste_agents, name='liste_agents'),
    # URL pour ajouter un agent
    path('agents/ajouter/', views.ajouter_agent, name='ajouter_agent'),
    # URL pour modifier un agent
    path('agents/modifier/<int:pk>/', views.modifier_agent, name='modifier_agent'),
    # URL pour supprimer un agent
    path('agents/supprimer/<int:pk>/', views.supprimer_agent, name='supprimer_agent'),
    path('modifier_est_paye/<int:actionnaire_id>/', views.modifier_est_paye, name='modifier_est_paye'),
    path('modifier_est_payeretard/<int:actionnaire_id>/', views.modifier_est_payere, name='modifier_est_payere'),

    # URL pour la liste des transactions
    path('creer_transaction_epargne/<int:id>', views.creer_transaction_epargne, name='creer_transaction_epargne'),
    path('creer_transaction_pret/', views.creer_transaction_pret, name='creer_transaction_pret'),
    path('modifier_transaction_epargne/<int:pk>/', views.modifier_transaction_epargne, name='modifier_transaction_epargne'),
    path('modifier_transaction_pret/<int:pk>/', views.modifier_transaction_pret, name='modifier_transaction_pret'),
    path('supprimer_transaction/<int:pk>/', views.supprimer_transactionEpargne, name='supprimer_transaction'),
    path('liste_transactions/', views.liste_transactions, name='liste_transactions'),

    # URL pour la liste des depenses
    path('liste_depenses/', views.liste_depenses, name='liste_depenses'),
    path('ajouter_depense/', views.ajouter_depense, name='ajouter_depense'),
    path('modifier_depense/<int:depense_id>/', views.modifier_depense, name='modifier_depense'),
    path('supprimer_depense/<int:depense_id>/', views.supprimer_depense, name='supprimer_depense'),

    # URL pour la liste des actionnaires
    path('resultats/', views.afficher_resultats, name='afficher_resultats'),
    path('actionnaires/', views.liste_actionnaires, name='liste_actionnaires'),
    path('detail_actionnaire/<int:actionnaire_id>/', views.detail_actionnaire, name='detail_actionnaire'),
    path('actionnaires/ajouter/', views.ajouter_actionnaire, name='ajouter_actionnaire'),
    path('actionnaires/modifier/<int:actionnaire_id>/', views.modifier_actionnaire, name='modifier_actionnaire'),
    path('actionnaires/supprimer/<int:actionnaire_id>/', views.supprimer_actionnaire, name='supprimer_actionnaire'),
    path('courbe_transactions/', views.courbe_transactions, name='courbe_transactions'),
]

