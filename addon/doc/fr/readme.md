# Dire le type  et l'état des contrôle  avant leur libellé

* Auteur: Pierre-Louis Renaud;
* URL: [Contact](https://www.rptools.org/NVDA-Thunderbird/toContact.html) ;
<!-- * Download the [stable version][1] ; -->
* Télécharger la [dernière version sur RPTools.org](https://www.rptools.org/?p=9200) ;
* Compatibilité NVDA : 2019.3 et supérieur ;
<!-- * [Source code on GitHub][2] ; --> 

## Présentation
Cette extension flexible permet à NVDA d'annoncer le type et l'état des éléments d'interface utilisateur avant leur libellé.

Par exemple, on entendra Case à cocher cochée avant son  libellé qui peut être long. 
Dans des dialogues comportant beaucoup de cases à cocher ou de boutons radio, ceci peut considérablement améliorer l'efficacité de la vérification d'options ou de paramètres ;

De plus, les libellés des types et états des contrôles peuvent être raccourcis. Pour "cases à cocher", vous pourrez indiquer "Case", vous entendrez alors : case cochée. 

Pour le moment, l'extension ne prend en charge que les cases à cocher, boutons radio,éléments de menu à cocher et radio. 
D'autres types d'éléments pourront être ajoutés ultérieurement.

En outre, vous pourrez décider d'utiliser cette extension avec des réglages propres à chaque profil d'application via son dialogue des paramètres.

En voici un exemple :

case à cocher coché Dire le texte des éléments en modifiant leur nom (mieux adapté au Braille), Alt+n, 

Sélectionnez le format d'annonce des éléments ci-dessous :

Cases à cocher et boutons radio : liste déroulante Type état libellé réduit Alt+c

Menus à cocher et radio : liste déroulante Type état libellé réduit Alt+m

OK Annuler

Chaque liste déroulante contient les options suivantes :

* Défaut : l'extension n'intervient pas pour ce type de contrôle et dans le profil de configuration courant ;
* Type état libellé : par exemple Case à cocher cochée Sauvegarder la configuration en quittant, Alt+s  ;
* Etat libellé : exemple : coché Sauvegarder la configuration en quittant, Alt+s ;

## Raccourcis-clavier

Ces raccourcis, modifiables via le dialogue des gestes de commandes, vous permettent de régler l'extension à votre meilleure convenance.

* Windows+$ : affiche le dialogue de configuration pour le profil actif.
  Ceci permet des réglages propres à chaque application. Veillez donc à créer au préalable un profil de configuration pour l'application où vous souhaitez une intervention de l'extension. ;
* Maj+Windows+$ : pour personnaliser les libellés des états et types d'éléments via le bloc-notes.
  Après l'installation de controlTypeBeforeLabel, l'extension récupère les libellés standards de votre système et les enregistre directement dans le fichier ini.
  Après modification de ce fichier, vous devez redémarrer NVDA ou recharger les extensions.
  Pour réinitialiser ces libellés à leurs valeurs d'origine, vous pouvez supprimer ce fichier ini puis relancer NVDA. Il sera recréé automatiquement.
  Ce ffichier de paramètres    est commun à tous les profils de configuration ; 


<!-- links section -->

[1]: https://github.com/RPTools-org/controlTypeBeforeLabel/releases/download/v2023.07.27/controlTypeBeforeLabel-2023.07.27.nvda-addon

[2]: https://github.com/RPTools-org/controlTypeBeforeLabel/
