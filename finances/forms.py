from datetime import date
from django import forms

from finances.views import definir_date_fin_pret
from .models import Actionnaire, Depense,Clients, CompteEpargnes, ComptePrets,TransactionEpargne, TransactionPret, Agent,Genres, Matrimoniales, Typeprets
        
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ['sexe']

class MatrimonialeForm(forms.ModelForm):
    class Meta:
        model = Matrimoniales
        fields = ['matrimoniale']

class TypepretForm(forms.ModelForm):
    class Meta:
        model = Typeprets
        fields = ['type_pret']

class TypePretForm(forms.Form):
    type_pret = forms.ModelChoiceField(queryset=Typeprets.objects.all())

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'sexe', 'email', 'photo', 'piece_identite_scan',
                  'profession', 'date_naissance', 'lieu_naissance', 'type_piece_identite', 'numero_piece_identite',
                  'validite_piece_identite_debut', 'validite_piece_identite_fin', 'ville_village', 'matrimoniale']
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le nom du client'}),
            'prenom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le prénom du client'}),
            'telephone': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de téléphone'}),
            'date_naissance': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de naissance'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Entrez l\'adresse e-mail'}),
            'adresse': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Entrez l\'adresse'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'piece_identite_scan': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'profession': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la profession du client'}),
            'lieu_naissance': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le lieu de naissance'}),
            'type_piece_identite': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez le type de pièce d\'identité'}),
            'numero_piece_identite': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de pièce d\'identité'}),
            'validite_piece_identite_debut': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de début de validité'}),
            'validite_piece_identite_fin': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de fin de validité'}),
            'ville_village': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la ville ou le village'}),
            'matrimoniale': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez l\'état matrimonial'}),
            'sexe': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez l\'état matrimonial'}),
            
        }

class CompteEpargneForm(forms.ModelForm):
    class Meta:
        model = CompteEpargnes
        fields = ['client', 'numero_compte', 'solde', 'statut']



    
class ComptePretForm(forms.ModelForm):
    

    class Meta:
        model = ComptePrets
        fields = ['client', 'taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret']
        
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
           
        }

    def save(self, commit=True):
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde = garantie + montant_pret

        elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde += montant_pret

        if commit:
            compte_pret.save()

        return compte_pret



class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['nom', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }


class ActionnaireForm(forms.ModelForm):
    class Meta:
        model = Actionnaire
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'apport', 'pourcentage']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActionnaireForm, self).__init__(*args, **kwargs)
        # Ajouter des widgets personnalisés pour les champs 'apport' et 'pourcentage'
        self.fields['apport'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'apport'})
        self.fields['pourcentage'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le pourcentage'})

class TransactionEpargneForm(forms.ModelForm):
    class Meta:
        model = TransactionEpargne
        fields = ['compte_epargne', 'montant', 'type_transaction']
        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'compte_epargne': forms.TextInput(attrs={'class':'form-control'} ),
        }
        

class TransactionPretForm(forms.ModelForm):
    class Meta:
        model = TransactionPret
        fields = ['type_transaction', 'montant', 'compte_pret']

        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'compte_pret': forms.Select(attrs={'class': 'form-select'}),
        }
