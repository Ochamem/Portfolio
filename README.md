# Analyste de données 
#### Compétences techniques : Python, SQL, PowerBI, Tableau, ETL, Knime, Excel
À l'origine, designer par passion ! je vous propose de partager mes compétences pour vous aider à transformer vos données abstraites en histoires visuelles.
> - Mes spécialités ? IT, data analyst , et la crème de la crème des nouvelles technos.
> - Mon super-pouvoir ? Je code en Python et SQL qui me permet de jongler avec les données avec une grande aisance.
> - Ma mission secrète ? Concevoir des tableaux de bord avec passion et créativité pour offrir une expérience utilisateur inégalée.
> - Mon objectif ? Continuer à progresser et à me perfectionner dans mon domaine.

## Mon Portfolio 
### Une application permettant de consulter des données sur les émissions de GES des véhicules en Europe via :
> - une API
> - une interface web

![image](https://github.com/Ochamem/portfolio/assets/145020975/ec8418c6-5431-4245-a57c-b778ccb6b7ad)

> Étapes clés
> - Extraction des données avec Selenium
> - Extract, transform & load des données avec Knime
> - Création d'une régression linéaire pour imputer les données manquantes
> - Analyse exploratoire des données (EDA)
> - Utilisation du clustering k-means
> - Détermination du meilleur modèle d'apprentissage automatique et prédiction réussie des émissions de GES des véhicules électriques en Europe
> - Conception et développement de l'interface utilisateur de l'application web en utilisant HTML, CSS et JavaScript.
> - Déploiement de l'application
> #### En savoir plus sur le projet [ICI](https://github.com/Ochamem/portfolio/tree/main/Projet%201).

### Une application pour gérer votre compte Sellsy à l'aide de Python:
![image](https://github.com/Ochamem/portfolio/assets/145020975/9ad4ce28-6b4c-44f5-ad0c-7f4dd6ff8a5d)

> Étapes clés
> - Vous permet de vous connecter avec vos clés API privées Oauth
> - Accès à toutes les méthodes répertoriées [ici](https://api.sellsy.com/documentation/methods) avec une seule fonction
> - Gestionnaire d'erreur
> - création des datamarts plus ciblé et plus convivial pour les consommer dans des rapports.
> - Création des maquettes par Figma pour valider la direction de la visualisation avant la phase d'implémentation complète.
> - Implémentation les tableaux de bord avec Power BI
> #### En savoir plus sur le projet [ICI](https://github.com/Ochamem/portfolio/tree/main/Projet%202).

### Une application pour classification d'image:
![image](https://github.com/Ochamem/portfolio/assets/145020975/dc4e3b05-e299-4063-8238-a00991cdc25c)

### Cloner Netflix avec DataStax DB et GraphQL:
![image](https://github.com/Ochamem/portfolio/assets/145020975/4902f80f-7c5d-4447-8b65-6293a318792d)

Un simple clone de page d'accueil ReactJS Netflix exécuté sur DataStax DB qui exploite l'API GraphQL avec pagination et défilement infini.

Voir la présentation vidéo [Resultat Final](https://glittery-twilight-7ada8e.netlify.app/) de ce qu'on va construire !

> Objectifs
> - Créez et exécutez un clone Netflix.
> - Découvrez l'API GraphQL et comment l'utiliser avec une base de données pour créer les tables et parcourir les données.
> - En savoir plus sur la pagination et le défilement infini dans une interface utilisateur Web.
> - Tirez parti de Netlify et de DataStax Astra DB.
> - Déployez le clone Netflix en production avec Netlify.
<details><summary>C'est quoi Graphql</summary>
GraphQL est un langage de requête de données open source développé par Facebook en 2012 pour simplifier la communication entre les applications frontales et les serveurs de données. Contrairement aux API REST traditionnelles, GraphQL permet aux clients de spécifier précisément les données dont ils ont besoin, ce qui évite le surchargement de l'API avec des requêtes multiples et redondantes.

Avec GraphQL, les clients peuvent interroger une API pour récupérer uniquement les données nécessaires à leur application, ce qui peut réduire considérablement la quantité de données transférées et améliorer les performances. GraphQL fournit également une documentation complète pour l'API, ce qui facilite la compréhension et l'utilisation de l'API par les développeurs.

En somme, GraphQL est un langage de requête flexible et efficace pour les API qui permet aux clients de spécifier exactement les données dont ils ont besoin, en évitant le gaspillage de ressources et en améliorant les performances.

</details>
# Commençons

## Table des matières

### Partie I - Configuration de la base de données et ingestion de données
1. [Créer une instance de base de données DataStax](#1-login-or-register-to-astradb-and-create-database)
2. [Créer un jeton de sécurité](#2-create-a-security-token)
3. [Créer une table pour les genres avec GraphQL](#3-create-table-for-genres-with-graphql)
4. [Insérer les données de genre avec GraphQL](#4-insert-genre-data-with-graphql)
5. [Récupérer les genres avec GraphQL](#5-retrieve-genres-with-graphql)
6. [Créer une table pour les films](#6-create-a-table-for-movies)
7. [Insérer quelques films](#7-insérer-quelques-films)
8. [Récupérer des films : pagination](#8-récupérer-films-pagination)

### Partie 2 – Créer et déployer le front-end

1. [Déployer l'interface graphique squelettique sur Netlify](#1-deploy-skeletal-gui-to-netlify)
2. [Lancez Gitpod depuis VOTRE dépôt Github](#2-launch-gitpod-from-your-github-repo)
3. [Configurer et utiliser `astra-cli`](#3-set-up-and-use-astra-cli)
4. [Fonctions sans serveur](#4-fonctions-sans-serveur)
5. [Récupération depuis le front-end](#5-fetching-from-the-front-end)
6. [Installer la CLI Netlify](#6-install-the-netlify-cli)
7. [Fournir les paramètres de connexion à la base de données](#7-provide-db-connection-parameters)
8. [Exécuter l'application en mode dev](#8-run-the-app-in-dev-mode)
9. [Connect to your Netlify site](#9-connect-to-your-netlify-site)
10. [Déployer en production !](#10-deploy-in-production)



