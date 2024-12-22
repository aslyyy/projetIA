import streamlit as st
import joblib
import os
import uuid  # Pour des noms de fichier uniques

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
            # Remplacez ou ajoutez vos vraies caractéristiques ici
            "dummy_feature_1": 0,
            "dummy_feature_2": 0,
            "dummy_feature_3": 0,
            "dummy_feature_4": 0,
            "dummy_feature_5": 0,  # Ajout d'une 8e caractéristique
            "dummy_feature_6": 0,  # Ajout d'une 9e caractéristique
        }
        return list(features.values())
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des caractéristiques : {e}")
        return None

# Interface utilisateur avec Streamlit
st.title("Détection de Malware avec Machine Learning")

# Upload du fichier
uploaded_file = st.file_uploader("Téléchargez un fichier exécutable", type=["exe"])

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
            # Afficher les caractéristiques
            st.write("Caractéristiques extraites :", features)
            
            # Faire une prédiction
            prediction = model.predict([features])
            result = "Malware" if prediction[0] == 1 else "Légitime"
            
            # Afficher le résultat
            st.success(f"Résultat : {result}")
    except Exception as e:
        st.error(f"Erreur : {e}")
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(filepath):
            os.remove(filepath)  # Nettoyage des fichiers temporaires
