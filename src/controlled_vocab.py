"""
Controlled Vocabulary Definitions
==================================

This module defines static normalization mappings used to convert
raw source values into ISO-compliant controlled vocabulary values.

Each field key maps to a dictionary of:

  raw_value -> normalized_display_text

Example:
  "EN" -> "eng; CAN"

These normalized values are later resolved to their corresponding
codeList identifiers (e.g., RI_XXX) during XML generation.

This file contains only vocabulary configuration.
Normalization logic is handled in normalization.py.
"""

CONTROLLED_VOCAB = {
  "language": {
    "EN": "eng; CAN",
    "FR": "fra; CAN"
  },

  "characterSet": {
    "utf8": "utf8; utf8"
  },
  
  # IC_90
  "role": {
    # EN
    "Resource Provider": "resourceProvider; fournisseurDeRessource",
    "Custodian": "custodian; gardien",
    "Owner": "owner; proprietaire",
    "User": "user; utilisateur",
    "Distributor": "distributor; distributeur",
    "Originator": "originator; createur",
    "Point of Contact": "pointOfContact; contact",
    "Principal Investigator": "principalInvestigator; chercheurPrincipal",
    "Processor": "processor; responsableDuTraitement",
    "Publisher": "publisher; editeur",
    "Author": "author; auteur",
    "Sponsor": "sponsor; commanditaire",
    "Co-Author": "coAuthor; coauteur",
    "Collaborator": "collaborator; collaborateur",
    "Editor": "editor; redacteur",
    "Mediator": "mediator; mediateur",
    "Rights Holder": "rightsHolder; titulaireDesDroits",

    # FR
    "Fournisseur de ressource": "resourceProvider; fournisseurDeRessource",
    "Gardien": "custodian; gardien",
    "Propriétaire": "owner; proprietaire",
    "Utilisateur": "user; utilisateur",
    "Distributeur": "distributor; distributeur",
    "Créateur": "originator; createur",
    "Contact": "pointOfContact; contact",
    "Chercheur Principal": "principalInvestigator; chercheurPrincipal",
    "Responsable du traitement": "processor; responsableDuTraitement",
    "Éditeur": "publisher; editeur",
    "Auteur": "author; auteur",
    "Commanditaire": "sponsor; commanditaire",
    "Coauteur": "coAuthor; coauteur",
    "Collaborateur": "collaborator; collaborateur",
    "Rédacteur": "editor; redacteur",
    "Médiateur": "mediator; mediateur",
    "Titulaire des droits": "rightsHolder; titulaireDesDroits",

    # 
    "point of contact": "pointOfContact; contact",
    "Principal Investigator": "principalInvestigator; chercheurPrincipal",
    # "PSSI Distributor": "distributor; distributeur",

    "contact": "pointOfContact; contact",
    "Chercheur Principal": "principalInvestigator; chercheurPrincipal",
  },

  # IC_106
  "status": {
    # EN
    "Completed": "completed; termine",
    "Historical Archive": "historicalArchive; archiveHistorique",
    "Obsolete": "obsolete; obsolete",
    "Ongoing": "onGoing; enContinue",
    "Planned": "planned; planifie",
    "Required": "required; requis",
    "Under Development": "underDevelopment; enDeveloppement",
    "Proposed": "proposed; propose",

    # FR
    "Terminé": "completed; termine",
    "Archive historique": "historicalArchive; archiveHistorique",
    "Obsolète": "obsolete; obsolete",
    "En continue": "onGoing; enContinue",
    "Planifié": "planned; planifie",
    "Requis": "required; requis",
    "En développement": "underDevelopment; enDeveloppement",
    "Proposé": "proposed; propose",

    # 
    "Ongoing Test": "onGoing; enContinue",
  },

  # 
  "keyword": {
    # EN
    "Economics": "economics",
    "Enforcement": "enforcement",
    "Enhancement": "enhancement",
    "Fisheries Management": "fisheriesManagement",
    "Aquaculture": "aquaculture",
    "Habitat": "habitat",
    "Science": "science",

    # FR
    "Économie": "economics",
    "Application": "enforcement",
    "Amélioration": "enhancement",
    "Gestion des pêches": "fisheriesManagement",
    "Aquaculture": "aquaculture",
    "Habitat": "habitat",
    "Science": "science",
  },
  
  # 
  "topicCategory": {
    # EN
    "Farming": "farming",
    "Biota": "biota",
    "Boundaries": "boundaries",
    "Climatology / Meteorology / Atmosphere": "climatologyMeteorologyAtmosphere",
    "Economy": "economy",
    "Elevation": "elevation",
    "Environment": "environment",
    "Geoscientific Information": "geoscientificInformation",
    "Health": "health",
    "Imagery / Base Maps / Earth Cover": "imageryBaseMapsEarthCover",
    "Intelligence / Military": "intelligenceMilitary",
    "Inland Waters": "inlandWaters",
    "Location": "location",
    "Oceans": "oceans",
    "Planning / Cadastre": "planningCadastre",
    "Society": "society",
    "Structure": "structure",
    "Transportation": "transportation",
    "Utilities / Communication": "utilitiesCommunication",

    # FR
    "Agriculture": "farming",
    "Biote": "biota",
    "Limites": "boundaries",
    "Climatologie / Météorologie / Atmosphère": "climatologyMeteorologyAtmosphere",
    "Économie": "economy",
    "Élévation": "elevation",
    "Environnement": "environment",
    "Information géoscientifique": "geoscientificInformation",
    "Santé": "health",
    "Imagerie / Cartes de base / Occupation des terres": "imageryBaseMapsEarthCover",
    "Renseignement / Militaire": "intelligenceMilitary",
    "Eaux intérieures": "inlandWaters",
    "Localisation": "location",
    "Océans": "oceans",
    "Aménagement / Cadastre": "planningCadastre",
    "Société": "society",
    "Structure": "structure",
    "Transport": "transportation",
    "Services publics / Communication": "utilitiesCommunication",
  },

  # IC_102
  "updateFrequency": {
    # EN
    "As available": "continual; continuellement",
    "Daily": "daily; quotidien",
    "Weekly": "weekly; hebdomadaire",
    "Every 2 Weeks": "fortnightly; bimensuel",
    "Monthly": "monthly; mensuel",
    "Quarterly (Every 3 Months)": "quarterly; trimestriel",
    "Semi-Annual (Every 6 Months)": "biannually; semestriel",
    "Annually": "annually; annuel",
    "On Demand": "asNeeded; au besoin",
    "Irregularly": "irregular; irrégulier",
    # "": "notPlanned; non planifié",
    # "": "unknown; inconnu",
    "Twice Monthly": "semimonthly; bimensuel",

    # FR
    "Selon disponibilité": "continual; continuellement",
    "Quotidiennement": "daily; quotidien",
    "Hebdomadairement": "weekly; hebdomadaire",
    "Toutes les deux semaines": "fortnightly; bimensuel",
    "Mensuellement": "monthly; mensuel",
    "Trimestriellement (Tous les trois mois)": "quarterly; trimestriel",
    "Semestriellement (Tous les six mois)": "biannually; semestriel",
    "Annuellement": "annually; annuel",
    "À la demande": "asNeeded; au besoin",
    "De manière irrégulière": "irregular; irrégulier",
    # "": "notPlanned; non planifié",
    # "": "unknown; inconnu",
    "Deux fois par mois": "semimonthly; bimensuel",
  },

  # IC_96
  "classification": {
    # EN
    "Unclassified": "unclassified; nonClassifié",
    "Restricted": "restricted; restreint",
    "Confidential": "confidential; confidentiel",
    "Secret": "secret; secret",
    "Top Secret": "topSecret: trèsSecret",
    "Sensitive": "sensitive; sensible",
    "For Official Use Only": "forOfficialUseOnly; réservéÀOrganisation",

    # FR
    "Non classifié": "unclassified; nonClassifié",
    "Restreint": "restricted; restreint",
    "Confidentiel": "confidential; confidentiel",
    "Secret": "secret; secret",
    "Très Secret": "topSecret: trèsSecret",
    "Sensible": "sensitive; sensible",
    "Réservé À Organisation": "forOfficialUseOnly; réservéÀOrganisation"
  },

  # IC_109
  "spatialType": {
    # EN
    "Vector": "vector; vecteur",
    "Grid": "grid; grille",
    "Text Table": "textTable; tableTexte",
    "TIN": "tin; tin",
    "Stereo Model": "stereoModel; modeleStereo",
    "Video": "video; video",

    # FR
    "Vecteur": "vector; vecteur",
    "Grille": "grid; grille",
    "Table texte": "textTable; tableTexte",
    "TIN": "tin; tin",
    "Modèle stéréo": "stereoModel; modeleStereo",
    "Vidéo": "video; video",
  }
}
