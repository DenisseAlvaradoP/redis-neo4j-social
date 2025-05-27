# Proyecto Big Data: Red Social con Redis y Neo4j  
# Big Data Project: Social Network with Redis and Neo4j

---

## Objetivo del proyecto  
## Project Objective

El objetivo de este proyecto es desarrollar un prototipo funcional de un sistema de red social que permita gestionar usuarios, publicaciones y relaciones entre usuarios utilizando tecnologías Big Data NoSQL, concretamente Redis para almacenamiento rápido y Neo4j para modelar relaciones en grafos. 

This project aims to develop a functional prototype of a social network system that manages users, posts, and user relationships using Big Data NoSQL technologies, specifically Redis for fast storage and Neo4j to model graph relationships.

Esto permitirá evaluar la aplicación práctica de bases de datos NoSQL y arquitecturas adecuadas para escenarios sociales con grandes volúmenes de datos y conexiones complejas.

This will allow evaluating the practical application of NoSQL databases and suitable architectures for social scenarios with large volumes of data and complex connections.

---

## Descripción del problema  
## Problem Description

Las redes sociales requieren manejar datos heterogéneos, con relaciones dinámicas y acceso rápido a publicaciones y conexiones. Las bases de datos tradicionales pueden presentar limitaciones para estos casos. Por eso, se propone usar Redis y Neo4j combinados para explotar sus fortalezas.

Social networks require managing heterogeneous data, with dynamic relationships and fast access to posts and connections. Traditional databases can show limitations for these cases. Therefore, the proposal is to use Redis and Neo4j combined to leverage their strengths.

---

## Tecnologías usadas  
## Technologies Used

- Redis (almacenamiento clave-valor y listas para posts)  
- Redis (key-value storage and lists for posts)
- Neo4j (base de datos de grafos para relaciones sociales)  
- Neo4j (graph database for social relationships)
- Flask (framework backend en Python)  
- Flask (backend framework in Python)
- python-dotenv (manejo seguro de variables de entorno)  
- python-dotenv (secure environment variable handling)

---

## Arquitectura general  
## General Architecture

- Backend en Flask expone API REST para crear usuarios, posts, y seguir usuarios.  
- Flask backend exposes REST API to create users, posts, and follow users.
- Redis guarda posts y datos rápidos.  
- Redis stores posts and fast-access data.
- Neo4j guarda usuarios y relaciones de seguimiento.  
- Neo4j stores users and follower relationships.

---

## Cómo ejecutar el proyecto  
## How to run the project

1. Clonar el repositorio  
   Clone the repository
2. Crear un entorno virtual e instalar dependencias:  
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1  # o source venv/bin/activate en Linux/Mac
   pip install -r requirements.txt
