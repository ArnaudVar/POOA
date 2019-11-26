# POOA
POOA project

Members : 

	- Arnaud Vargas
	- Hippolyte Favreau
	- Victor Le Fourn

##  Pour commencer
    - Se rendre à l'adresse https://seriegenda.herokuapp.com/ (site un peu plus rapide)
    Ou 
    - pip install -r requirements.txt
    - python main.py
    - Go to http://localhost:5000


## Login
    Identifiants :
        - Username : Admin  
     
        - Mot de passe : test

    Register : 
    Possibilité de s'inscrire sur le site avec une adresse mail et un mot de passe
    
    Forgot password :
    Possibilité de retrouver son mot de passe par mail si on l'a oublié

## Home page 
    Affichage des dernières sorties de séries et films au centre de la page 
### Sidebar 
        - My movies/My series pour voir les médias que l'on a ajoutés à notre liste avec le dernier 
        épisode regardé qui s'affiche sur l'image de la série lorsque la souris passe dessus
        
        - Best series/Best movies pour les series ou films les plus populaires
        
        - TV genres/Movies genres pour voir les séries ou films répartis par thème
        
        - Unseen Episodes avec notifications pour voir  parmi les séries ajoutées celles
         pour lesquelles l'utilisateur n'est pas à jour. Les notifications correspondent au nombre de 
         séries pour lesquelles l'utilisateur n'est pas à jour et s'affichent en collapse lorsque la souris 
         passe sur la zone de "Unseen Episode"
        
### Searchbar 
        Il est bien évidemment possible d'effectuer une recherche pour un film ou une série 
        avec la barre de recherche en haut à gauche.
        Les résultats seront affichés avec les séries à gauche et les films à droite
     
## Serie/Film
        Pour ajouter une série/un film à sa liste, l'utilisateur doit cliquer d'abord sur le bouton 
        plus qui s'affiche quand la souris passe sur l'image de la série.
        Une fois sur la page de la série ou du film :
        Il est possible dans la headbar de noter la série sur 5 à l'aide des étoiles et du bouton "Rate"
        (d'abord établir la note avec les étoiles puis la valider avec Rate pour l'envoyer à l'API
        TheMovieDB). 
        - Pour les séries : on trouve sur le côté une barre permettant de sélectionner l'épisode 
        affiché, on a le résumé de l'épisode sélectionné avec son image et les séries similaires 
        en dessous de ce résumé. Pour indiquer qu'un épisode a été vu, il suffit de cliquer 
        sur l'icone oeil barré à côté de "Not viewed" et il passera à Viewed comme tous les 
        épisodes précédents
        
        - Pour les films, on peut trouver le synopsis du film avec son image et en dessous les 
        films similaires.
        
     
         
    
        
