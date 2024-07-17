# Introduction
Dans le cadre des travaux de recherche menés au LDR sur les plateformes embarquées, les chercheurs souhaitent mettre en place des environnements de développements et de tests plus récents et robustes pour 2 applications en particulier, dans l’ordre d’importance :  

- La programmation embarquée, en particulier avec OS Temps Réel. 
Mettre en place un environnement de dev/tests avec sondes logicielles pour le temps réel. Pour réaliser des tests de systèmes contraints, possiblement utilisant des architectures matérielles diverses (ARM, RISC-V, etc.), les chercheurs ont besoin d’un environnement clair, générant des traces analysables (quantité de mémoire utilisée, temps passé sur le processeur et lors des accès aux périphériques, décisions d’ordonnancement, etc.).

- Simulateur pour robotique/drone. 
Mettre en place un environnement de dev/tests avec, par exemple CoppeliaSim et Python/ROS, génération de scénario et récupération des données de vol et de l’environnement simulé.  
Différents travaux sont réalisés depuis plusieurs années avec l’ONERA sur des simulations utilisant de drones. Ces travaux utilisent d’anciens simulateurs difficiles à maintenir aujourd’hui, ce qui rend complexe la reproduction de certains résultats. Plusieurs exemples existent pour des applications spécifiques, comme avec le robot Poppy et ROS.

La documentation de la partie "Simulation" est disponible dans le dossier LDR_Simulation