from datetime import timezone
from django.db import models
from django.db.models import Count, Q,Sum
from accounts.models import Utilisateurs


class Genres(models.Model):
    sexe = models.CharField(max_length=10)
    def __str__(self):
        return f'{self.sexe}'

class Matrimoniales(models.Model):
    matrimoniale = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.matrimoniale}'
    
class Typeprets(models.Model):
    type_pret = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.type_pret}'

class Statuts(models.Model):
    statut = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.statut}'

class Clients(models.Model):
    TYPE_PIECE_CHOICES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('passeport', 'Passeport'),
        ('Attestation', 'Attestation d\'identité'),
    ]
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    adresse = models.CharField(max_length=200, null=True)
    telephone = models.CharField(max_length=20, null=True)
    sexe = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True, null=True)
    date_inscription = models.DateField(auto_now_add=True, null=True)
    photo = models.ImageField(upload_to='Images/Photos/Clients/', blank=True, null=True)
    piece_identite_scan = models.ImageField(upload_to='Images/Photos/Clients/Pieceidentite/', blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, null=True)
    type_piece_identite = models.CharField(max_length=20, choices=TYPE_PIECE_CHOICES)
    numero_piece_identite = models.CharField(max_length=100, null=True)
    validite_piece_identite_debut = models.DateField()
    validite_piece_identite_fin = models.DateField()
    ville_village = models.CharField(max_length=100, null=True)
    matrimoniale = models.ForeignKey(Matrimoniales, on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class CompteEpargnes(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Compte épargne {self.numero_compte} - {self.client}"
    
class ComptePrets(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=1)  # type: ignore # 1% par mois
    duree_en_mois = models.PositiveIntegerField(default=12)
    date_debut_pret = models.DateField()
    

    date_fin_pret = models.DateField()
    somme_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    domicile_bancaire = models.CharField(max_length=200, null=True)
    type_pret = models.ForeignKey(Typeprets, on_delete=models.CASCADE, null=True)
    date_demande = models.DateField(auto_now_add=True, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE)

    def calculer_interets(self):
        # Calculez les intérêts en fonction de la durée du prêt
        # Vous pouvez ajouter le code ici pour effectuer le calcul des intérêts
        # Assurez-vous d'utiliser la durée en mois et le taux d'intérêt du prêt
        # Pour cet exemple, supposons que le taux d'intérêt est exprimé en pourcentage (1% par mois)
        return self.solde * (self.taux_interet / 100) * self.duree_en_mois

    def __str__(self):
        return f"Compte prêt {self.numero_compte} - {self.client}"
    
class Agent(models.Model):
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Actionnaire(models.Model):
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    apport = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2,null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Echeancier(models.Model):
    compte_pret = models.ForeignKey(ComptePrets, on_delete=models.CASCADE)
    date_echeance = models.DateField()
    montant_echeance = models.DecimalField(max_digits=10, decimal_places=2)
    montant_interet = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    est_paye = models.BooleanField(default=False)

    def __str__(self):
        return f"Échéance pour le compte prêt {self.compte_pret.numero_compte} - Montant: {self.montant_echeance}"


class TransactionEpargne(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_epargne = models.ForeignKey(
        CompteEpargnes,
        on_delete=models.CASCADE,
        related_name='transactions_epargne',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_epargne} à {self.compte_pret}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_epargne}"


class TransactionPret(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_pret = models.ForeignKey(
        ComptePrets,
        on_delete=models.CASCADE,
        related_name='transactions_pret',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_pret} à {self.compte_epargne}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_pret}"

class Depense(models.Model):
    nom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nom
    
class License(models.Model):
    client_name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_valid_until(self):
        # Calculer la date d'expiration en ajoutant un an à la date de création
        return self.created_at + timezone.timedelta(days=365)

    def is_valid(self):
        return timezone.now() <= self.calculate_valid_until()