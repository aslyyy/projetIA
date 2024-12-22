import streamlit as st
import joblib
import os
import uuid

# Dossier pour stocker les fichiers uploadés
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Crée automatiquement le dossier si nécessaire

# Charger le modèle
model = joblib.load("model.pkl")

# Fonction pour extraire les caractéristiques
def extract_features(filepath):
    try:
        features = {
            "size": os.path.getsize(filepath),
            "name_length": len(os.path.basename(filepath)),
            "is_executable": filepath.endswith(".exe"),
            "dummy_feature_1": 0,
            "dummy_feature_2": 0,
            "dummy_feature_3": 0,
            "dummy_feature_4": 0,
            "dummy_feature_5": 0,
            "dummy_feature_6": 0,
        }
        return features
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des caractéristiques : {e}")
        return None

# Titre de l'application
st.title("Détection de Malware avec Machine Learning")

# Section de téléversement du fichier
st.header("Téléversez un Fichier Exécutable")
uploaded_file = st.file_uploader("Choisissez un fichier exécutable", type=["exe"])

if uploaded_file:
    # Générer un chemin unique pour le fichier
    unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    # Sauvegarder temporairement le fichier
    try:
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extraire les caractéristiques
        features = extract_features(filepath)
        if features is None:
            st.error("Impossible d'extraire les caractéristiques.")
        else:
            # Afficher les caractéristiques dans des colonnes
            st.subheader("Caractéristiques Extraites")
            col1, col2, col3 = st.columns(3)
            col1.write(f"Taille: {features['size']} octets")
            col2.write(f"Longueur du Nom: {features['name_length']}")
            col3.write(f"Est Exécutable: {features['is_executable']}")
            col1.write(f"Caractéristique 1: {features['dummy_feature_1']}")
            col2.write(f"Caractéristique 2: {features['dummy_feature_2']}")
            col3.write(f"Caractéristique 3: {features['dummy_feature_3']}")
            col1.write(f"Caractéristique 4: {features['dummy_feature_4']}")
            col2.write(f"Caractéristique 5: {features['dummy_feature_5']}")
            col3.write(f"Caractéristique 6: {features['dummy_feature_6']}")

            # Faire une prédiction
            prediction = model.predict([list(features.values())])
            result = "Malware" if prediction[0] == 1 else "Non Malware"

            # Afficher le résultat dans une métrique
            st.subheader("Résultat de la Détection")
            st.write(f"Statut : {result}")

    except Exception as e:
        st.error(f"Erreur : {e}")
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(filepath):
            os.remove(filepath)  # Nettoyage des fichiers temporaires
