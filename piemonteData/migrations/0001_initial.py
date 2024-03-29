# Generated by Django 4.2.7 on 2024-01-09 19:29

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
            name="Diretoria",
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
                ("nome", models.CharField(max_length=20)),
                ("sobrenome", models.CharField(max_length=20)),
                ("matricula", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                ("email_sent", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Gerencia",
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
                ("nome", models.CharField(max_length=20)),
                ("sobrenome", models.CharField(max_length=30)),
                ("matricula", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                ("email_sent", models.BooleanField(default=False)),
                (
                    "diretoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.diretoria",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("must_change_password", models.BooleanField(default=False)),
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
            name="Supervisao",
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
                ("nome", models.CharField(max_length=20, null=True)),
                ("sobrenome", models.CharField(max_length=30, null=True)),
                ("matricula", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                ("email_sent", models.BooleanField(default=False)),
                (
                    "diretoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.diretoria",
                    ),
                ),
                (
                    "gerencia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.gerencia",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Agente",
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
                ("nome", models.CharField(max_length=30)),
                ("sobrenome", models.CharField(max_length=50)),
                ("matricula", models.CharField(max_length=30)),
                (
                    "cidade",
                    models.CharField(
                        choices=[
                            ("a. dourada", "A. Dourada"),
                            ("aracaju", "Aracaju"),
                            ("camaçari", "Camaçari"),
                            ("campo do brito", "Campo do Brito"),
                            ("candeal", "Candeal"),
                            ("capim grosso", "Capim Grosso"),
                            ("carira", "Carira"),
                            ("frei paulo", "Frei Paulo"),
                            ("iaçu", "Iaçu"),
                            ("ibitiara", "Ibitiara"),
                            ("ibotirama", "Ibotirama"),
                            ("iuiu", "Iuiu"),
                            ("jacobina", "Jacobina"),
                            ("macambira", "Macambira"),
                            ("n. sª da glória", "N. Sª Da Glória"),
                            ("neópolis", "Neópolis"),
                            ("pindobaçu", "Pindobaçu"),
                            ("salvador", "Salvador"),
                            ("saúde", "Saúde"),
                            ("seabra", "Seabra"),
                            ("serrolândia", "Serrolândia"),
                            ("simãodias", "SimãoDias"),
                            ("sobradinho", "Sobradinho"),
                            ("são cristóvão", "São Cristóvão"),
                            ("utinga", "Utinga"),
                            ("várzeanova", "VárzeaNova"),
                        ],
                        max_length=50,
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("email_sent", models.BooleanField(default=False)),
                (
                    "diretoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.diretoria",
                    ),
                ),
                (
                    "gerencia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.gerencia",
                    ),
                ),
                (
                    "supervisor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="piemonteData.supervisao",
                    ),
                ),
            ],
        ),
    ]
