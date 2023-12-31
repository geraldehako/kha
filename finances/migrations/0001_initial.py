# Generated by Django 4.1.7 on 2023-08-02 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("adresse", models.CharField(max_length=200)),
                ("telephone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Clients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, null=True)),
                ("prenom", models.CharField(max_length=100, null=True)),
                ("adresse", models.CharField(max_length=200, null=True)),
                ("telephone", models.CharField(max_length=20, null=True)),
                ("email", models.EmailField(max_length=254, null=True, unique=True)),
                ("date_inscription", models.DateField(auto_now_add=True, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="Images/Photos/Clients/"
                    ),
                ),
                (
                    "piece_identite_scan",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Images/Photos/Clients/Pieceidentite/",
                    ),
                ),
                ("profession", models.CharField(blank=True, max_length=100, null=True)),
                ("date_naissance", models.DateField()),
                ("lieu_naissance", models.CharField(max_length=100, null=True)),
                (
                    "type_piece_identite",
                    models.CharField(
                        choices=[
                            ("CNI", "Carte Nationale d'Identité"),
                            ("passeport", "Passeport"),
                            ("Attestation", "Attestation d'identité"),
                        ],
                        max_length=20,
                    ),
                ),
                ("numero_piece_identite", models.CharField(max_length=100, null=True)),
                ("validite_piece_identite_debut", models.DateField()),
                ("validite_piece_identite_fin", models.DateField()),
                ("ville_village", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CompteEpargnes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_compte", models.CharField(max_length=20, unique=True)),
                (
                    "solde",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finances.clients",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComptePrets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_compte", models.CharField(max_length=20, unique=True)),
                (
                    "solde",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "taux_interet",
                    models.DecimalField(decimal_places=2, default=1, max_digits=5),
                ),
                ("duree_en_mois", models.PositiveIntegerField(default=12)),
                ("date_debut_pret", models.DateField()),
                ("date_fin_pret", models.DateField()),
                (
                    "somme_initiale",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("domicile_bancaire", models.CharField(max_length=200, null=True)),
                ("date_demande", models.DateField(auto_now_add=True, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finances.clients",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genres",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sexe", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Matrimoniales",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("matrimoniale", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Statuts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("statut", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Typeprets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_pret", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="TransactionPret",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "type_transaction",
                    models.CharField(
                        choices=[
                            ("Depot", "Dépôt"),
                            ("Retrait", "Retrait"),
                            ("Virement", "Virement"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_transaction", models.DateTimeField(auto_now_add=True)),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="finances.agent",
                    ),
                ),
                (
                    "compte_pret",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_pret",
                        to="finances.compteprets",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransactionEpargne",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "type_transaction",
                    models.CharField(
                        choices=[
                            ("Depot", "Dépôt"),
                            ("Retrait", "Retrait"),
                            ("Virement", "Virement"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_transaction", models.DateTimeField(auto_now_add=True)),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="finances.agent",
                    ),
                ),
                (
                    "compte_epargne",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_epargne",
                        to="finances.compteepargnes",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Echeancier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_echeance", models.DateField()),
                (
                    "montant_echeance",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("est_paye", models.BooleanField(default=False)),
                (
                    "compte_pret",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finances.compteprets",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="compteprets",
            name="statut",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="finances.statuts"
            ),
        ),
        migrations.AddField(
            model_name="compteprets",
            name="type_pret",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finances.typeprets",
            ),
        ),
        migrations.AddField(
            model_name="compteepargnes",
            name="statut",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finances.statuts",
            ),
        ),
        migrations.AddField(
            model_name="clients",
            name="matrimoniale",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finances.matrimoniales",
            ),
        ),
        migrations.AddField(
            model_name="clients",
            name="sexe",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finances.genres",
            ),
        ),
        migrations.AddField(
            model_name="clients",
            name="statut",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finances.statuts",
            ),
        ),
        migrations.CreateModel(
            name="Actionnaire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("adresse", models.CharField(max_length=200)),
                ("telephone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
