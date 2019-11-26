# POOA
POOA project

Members : 

	- Arnaud Vargas
	- Hippolyte Favreau
	- Victor Le Fourn

##  Pour commencer
    - Se rendre � l'adresse https://seriegenda.herokuapp.com/ (site un peu plus rapide)
    Ou 
    - pip install -r requirements.txt
    - python main.py
    - Go to http://localhost:5000


## Login
    Identifiants :
        - Username : Admin  
     
        - Mot de passe : test

    Register : 
    Possibilit� de s'inscrire sur le site avec une adresse mail et un mot de passe
    
    Forgot password :
    Possibilit� de retrouver son mot de passe par mail si on l'a oubli�

## Home page 
    Affichage des derni�res sorties de s�ries et films au centre de la page 
### Sidebar 
        - My movies/My series pour voir les m�dias que l'on a ajout�s � notre liste avec le dernier 
        �pisode regard� qui s'affiche sur l'image de la s�rie lorsque la souris passe dessus
        
        - Best series/Best movies pour les series ou films les plus populaires
        
        - TV genres/Movies genres pour voir les s�ries ou films r�partis par th�me
        
        - Unseen Episodes avec notifications pour voir  parmi les s�ries ajout�es celles
         pour lesquelles l'utilisateur n'est pas � jour. Les notifications correspondent au nombre de 
         s�ries pour lesquelles l'utilisateur n'est pas � jour et s'affichent en collapse lorsque la souris 
         passe sur la zone de "Unseen Episode"
        
### Searchbar 
        Il est bien �videmment possible d'effectuer une recherche pour un film ou une s�rie 
        avec la barre de recherche en haut � gauche.
        Les r�sultats seront affich�s avec les s�ries � gauche et les films � droite
     
## Serie/Film
        Pour ajouter une s�rie/un film � sa liste, l'utilisateur doit cliquer d'abord sur le bouton 
        plus qui s'affiche quand la souris passe sur l'image de la s�rie.
        Une fois sur la page de la s�rie ou du film :
        Il est possible dans la headbar de noter la s�rie sur 5 � l'aide des �toiles et du bouton "Rate"
        (d'abord �tablir la note avec les �toiles puis la valider avec Rate pour l'envoyer � l'API
        TheMovieDB). 
        - Pour les s�ries : on trouve sur le c�t� une barre permettant de s�lectionner l'�pisode 
        affich�, on a le r�sum� de l'�pisode s�lectionn� avec son image et les s�ries similaires 
        en dessous de ce r�sum�. Pour indiquer qu'un �pisode a �t� vu, il suffit de cliquer 
        sur l'icone oeil barr� � c�t� de "Not viewed" et il passera � Viewed comme tous les 
        �pisodes pr�c�dents
        
        - Pour les films, on peut trouver le synopsis du film avec son image et en dessous les 
        films similaires.
        
     
         
    
        
