# 📊 QueryGenius

## 🚀 Présentation du Projet
QueryGenius est une application interactive conçue pour simplifier le nettoyage, la transformation et la visualisation des données grâce à un chatbot alimenté par un **Large Language Model (LLM)**. L'objectif est de permettre aux utilisateurs de charger un dataset brut, de l'améliorer avec des transformations adaptées, puis d'utiliser le chatbot pour générer des visualisations adaptées aux besoins de l'analyse.

## 🏗️ Fonctionnalités Principales
### 1️⃣ **Chargement et Détection Automatique du Format des Données**
- Prise en charge des fichiers **CSV, Excel, JSON et PDF**.
- Détection automatique de l'encodage des fichiers pour éviter les erreurs de lecture.
- Extraction du texte des fichiers PDF et transformation en dataframe exploitable.

### 2️⃣ **Transformation et Nettoyage des Données**
- **Résumé du dataset** : aperçu des statistiques clés (nombre de lignes, valeurs manquantes, doublons, types de données).
- **Traitement des valeurs manquantes** : possibilité de les remplacer par la moyenne, la médiane, la valeur la plus fréquente, ou de supprimer les lignes incomplètes.
- **Gestion des doublons** : suppression optionnelle des lignes dupliquées.
- **Détection et traitement des outliers** :
  - Aucune action
  - Transformation logarithmique
  - Remplacement par la moyenne/médiane
  - Suppression des lignes contenant des valeurs aberrantes

### 3️⃣ **Génération Automatique de Visualisations**
- **Interaction avec un chatbot LLM** (Claude) pour comprendre la requête utilisateur et proposer une visualisation adaptée.
- **Sélection intelligente du type de graphique** basé sur les données fournies et la requête.
- **Génération de code Python avec Plotly** pour afficher la visualisation directement dans Streamlit.

### 4️⃣ **Téléchargement des Données Transformées**
- Export des données nettoyées sous forme de fichier CSV.

## 🛠️ Technologies Utilisées
- **Python** : Langage principal pour le traitement des données et l'interfaçage avec l'API LLM.
- **Streamlit** : Développement de l'interface utilisateur interactive.
- **Pandas & NumPy** : Manipulation et transformation des données.
- **Matplotlib & Seaborn** : Visualisation des données.
- **Plotly** : Graphiques interactifs générés automatiquement.
- **Anthropic Claude API** : Intégration du chatbot d'intelligence artificielle.

## 🏁 Comment Utiliser QueryGenius ?
### 🔹 1.Clone repository
```bash
git clone https://github.com/Meriam-Inoubli/DataViz-LLM
cd DataViz-LLM
```

### 🔹 2. Install dependencies using Poetry:

```bash
poetry install
```
### 🔹 3.Activate the virtual environment:


```bash
poetry shell
```
### 🔹 4.Run the Streamlit application:
```bash
streamlit run src\dataviz_project\app.py
```
### 🔹 3. Utilisation de l'application
1. **Charger un fichier** (CSV, Excel, JSON, PDF).
2. **Appliquer des transformations** (gestion des valeurs manquantes, des doublons, des outliers).
3. **Télécharger le fichier transformé** pour une utilisation ultérieure.
4. **Utiliser le chatbot** pour générer des visualisations automatiques et obtenir des insights sur vos données.

## 💡 Auteurs & Encadrement
Projet réalisé par :
- **Kabeda Hiba** - hiba.kabeda@dauphine.eu
- **Inoubli Meriam** - meriam.inoubli@dauphine.eu

Encadré par :
- **Professeur Hadrien Mariaccia**

---
✉️ N'hésitez pas à nous contacter pour toute question ou suggestion !
