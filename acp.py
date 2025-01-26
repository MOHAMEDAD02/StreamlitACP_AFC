import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from prince import CA

# Configuration de la page
st.set_page_config(page_title="Analyse de données (ACP/AFC)", layout="wide")

# Titre de l'application
st.title("📊 Analyse de Données : ACP & AFC")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Chargement des données
    df = pd.read_csv(uploaded_file)
    st.sidebar.header("🔍 Aperçu des données")
    st.sidebar.write(df.head())

    # Analyse descriptive
    st.subheader("Analyse descriptive des données")
    st.write(df.describe())

    # Gestion des valeurs manquantes
    st.subheader("Gestion des valeurs manquantes")
    missing_values = df.isnull().sum()
    st.write(missing_values[missing_values > 0])

    if missing_values.sum() > 0:
        option_missing = st.radio("Comment gérer les valeurs manquantes ?", ("Supprimer les lignes", "Remplacer par la moyenne", "Remplacer par la médiane"))
        if option_missing == "Supprimer les lignes":
            df = df.dropna()
        elif option_missing == "Remplacer par la moyenne":
            df = df.fillna(df.mean())
        elif option_missing == "Remplacer par la médiane":
            df = df.fillna(df.median())
        st.success("Les valeurs manquantes ont été traitées.")

    # Sélection du type d'analyse
    analysis_type = st.sidebar.selectbox("Choisissez le type d'analyse", ["ACP", "AFC"])

    if analysis_type == "ACP":
        st.subheader("Analyse en Composantes Principales (ACP)")

        # Sélection des colonnes numériques
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        selected_cols = st.multiselect("Sélectionnez les colonnes pour l'ACP", num_cols, default=num_cols)

        if st.button("Effectuer l'ACP"):
            # Normalisation des données
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df[selected_cols])

            # Choix du nombre de composantes
            n_components = st.slider("Nombre de composantes à conserver :", 2, min(len(selected_cols), 10), 2)
            pca = PCA(n_components=n_components)
            principal_components = pca.fit_transform(df_scaled)

            # Résultat des composantes principales
            pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])
            st.write("Résultat des composantes principales :", pca_df.head())

            # Visualisation
            fig, ax = plt.subplots()
            sns.scatterplot(x=pca_df['PC1'], y=pca_df['PC2'], alpha=0.7)
            plt.title("Projection des données (ACP)")
            st.pyplot(fig)

            # Variance expliquée
            st.write("Variance expliquée par composante :", pca.explained_variance_ratio_)

            # Export des résultats
            st.download_button(label="Télécharger les résultats ACP", data=pca_df.to_csv().encode(), file_name="ACP_results.csv")

    elif analysis_type == "AFC":
        st.subheader("Analyse Factorielle des Correspondances (AFC)")

        # Sélection des colonnes catégoriques
        cat_cols = df.select_dtypes(include=['object']).columns
        selected_cols = st.multiselect("Sélectionnez les colonnes pour l'AFC", cat_cols, default=cat_cols)

        if st.button("Effectuer l'AFC"):
            ca = CA(n_components=2)
            df_cat = df[selected_cols]
            ca.fit(df_cat)

            # Transformation des données
            ca_result = ca.row_coordinates(df_cat)
            st.write("Résultat de l'AFC :", ca_result.head())

            # Visualisation
            fig, ax = plt.subplots()
            sns.scatterplot(x=ca_result[0], y=ca_result[1], alpha=0.7)
            plt.title("Projection des données (AFC)")
            st.pyplot(fig)

            # Export des résultats
            st.download_button(label="Télécharger les résultats AFC", data=ca_result.to_csv().encode(), file_name="AFC_results.csv")

    # Visualisation supplémentaire
    st.sidebar.subheader("📊 Visualisations des données")
    if st.sidebar.checkbox("Afficher la heatmap de corrélation"):
        st.subheader("Matrice de corrélation")
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)

    if st.sidebar.checkbox("Afficher les boxplots"):
        selected_box_col = st.sidebar.selectbox("Choisir une colonne pour le boxplot", df.select_dtypes(include=['float64', 'int64']).columns)
        st.subheader(f"Boxplot de {selected_box_col}")
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=df[selected_box_col])
        st.pyplot(plt)

    if st.sidebar.checkbox("Afficher la distribution des données"):
        selected_hist_col = st.sidebar.selectbox("Choisir une colonne pour l'histogramme", df.select_dtypes(include=['float64', 'int64']).columns)
        st.subheader(f"Distribution de {selected_hist_col}")
        plt.figure(figsize=(8, 4))
        sns.histplot(df[selected_hist_col], kde=True, bins=30)
        st.pyplot(plt)

else:
    st.write("Veuillez charger un fichier CSV pour commencer l'analyse.")


st.write("Veuillez charger un fichier CSV pour commencer l'analyse.")
