# Introduction
Dans le cadre des travaux de recherche menés au LDR sur les plateformes embarquées, les chercheurs souhaitent mettre en place des environnements de développements et de tests plus récents et robustes pour 2 applications en particulier, dans l’ordre d’importance :  

- La programmation embarquée, en particulier avec OS Temps Réel. 
Mettre en place un environnement de dev/tests avec sondes logicielles pour le temps réel. Pour réaliser des tests de systèmes contraints, possiblement utilisant des architectures matérielles diverses (ARM, RISC-V, etc.), les chercheurs ont besoin d’un environnement clair, générant des traces analysables (quantité de mémoire utilisée, temps passé sur le processeur et lors des accès aux périphériques, décisions d’ordonnancement, etc.).

- Simulateur pour robotique/drone. 
Mettre en place un environnement de dev/tests avec, par exemple CoppeliaSim et Python/ROS, génération de scénario et récupération des données de vol et de l’environnement simulé.  
Différents travaux sont réalisés depuis plusieurs années avec l’ONERA sur des simulations utilisant de drones. Ces travaux utilisent d’anciens simulateurs difficiles à maintenir aujourd’hui, ce qui rend complexe la reproduction de certains résultats. Plusieurs exemples existent pour des applications spécifiques, comme avec le robot Poppy et ROS.

On va s'intéresser que sur la partie simulation pour la suite de cette documentation, concernant la documentation de la partie embarqué, elle est disponible sur un autre dossier nommé LDR_ZephyrOS

# Simulation

La simulation c’est la création d’un modèle virtuel d’une machine, tout en prenant en considération l’environnement de travail et tous les autres facteurs influents. Ça nous permet de savoir si la conception peut fonctionner après la fabrication. Ça nous permet de tester différentes machines/algorithmes dans un même environnement (plusieurs drones dans un parc urbain et voir comment chaque drone navigue entre les arbres et réagit aux obstacles), et de tester une machine dans différents environnements (simuler un seul modèle de drone au-dessus d'une forêt avec des vents variables, dans un désert avec des températures élevées ou à l’intérieur de la maison).

Pour la suite du projet, on va se concentrer sur deux simulateurs qui sont CoppeliaSim et GazeboSim, ils sont tous les deux des simulateurs dynamiques de la robotique mais avec des caractéristiques distinctes.

L'image suivante est l'interface graphique de CoppeliaSim 

![Interface graphique de Coppeliasim](/assets/images/interface_coppeliasim.png "Interface graphique de Coppeliasim")

L'image suivante est l'interface graphique de GazeboSim

![Interface graphique de GazeboSim](/assets/images/interface_gazebo.png "Interface graphique de GazeboSim")


Après avoir tester les deux simulateurs, j'ai pu restituer les avantages et inconvenients de chacun, l’objectif de cette comparaison est de déterminer le simulateur le plus adapté à nos besoins (coté recherche et coté enseignements)

## La restitution des avantages/inconvénients

### Le simulateur CoppeliaSim

|  **Avantages** 	|  **Inconvénients** 	|
|---	|---	|
| L'installation est simple et rapide<br>sur Windows, une version portable est<br>également disponible. 	| L’exécution n’est pas possible via le<br>terminal directement sans avoir lancer<br>CoppeliaSim avant. 	|
| La création des scènes est simple,<br>la personnalisation est également<br>possible grâce aux script intégrés 	| un facteur de temps réel n’est pas très<br>lent que le temps réel (pour l’exemple<br>de BubbleRob il est de 0.99 donc 9900 fois<br>plus lent que le temps réel). 	|
| Interface graphique conviviale et<br>facile à utiliser, la création des<br>scènes est donc simple, la personnalisation<br>est possible grâce aux script intégrés 	|  	|
| CoppeliaSim n’est pas déterministe<br>mais on peut le configurer pour l’être<br>en modifiantcertains paramètres mais ces <br>modifications influencent négativement sur<br>le comportement dans les simulations<br>(disparition des objets par exemple) 	|  	|


### Le simulateur GazeboSim

| **Avantages** 	| **Inconvénients** 	|
|---	|---	|
| L’installation et la prise en main de <br>la plateforme sur Linux est plus facile <br>à installer et à configurer 	| L’installation sur Windows est complexe<br>car des installations supplémentaires<br>sont nécessaires (via conda-forge,<br>vcpkg ou WSL) 	|
| La création d’une scène est en XML <br>et son exécution est dans un terminal <br>directement sans passer par l’interface<br>graphique 	| Windows n'est pas une plateforme officiellement<br>supportée par Open Robotics pour Gazebo 	|
| GazeboSim offre une personnalisation<br>avancée car il supporte plusieurs langages<br> de programmation (Python, C++) 	| L’installation nécessite une version <br>spécifique sur Linux (ubuntu 22.04) donc<br>manque de flexibilité 	|
| Un facteur de temps réel est beaucoup<br>plus rapide que le temps réel  	| L'interface graphique de GazeboSim<br>est complexe pour les débutants <br>(notamment pour la version classique). 	|
|  	| Une carte graphique Nvidia avec support<br>CUDA est requise pour l’exécution de<br>certaines simulations. 	|

 #### Tableau récapitulatif de la comparaison 

![Comparaison en tableau](/assets/images/comparaison.png "tableau récapitulatif")


## Les besoins pour la simulation

Un simulateur :

-  Qui a l’interface graphique de Coppeliasim pour qu'il soit facilement utilisé par les étudiants.
-  Qui exécute les scènes facilement, où on a pas besoin de jouer sur plusieurs plans pour lancer la simulation
-  Facile à installer sur windows de preférence (car sur linux certaines exécutions bug) 
-  Deterministe et reproductible
-  Avec un facteur temps réel qui soit proche du temps réel 

![besoins pour la simulation](/assets/images/besoin_simulation.png "Les besoins pour la simulation")

Après avoir tester les deux simulateurs et formalisé les besoins sur la simulation, j’ai choisi comme outil de simulation CoppeliaSim pour sa facilité et son efficacité ainsi que son optimalité


## Drone Painting


![Drone Painting](/assets/images/gif1.gif "DRONE PAINTING")


Il faut savoir que dans CoppeliaSim, on peut prendre des objets directement sur l'interface graphique; pour mon cas, j'ai pris un drone ensuite je lui ai rajouté un proximité sensor, qui le cone large rose, j'ai également rajouté un painting nozzle qui est le cone un peu plus fin rose, donc une fois la scène est crée on va créer une connexion entre CoppeliaSim et Python grace à ce header qu'on rajoute à notre code Python «from coppeliasim_zmqremoteapi_client import RemoteAPIClient et rajouter à l'interieur du dossier un fichier requirements.txt contenant :

```coppeliasim-zmqremoteapi-client > 2 # Since CoppeliaSim 4.6.0```
 
Donc on va avoir un seul dossier qui va avoir notre fichier **drone.ttt** qui représente la scène crée sur CoppeliaSim qu'on a enregistré sous le nom de "drone" , un fichier **movingdrone.py** et un fichier **requirements.txt**
Pour exécuter le code on le fait avec cette ligne la : ```python .\movingdrone.py```

On peut donc dire qu'à partir d'un code python simple on peut: 

> Modifier des scènes

> Faire déplacer des objets

> Récuperer des valeurs des capteurs


![Simulation](/assets/images/sim.png "Exécution d'une scène")


Donc comme application réelle j'ai choisi de faire du Drone Painting, c'est une scène qui contient deux drones et faire en sorte qu'ils volent vers un mur et dessinent des points selon mes indications (ils peuvent former un rectangle par exemple)

Lancer la simulation en mode stepped pour avoir une simulation déterministe et reproductible (la simulation en mode stepped est plus lente mais c'est reproductible)


***TIPS COPPELIASIM***

-	Toujours enregistrer la scène avant de lancer la simulation sinon tous les objets que vous avez rajoutés ou toutes modifications apportées seront disparus

-	Toujours arrêter la simulation en cours avant de lancer une nouvelle simulation 

-	Si vous avez ouvert plusieurs scènes à la fois, arrêtez la simulation de toutes les scènes avant de lancer une nouvelle simulation

-	Si vous voulez déplacer un objet avec la souris cliquez sur ça ![position](/assets/images/position.png "position") , il y aura même une petite fenêtre qui va s'afficher pour modifier la valeur de x, y ou z si souhaité.

