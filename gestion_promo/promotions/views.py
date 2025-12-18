from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Promotion


def promotion_create(request: HttpRequest) -> HttpResponse:
    context: dict = {
        "current_year": datetime.now().year,
    }

    if request.method == "POST":
        raw_year = request.POST.get("year", "").strip()
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip().upper()
        description = request.POST.get("description", "").strip()

        errors: dict[str, str] = {}

        # Validation année
        try:
            year_int = int(raw_year)
        except ValueError:
            year_int = None
            errors["year"] = "L'année doit être un nombre valide."

        if year_int is None:
            errors["year"] = errors.get("year") or "L'année est obligatoire."
        elif year_int < 2000 or year_int > datetime.now().year + 10:
            errors["year"] = "L'année doit être comprise entre 2000 et dans 10 ans."

        # Validation texte
        if not name:
            errors["name"] = "L'intitulé de la promotion est obligatoire."

        if not code:
            errors["code"] = "Le code de la promotion est obligatoire."

        # Unicité
        if year_int is not None and Promotion.objects.filter(year=year_int).exists():
            errors["year"] = "Une promotion existe déjà pour cette année."

        if code and Promotion.objects.filter(code__iexact=code).exists():
            errors["code"] = "Ce code est déjà utilisé par une autre promotion."

        # Création
        if not errors and year_int is not None:
            Promotion.objects.create(
                year=year_int,
                name=name,
                code=code,
                description=description,
            )
            return redirect(reverse("promotions:promotion_success"))

        # Retour erreurs
        context.update(
            {
                "errors": errors,
                "form_values": {
                    "year": raw_year,
                    "name": name,
                    "code": code,
                    "description": description,
                },
            }
        )

    return render(request, "promotions/promotion_form.html", context)


def promotion_success(request: HttpRequest) -> HttpResponse:
    return render(request, "promotions/promotion_success.html")
