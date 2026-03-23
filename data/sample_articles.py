"""
Générateur d'articles juridiques fictifs mais réalistes pour le mode DÉMO.

Les numéros d'articles, la terminologie et la structure suivent fidèlement
le Code du travail français et le RGPD. Le contenu est synthétique et ne
constitue pas un avis juridique.
"""

from typing import Any


def get_sample_articles() -> list[dict[str, Any]]:
    """
    Retourne une liste de 30 chunks d'articles juridiques avec métadonnées.

    Chaque chunk contient :
        - article_number : référence officielle (ex. L1221-1)
        - title          : intitulé de l'article
        - source         : "Code du travail" ou "RGPD"
        - content        : texte de l'article (fictif mais plausible)
    """
    articles = [
        # ── CODE DU TRAVAIL — Contrat de travail ─────────────────────────────
        {
            "article_number": "L1221-1",
            "title": "Définition du contrat de travail",
            "source": "Code du travail",
            "content": (
                "Le contrat de travail est défini comme la convention par laquelle "
                "une personne physique s'engage à mettre son activité à la disposition "
                "d'une autre personne, physique ou morale, sous la subordination de "
                "laquelle elle se place, moyennant une rémunération. Le lien de "
                "subordination juridique constitue l'élément déterminant qui distingue "
                "le contrat de travail d'autres formes contractuelles telles que le "
                "contrat de prestation de services ou le mandat. La qualification de "
                "contrat de travail relève des juges du fond, indépendamment de la "
                "dénomination retenue par les parties."
            ),
        },
        {
            "article_number": "L1221-2",
            "title": "Forme du contrat de travail",
            "source": "Code du travail",
            "content": (
                "Le contrat de travail à durée indéterminée est la forme normale et "
                "générale de la relation de travail. Il peut être conclu sans écrit, "
                "sauf disposition légale contraire. Toutefois, lorsqu'il est conclu "
                "entre un employeur et un travailleur étranger, il doit être rédigé "
                "par écrit. Toute clause dérogatoire à cet article doit être expressément "
                "stipulée. L'absence d'écrit ne prive pas le salarié des droits attachés "
                "au contrat de travail à durée indéterminée."
            ),
        },
        {
            "article_number": "L1221-19",
            "title": "Période d'essai — CDI",
            "source": "Code du travail",
            "content": (
                "Le contrat de travail à durée indéterminée peut comporter une période "
                "d'essai dont la durée maximale est fixée comme suit : deux mois pour "
                "les ouvriers et employés ; trois mois pour les agents de maîtrise et "
                "techniciens ; quatre mois pour les cadres. La période d'essai, "
                "renouvellement inclus, ne peut dépasser ces durées maximales. Elle "
                "doit être expressément stipulée dans le contrat de travail ou la lettre "
                "d'engagement pour être opposable au salarié."
            ),
        },
        {
            "article_number": "L1237-19",
            "title": "Rupture conventionnelle",
            "source": "Code du travail",
            "content": (
                "L'employeur et le salarié peuvent convenir en commun des conditions de "
                "la rupture du contrat de travail à durée indéterminée qui les lie. La "
                "rupture conventionnelle, exclusive du licenciement ou de la démission, "
                "ne peut être imposée par l'une ou l'autre des parties. Elle résulte d'une "
                "convention signée par les parties au contrat. Elle est soumise aux "
                "dispositions de la présente section destinées à garantir la liberté du "
                "consentement des parties. Le salarié bénéficie d'une indemnité spécifique "
                "de rupture dont le montant ne peut être inférieur à l'indemnité légale "
                "de licenciement."
            ),
        },
        {
            "article_number": "L1231-1",
            "title": "Rupture du contrat à durée indéterminée",
            "source": "Code du travail",
            "content": (
                "Le contrat de travail à durée indéterminée peut être rompu à l'initiative "
                "de l'employeur ou du salarié, ou d'un commun accord, dans les conditions "
                "prévues par les dispositions du présent titre. Ces dispositions sont "
                "applicables aux employeurs de droit privé ainsi qu'à leurs salariés. "
                "Elles sont également applicables au personnel des établissements publics "
                "à caractère industriel et commercial. En cas de litige, le juge prud'homal "
                "est compétent pour statuer sur la validité et les conséquences de la rupture."
            ),
        },
        {
            "article_number": "L1237-1",
            "title": "Démission du salarié",
            "source": "Code du travail",
            "content": (
                "La démission est un acte unilatéral par lequel le salarié manifeste de "
                "façon claire et non équivoque sa volonté de mettre fin au contrat de "
                "travail. Pour être valable, la démission doit résulter d'une volonté "
                "libre et éclairée du salarié. Elle n'est pas soumise à un formalisme "
                "particulier, mais il est fortement conseillé de la notifier par écrit "
                "avec accusé de réception. Le salarié qui démissionne est tenu d'effectuer "
                "un préavis dont la durée est fixée par la convention collective applicable."
            ),
        },
        {
            "article_number": "L1251-1",
            "title": "Travail temporaire — définition",
            "source": "Code du travail",
            "content": (
                "Le travail temporaire est l'opération par laquelle une entreprise de "
                "travail temporaire met à la disposition provisoire d'une entreprise "
                "utilisatrice des salariés qu'elle recrute et rémunère à cet effet. "
                "Une mission de travail temporaire ne peut avoir ni pour objet ni pour "
                "effet de pourvoir durablement un emploi lié à l'activité normale et "
                "permanente de l'entreprise utilisatrice. La durée maximale d'une mission "
                "est en principe de dix-huit mois, renouvellement compris."
            ),
        },
        # ── CODE DU TRAVAIL — Durée du travail ───────────────────────────────
        {
            "article_number": "L3121-1",
            "title": "Définition du temps de travail effectif",
            "source": "Code du travail",
            "content": (
                "La durée du travail effectif est le temps pendant lequel le salarié est "
                "à la disposition de l'employeur et se conforme à ses directives sans "
                "pouvoir vaquer librement à des occupations personnelles. Le temps de "
                "travail effectif se distingue du temps de trajet entre le domicile et "
                "le lieu de travail habituel, ainsi que des temps de pause qui ne "
                "satisfont pas aux critères précités. Cette définition conditionne le "
                "calcul des heures supplémentaires et le respect des durées maximales."
            ),
        },
        {
            "article_number": "L3121-18",
            "title": "Durée maximale quotidienne de travail",
            "source": "Code du travail",
            "content": (
                "La durée quotidienne du travail effectif par salarié ne peut excéder "
                "dix heures, sauf en cas de dérogation accordée par l'inspecteur du "
                "travail dans les cas prévus par décret. Une convention ou un accord "
                "d'entreprise ou d'établissement ou, à défaut, une convention ou un "
                "accord de branche peut prévoir le dépassement de la durée maximale "
                "quotidienne de dix heures en cas d'activité accrue ou pour des motifs "
                "liés à l'organisation de l'entreprise, à condition que ce dépassement "
                "n'ait pas pour effet de porter cette durée à plus de douze heures."
            ),
        },
        {
            "article_number": "L3121-20",
            "title": "Durée maximale hebdomadaire absolue",
            "source": "Code du travail",
            "content": (
                "Au cours d'une même semaine, la durée maximale absolue du travail "
                "effectif est de quarante-huit heures. Cette limite hebdomadaire absolue "
                "ne peut faire l'objet d'aucune dérogation, sauf circonstances "
                "exceptionnelles et autorisation de l'autorité administrative. Sur une "
                "période quelconque de douze semaines consécutives, la durée hebdomadaire "
                "moyenne de travail ne peut dépasser quarante-quatre heures. Le non-respect "
                "de ces limites est passible de sanctions pénales."
            ),
        },
        {
            "article_number": "L3121-27",
            "title": "Durée légale hebdomadaire — 35 heures",
            "source": "Code du travail",
            "content": (
                "La durée légale du travail effectif des salariés à temps complet est "
                "fixée à trente-cinq heures par semaine. Toute heure accomplie au-delà "
                "de cette durée légale est une heure supplémentaire qui ouvre droit à "
                "une majoration salariale ou, le cas échéant, à un repos compensateur "
                "équivalent. Le contingent annuel d'heures supplémentaires est fixé par "
                "convention ou accord collectif d'entreprise ou d'établissement ou, à "
                "défaut, par accord de branche. À défaut d'accord, le contingent est "
                "fixé à deux cent vingt heures par an et par salarié."
            ),
        },
        {
            "article_number": "L3131-1",
            "title": "Repos quotidien",
            "source": "Code du travail",
            "content": (
                "Tout salarié bénéficie d'un repos quotidien d'une durée minimale de "
                "onze heures consécutives. Cette obligation s'applique à tous les "
                "salariés, quelle que soit la taille de l'entreprise ou le secteur "
                "d'activité. Des dérogations peuvent être prévues par convention ou "
                "accord collectif, sous réserve que des périodes de repos équivalent "
                "soient accordées. Le non-respect du repos quotidien minimal est "
                "constitutif d'une infraction au droit du travail susceptible d'entraîner "
                "la responsabilité de l'employeur."
            ),
        },
        {
            "article_number": "L3132-1",
            "title": "Repos hebdomadaire",
            "source": "Code du travail",
            "content": (
                "Il est interdit de faire travailler un même salarié plus de six jours "
                "par semaine. Le repos hebdomadaire a une durée minimale de vingt-quatre "
                "heures consécutives, auxquelles s'ajoutent les heures consécutives de "
                "repos quotidien prévu par l'article L3131-1, soit au total trente-cinq "
                "heures minimum de repos consécutif. En principe, le jour de repos "
                "hebdomadaire est le dimanche. Des dérogations au repos dominical peuvent "
                "être accordées par le préfet ou prévues par accord collectif dans les "
                "secteurs et zones géographiques définis par la loi."
            ),
        },
        # ── CODE DU TRAVAIL — Congés payés ───────────────────────────────────
        {
            "article_number": "L3141-1",
            "title": "Droit aux congés payés",
            "source": "Code du travail",
            "content": (
                "Tout salarié a droit à un congé payé à la charge de l'employeur. "
                "Ce droit est ouvert dès lors que le salarié justifie avoir travaillé "
                "chez le même employeur pendant un temps équivalant à un minimum de "
                "dix jours de travail effectif. La période de référence pour l'acquisition "
                "des congés payés est fixée du 1er juin de l'année précédente au 31 mai "
                "de l'année en cours, sauf disposition conventionnelle contraire. "
                "Les congés payés doivent être pris dans la période fixée par la "
                "convention collective ou, à défaut, entre le 1er mai et le 31 octobre."
            ),
        },
        {
            "article_number": "L3141-3",
            "title": "Durée des congés payés",
            "source": "Code du travail",
            "content": (
                "Le salarié a droit à un congé de deux jours et demi ouvrables par "
                "mois de travail effectif chez le même employeur. La durée totale du "
                "congé exigible ne peut excéder trente jours ouvrables par an, soit "
                "cinq semaines. Sont assimilées à des périodes de travail effectif pour "
                "la détermination de la durée du congé : les périodes de congé payé "
                "de l'année précédente, les congés de maternité, de paternité, d'adoption "
                "et d'accueil de l'enfant, ainsi que les arrêts de travail pour accident "
                "du travail ou maladie professionnelle dans la limite d'un an."
            ),
        },
        # ── CODE DU TRAVAIL — Rémunération ───────────────────────────────────
        {
            "article_number": "L3211-1",
            "title": "Salaire minimum de croissance (SMIC)",
            "source": "Code du travail",
            "content": (
                "Tout salarié bénéficie d'une rémunération au moins égale au salaire "
                "minimum de croissance (SMIC). Aucun salarié ne peut percevoir une "
                "rémunération inférieure à ce seuil, indépendamment de toute convention "
                "collective ou accord d'entreprise. Le SMIC est revalorisé automatiquement "
                "chaque année au 1er janvier et, en cours d'année, dès lors que l'indice "
                "des prix à la consommation atteint une hausse d'au moins deux pour cent "
                "par rapport à l'indice constaté lors de la dernière revalorisation. "
                "Le montant du SMIC est fixé par décret en Conseil d'État."
            ),
        },
        {
            "article_number": "L3241-1",
            "title": "Bulletin de paie",
            "source": "Code du travail",
            "content": (
                "À l'occasion du paiement du salaire, l'employeur remet à chaque salarié "
                "un bulletin de paie. L'employeur ne peut exiger la signature de ce "
                "bulletin que pour valoir reçu du paiement. Le bulletin de paie peut "
                "être remis sous forme électronique, sous réserve que le salarié ne s'y "
                "soit pas opposé. Il doit mentionner notamment l'identité de l'employeur "
                "et du salarié, le montant du salaire brut, les cotisations et contributions "
                "sociales, le salaire net imposable et le net à payer. La conservation "
                "du bulletin de paie est assurée sans limitation de durée."
            ),
        },
        # ── CODE DU TRAVAIL — Santé et sécurité ──────────────────────────────
        {
            "article_number": "L4121-1",
            "title": "Obligation de sécurité de l'employeur",
            "source": "Code du travail",
            "content": (
                "L'employeur prend les mesures nécessaires pour assurer la sécurité et "
                "protéger la santé physique et mentale des travailleurs. Ces mesures "
                "comprennent : des actions de prévention des risques professionnels et "
                "de la pénibilité au travail, des actions d'information et de formation, "
                "la mise en place d'une organisation et de moyens adaptés. L'employeur "
                "veille à l'adaptation de ces mesures pour tenir compte du changement "
                "des circonstances et tendre à l'amélioration des situations existantes. "
                "L'obligation de sécurité est une obligation de résultat renforcée "
                "dont le non-respect engage la responsabilité civile et pénale de l'employeur."
            ),
        },
        {
            "article_number": "L1152-1",
            "title": "Harcèlement moral",
            "source": "Code du travail",
            "content": (
                "Aucun salarié ne doit subir les agissements répétés de harcèlement moral "
                "qui ont pour objet ou pour effet une dégradation de ses conditions de "
                "travail susceptible de porter atteinte à ses droits et à sa dignité, "
                "d'altérer sa santé physique ou mentale ou de compromettre son avenir "
                "professionnel. L'employeur prend toutes dispositions nécessaires en "
                "vue de prévenir les agissements de harcèlement moral. Tout salarié "
                "ayant procédé à de tels agissements est passible d'une sanction "
                "disciplinaire. Est nul tout licenciement prononcé en méconnaissance "
                "de cet article."
            ),
        },
        {
            "article_number": "L1153-1",
            "title": "Harcèlement sexuel",
            "source": "Code du travail",
            "content": (
                "Aucun salarié ne doit subir des faits de harcèlement sexuel, constitué "
                "par des propos ou comportements à connotation sexuelle ou sexiste répétés "
                "qui soit portent atteinte à sa dignité en raison de leur caractère "
                "dégradant ou humiliant, soit créent à son encontre une situation "
                "intimidante, hostile ou offensante. Est assimilé au harcèlement sexuel "
                "le fait, même non répété, d'user de toute forme de pression grave dans "
                "le but réel ou apparent d'obtenir un acte de nature sexuelle. L'employeur "
                "affiche dans les lieux de travail ainsi que dans les locaux ou à la porte "
                "des locaux où se fait l'embauche les textes relatifs à l'égalité "
                "professionnelle et au harcèlement sexuel."
            ),
        },
        # ── CODE DU TRAVAIL — Représentation du personnel ────────────────────
        {
            "article_number": "L2311-1",
            "title": "Comité social et économique (CSE)",
            "source": "Code du travail",
            "content": (
                "Des comités sociaux et économiques sont constitués dans les entreprises "
                "d'au moins onze salariés. La mise en place d'un comité social et "
                "économique n'est obligatoire que si l'effectif de onze salariés est "
                "atteint pendant douze mois consécutifs. Le comité social et économique "
                "a pour mission d'assurer une expression collective des salariés permettant "
                "la prise en compte permanente de leurs intérêts dans les décisions "
                "relatives à la gestion et à l'évolution économique et financière de "
                "l'entreprise, à l'organisation du travail, à la formation professionnelle "
                "et aux techniques de production."
            ),
        },
        {
            "article_number": "L2314-1",
            "title": "Élections des membres du CSE",
            "source": "Code du travail",
            "content": (
                "Les membres de la délégation du personnel du comité social et économique "
                "sont élus pour quatre ans. Le nombre de membres titulaires et suppléants "
                "est fixé par décret en Conseil d'État en fonction de l'effectif de "
                "l'entreprise. Les membres du CSE sont élus par deux collèges électoraux : "
                "le collège des ouvriers et employés et le collège des ingénieurs, chefs "
                "de service, techniciens, agents de maîtrise et assimilés. Un troisième "
                "collège peut être créé dans les entreprises comportant des cadres. "
                "Le vote peut être effectué par voie électronique dans les conditions "
                "fixées par accord d'entreprise."
            ),
        },
        # ── CODE DU TRAVAIL — Licenciement ───────────────────────────────────
        {
            "article_number": "L1232-1",
            "title": "Licenciement pour motif personnel",
            "source": "Code du travail",
            "content": (
                "Tout licenciement pour motif personnel doit être justifié par une cause "
                "réelle et sérieuse. La cause est réelle lorsqu'elle est établie, c'est-à-dire "
                "objective, exacte et vérifiable. La cause est sérieuse lorsqu'elle est "
                "suffisamment importante pour rendre impossible, sans dommage pour "
                "l'entreprise, la continuation du contrat de travail. L'employeur qui "
                "envisage de licencier un salarié pour motif personnel convoque ce "
                "dernier à un entretien préalable au licenciement par lettre recommandée "
                "ou remise en main propre contre décharge."
            ),
        },
        {
            "article_number": "L1237-13",
            "title": "Indemnité spécifique de rupture conventionnelle",
            "source": "Code du travail",
            "content": (
                "La convention de rupture définit notamment le montant de l'indemnité "
                "spécifique de rupture conventionnelle qui ne peut pas être inférieur "
                "à celui de l'indemnité légale de licenciement prévue à l'article "
                "L1234-9. La convention de rupture fixe la date de rupture du contrat "
                "de travail qui ne peut intervenir avant le lendemain du jour de "
                "l'homologation de la convention ou, pour les salariés protégés, le "
                "lendemain de la date d'autorisation de la rupture conventionnelle. "
                "À compter de la date de la signature de la convention, les parties "
                "disposent d'un délai de quinze jours calendaires pour exercer leur "
                "droit de rétractation."
            ),
        },
        # ── RGPD ─────────────────────────────────────────────────────────────
        {
            "article_number": "RGPD - Article 4",
            "title": "Définitions RGPD",
            "source": "RGPD",
            "content": (
                "Aux fins du présent règlement, on entend par « données à caractère "
                "personnel » toute information se rapportant à une personne physique "
                "identifiée ou identifiable, dénommée « personne concernée ». Est "
                "réputée identifiable une personne physique qui peut être identifiée, "
                "directement ou indirectement, notamment par référence à un identifiant "
                "tel qu'un nom, un numéro d'identification, des données de localisation, "
                "un identifiant en ligne, ou à un ou plusieurs éléments spécifiques "
                "propres à son identité physique, physiologique, génétique, psychique, "
                "économique, culturelle ou sociale."
            ),
        },
        {
            "article_number": "RGPD - Article 5",
            "title": "Principes relatifs au traitement des données",
            "source": "RGPD",
            "content": (
                "Les données à caractère personnel doivent être traitées de manière "
                "licite, loyale et transparente (licéité, loyauté, transparence). Elles "
                "doivent être collectées pour des finalités déterminées, explicites et "
                "légitimes, et ne pas être traitées ultérieurement d'une manière "
                "incompatible avec ces finalités (limitation des finalités). Elles "
                "doivent être adéquates, pertinentes et limitées à ce qui est nécessaire "
                "au regard des finalités pour lesquelles elles sont traitées (minimisation "
                "des données). Elles doivent être exactes et, si nécessaire, tenues à "
                "jour (exactitude)."
            ),
        },
        {
            "article_number": "RGPD - Article 6",
            "title": "Licéité du traitement",
            "source": "RGPD",
            "content": (
                "Le traitement n'est licite que si, et dans la mesure où, au moins une "
                "des conditions suivantes est remplie : la personne concernée a consenti "
                "au traitement pour une ou plusieurs finalités spécifiques ; le traitement "
                "est nécessaire à l'exécution d'un contrat auquel la personne concernée "
                "est partie ; le traitement est nécessaire au respect d'une obligation "
                "légale ; le traitement est nécessaire à la sauvegarde des intérêts "
                "vitaux de la personne concernée ; le traitement est nécessaire à "
                "l'exécution d'une mission d'intérêt public ; le traitement est nécessaire "
                "aux fins des intérêts légitimes poursuivis par le responsable du "
                "traitement, sauf si ces intérêts sont contrebalancés par les droits "
                "fondamentaux de la personne concernée."
            ),
        },
        {
            "article_number": "RGPD - Article 7",
            "title": "Conditions applicables au consentement",
            "source": "RGPD",
            "content": (
                "Dans les cas où le traitement repose sur le consentement, le responsable "
                "du traitement est en mesure de démontrer que la personne concernée a "
                "donné son consentement au traitement de données à caractère personnel "
                "la concernant. Si le consentement de la personne concernée est donné "
                "dans le cadre d'une déclaration écrite qui concerne également d'autres "
                "questions, la demande de consentement est présentée sous une forme "
                "qui la distingue clairement de ces autres questions. La personne "
                "concernée a le droit de retirer son consentement à tout moment. Le "
                "retrait du consentement ne compromet pas la licéité du traitement "
                "fondé sur le consentement effectué avant ce retrait."
            ),
        },
        {
            "article_number": "RGPD - Article 15",
            "title": "Droit d'accès de la personne concernée",
            "source": "RGPD",
            "content": (
                "La personne concernée a le droit d'obtenir du responsable du traitement "
                "la confirmation que des données à caractère personnel la concernant "
                "sont ou ne sont pas traitées et, lorsqu'elles le sont, l'accès auxdites "
                "données à caractère personnel ainsi que les informations suivantes : "
                "les finalités du traitement ; les catégories de données concernées ; "
                "les destinataires ou catégories de destinataires ; la durée de "
                "conservation envisagée ou les critères utilisés pour la déterminer ; "
                "l'existence du droit de demander la rectification ou l'effacement des "
                "données. Le responsable du traitement fournit une copie des données "
                "faisant l'objet d'un traitement dans un délai d'un mois."
            ),
        },
        {
            "article_number": "RGPD - Article 17",
            "title": "Droit à l'effacement (droit à l'oubli)",
            "source": "RGPD",
            "content": (
                "La personne concernée a le droit d'obtenir du responsable du traitement "
                "l'effacement, dans les meilleurs délais, de données à caractère "
                "personnel la concernant et le responsable du traitement a l'obligation "
                "d'effacer ces données à caractère personnel dans les meilleurs délais, "
                "lorsque l'un des motifs suivants s'applique : les données ne sont plus "
                "nécessaires au regard des finalités pour lesquelles elles ont été "
                "collectées ou traitées ; la personne concernée retire le consentement "
                "sur lequel est fondé le traitement et il n'existe pas d'autre fondement "
                "juridique au traitement ; la personne concernée s'oppose au traitement "
                "et il n'existe pas de motif légitime impérieux pour le traitement."
            ),
        },
        {
            "article_number": "RGPD - Article 25",
            "title": "Protection des données dès la conception et par défaut",
            "source": "RGPD",
            "content": (
                "Compte tenu de l'état des techniques, du coût de la mise en œuvre et "
                "de la nature, de la portée, du contexte et des finalités du traitement "
                "ainsi que des risques, dont le degré de probabilité et de gravité varie, "
                "que le traitement présente pour les droits et libertés des personnes "
                "physiques, le responsable du traitement met en œuvre, tant au moment "
                "de la détermination des moyens du traitement qu'au moment du traitement "
                "lui-même, des mesures techniques et organisationnelles appropriées, "
                "telles que la pseudonymisation, qui sont destinées à mettre en œuvre "
                "les principes relatifs à la protection des données (privacy by design)."
            ),
        },
        {
            "article_number": "RGPD - Article 83",
            "title": "Conditions générales pour imposer des amendes administratives",
            "source": "RGPD",
            "content": (
                "Les violations des dispositions suivantes font l'objet, conformément "
                "au paragraphe 2, d'amendes administratives pouvant s'élever jusqu'à "
                "20 000 000 EUR ou, dans le cas d'une entreprise, jusqu'à 4 % du chiffre "
                "d'affaires annuel mondial total de l'exercice précédent, le montant le "
                "plus élevé étant retenu. Pour les violations portant sur les principes "
                "de base du traitement (article 5), les conditions applicables au "
                "consentement (article 7), les droits des personnes (articles 12 à 22), "
                "le montant maximal est de 20 millions d'euros ou 4 % du chiffre d'affaires "
                "mondial. La CNIL est l'autorité de contrôle compétente en France."
            ),
        },
    ]

    return articles
