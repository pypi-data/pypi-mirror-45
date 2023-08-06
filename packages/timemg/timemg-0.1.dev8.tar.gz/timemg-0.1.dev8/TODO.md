# TODO

## Version 1.0

- [x] IO: ne pas enregistrer les lignes à None ; permettre la lecture de fichiers dont il manque des champs
- [x] Dissocier les valeurs par défaut quand on crée une nouvelle ligne des valeurs par défaut quand on clic sur une cellule à None
- [x] Trier selon la date par défaut
- [x] Del = supprimer la valeur d'une/plusieurs cellule(s) selectionnée(s) (remettre valeur à None) et selection cell + Ctrl+Del ou selection ligne = supprimer la ligne ; ATTENTION à la séléction multiple !
- [x] Selection mode : row -> (single) cell
- [ ] Plots (réutiliser se qui a déjà été écrit dans le notebook "sleep")
- [ ] Vérifier que modifier les données d'une cellule se fait bien via un appel direct à "model.set_data()" ; en profiter pour réviser le "flux" normal de lecture/écriture en MVC dans Qt5 (faire un diagramme)
- [ ] Ajouter le champ "Mood" (attention : c'est une variable de type categorie -> combobox)
- [ ] Anticiper la v2: ajouter un onglet avec un chrono (juste un chrono avec boutons start, stop et reset)
- [ ] Nettoyer: renommer modules, supprimer splitter, etc.
- [x] Nettoyer: supprimer splitter et widgets innutils
- [ ] Ligne d'aujourd'hui: sur fond coloré pour la mettre en évidence
- [ ] Date par défaut = "None" ??? + à l'édition, vérif si une date n'existe pas déjà et reffuse si oui -> revoir la logique de la gestion des dates dans l'interface...

Apparance Qt5 dans XFCE:
gtk2-engines-qtcurve/cosmic 1.9-2 amd64
  QtCurve widget style for applications based on GTK+ 2.x

kde-style-qtcurve-qt5/cosmic 1.9-2 amd64
  QtCurve widget style for applications based on Qt 5.x

libqtcurve-utils2/cosmic 1.9-2 amd64
  common library for QtCurve

qt5ct/cosmic 0.35-1build1 amd64
  Qt5 Configuration Utility

qtcurve/cosmic 1.9-2 amd64
  décoration de fenêtre unifiée pour applications Qt et GTK+ —⋅méta-paquet

qtcurve-l10n/cosmic,cosmic 1.9-2 all
  translation files for QtCurve

