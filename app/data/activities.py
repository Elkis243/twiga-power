from django.utils.translation import gettext_lazy as _

ACTIVITIES = [
    {
        "slug": "importation",
        "title": _("Importation de l'énergie électrique"),
        "description": _(
            "L'importation de l'énergie électrique constitue un levier stratégique pour Twiga Power Sarl. Elle permet de renforcer l'approvisionnement lorsque la production locale est insuffisante, d'assurer la continuité et la stabilité du service, et de répondre efficacement aux pics de consommation."
        ),
        "image": "images/activite6.webp",
        "image_alt": _("Importation d'énergie électrique"),
    },
    {
        "slug": "exportation",
        "title": _("Exportation de l'énergie électrique"),
        "description": _(
            "Twiga Power Sarl développe également des activités d'exportation de l'énergie électrique visant à valoriser les capacités de production excédentaires et à participer aux échanges énergétiques régionaux. Cette activité contribue au renforcement de la compétitivité de l'entreprise, à la création de valeur économique et au positionnement de la RDC comme un acteur énergétique régional."
        ),
        "image": "images/activite5.webp",
        "image_alt": _("Exportation d'énergie électrique"),
    },
    {
        "slug": "production",
        "title": _("Production de l'énergie électrique"),
        "description": _(
            "La production constitue un pilier stratégique pour Twiga Power Sarl, qui développe des capacités basées sur l'eau (centrales hydroélectriques), la chaleur (solutions thermiques), le vent (éolien), le soleil (photovoltaïque) et des solutions hybrides combinant plusieurs sources selon les besoins locaux. Cette diversification assure un approvisionnement énergétique sûr, durable et résilient, tout en contribuant à la transition énergétique du pays."
        ),
        "image": "images/activite1.webp",
        "image_alt": _("Production d'énergie électrique"),
    },
    {
        "slug": "transport",
        "title": _("Transport de l'énergie électrique"),
        "description": _(
            "Le transport de l'électricité consiste à acheminer l'énergie produite ou importée vers les centres de consommation à travers des infrastructures haute et moyenne tension, en veillant à la sécurité, à la performance des lignes et à la réduction des pertes techniques."
        ),
        "image": "images/activite2.webp",
        "image_alt": _("Transport d'énergie électrique"),
    },
    {
        "slug": "distribution",
        "title": _("Distribution de l'énergie électrique"),
        "description": _(
            "La distribution constitue le lien direct entre Twiga Power Sarl et les consommateurs finaux. L'entreprise déploie et exploite des réseaux adaptés aux réalités locales, en mettant l'accent sur la fiabilité, la qualité du service et l'amélioration de l'accès à l'électricité pour les ménages et les entreprises, contribuant ainsi à la satisfaction des clients et à la confiance des partenaires."
        ),
        "image": "images/activite3.webp",
        "image_alt": _("Distribution d'énergie électrique"),
    },
    {
        "slug": "commercialisation",
        "title": _("Commercialisation de l'énergie électrique"),
        "description": _(
            "La commercialisation regroupe la vente d'électricité, la relation client et la gestion de la consommation. Twiga Power Sarl adopte une approche client basée sur la transparence tarifaire, la sensibilisation à une consommation responsable et la réduction des plaintes, contribuant ainsi à la satisfaction des clients et à la confiance des partenaires."
        ),
        "image": "images/activite4.webp",
        "image_alt": _("Commercialisation d'énergie électrique"),
    },
]
