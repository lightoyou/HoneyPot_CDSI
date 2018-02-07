# Honey_CDSI
----------------------------------
# Introduction
Ce projet est un HoneyPot dédié aux Industrial Control Système- ICS.
L'Objectif est de fournir un moyen de collecter des données permettant de comprendre les motivations, les méthodes utilisé par des adversaires essayant d'attaquer ce type de système industriel et particulièrement le protocole ModBus.

# Vidéo Démonstration
[![IMAGE ALT TEXT](http://img.youtube.com/vi/JF7ICV8LGU8/0.jpg)](http://www.youtube.com/watch?v=JF7ICV8LGU8 "Demonstration")


# Infrastructure
![schéma](/doc/img/_ARCHI.png)

## Explications
Le projet se base sur la Stack ELK.

La stack ELK est une solution open source, de la société elastic,composée de trois produits que sont Elasticsearch, Logstash et Kibana, qui permettent de parser, indexer et présenter de gros volumes de données issues de vos logs sous forme de dashbords et de faire des recherches au sein de vos logs comme vous pourriez le faire avec un moteur de recherche.

Schématiquement le processus de fonctionnement de la stask est le suivant :
![schéma](/doc/img/elk.jpg)
![schéma](/doc/img/archi2.png)

## Elasticsearch
![schéma](/doc/img/elastic.png)

Elasticsearch est un puissant moteur d'indexation qui se base sur le projet Apache Lucene mais qui en simplifie l'utilisation. Il permet via une API Rest d'indexer et d'interroger facilement à l'aide de requêtes au format JSON les documents stockés dans une base nosql adaptée pour traiter de très gros volumes de données suivant des critères d'indexation complètement paramétrables afin d'optimiser les recherches.

## Elasticsearch
![schéma](/doc/img/logstash.jpg)
Logstash est un très bon outil permettant de collecter, analyser, formater et redistribuer des flux de chaines de caractères, des logs par exemple, via des fichiers de configuration et des plugins. Les points d'entrée de logstash sont définis dans des fichiers de configuration, ils peuvent être de nature variée via des plugins, presque une cinquantaine (ex : jdbc, nosql, fichiers, flux http, streams twitter, csv, syslog...). Logstash parse les  lignes de données qui sont ensuite traitées par des filtres pour filtrer mais également transformer les entrants, via des plugins, afin de les restituer dans un format attendu par le consommateur qui le traitera. Là encore les possibilités de sorties, via des plugins, sont multiples, près d'une soixantaine  (ex :  elasticsearch, jira, websocket, cvs, nosql ...)

## Kibana
![schéma](/doc/img/kibana.jpg)
Kibana est une interface web riche qui permet de présenter sous forme de dashboards des documents issus d'index Elastisearch. Kibana offre de nombreuses possibilités de représentations graphiques des données et cela de manière rapide et simple, pouvant être partagées avec l'ensemble des membres d'une équipe. Les données affichées peuvent être affinées en temps réel grâce à un système filtres et de requêtage.

# Scripts attaques
Les scripts d'attaques sont dans le dossier modbus.

# Installation facile avec Docker
## Depuis les sources
1. Installer Docker 'documentation installation Docker community edition'
2. Cloner ce répository via
```git clone
https://github.com/lightoyou/HoneyPot_CDSI.git```
