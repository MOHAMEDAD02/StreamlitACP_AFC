import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Simulation du système M/M/1")
st.sidebar.header("Entrée des données")

# Paramètres d'entrée
simulation_temps = st.sidebar.number_input("Temps de simulation (minutes)", min_value=1, value=100, step=1)
num_pieces = st.sidebar.number_input("Nombre de pièces", min_value=1, value=20, step=1)

# Distributions basées sur les données fournies
inter_arrivees = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Temps inter-arrivées (en minutes)
proba_inter_arrivees = np.array([0.1] * 10)  # Probabilités associées

service_times = np.array([2, 3, 4, 5])  # Temps de service (en minutes)
proba_service_times = np.array([0.25, 0.25, 0.25, 0.25])  # Probabilités associées

# Génération des temps d'inter-arrivées et de service
np.random.seed(42)  # Pour la reproductibilité
a = np.random.choice(inter_arrivees, size=num_pieces, p=proba_inter_arrivees)  # Temps d'inter-arrivées
s = np.random.choice(service_times, size=num_pieces, p=proba_service_times)  # Temps de service

# Calcul des paramètres du système
lambda_ = 1 / np.mean(a)  # Taux d'arrivée moyen
mu = 1 / np.mean(s)       # Taux de service moyen
rho = lambda_ / mu        # Taux d'occupation du serveur

# Formules analytiques
P0_analytique = 1 - rho
L_analytique = rho / (1 - rho)
Lq_analytique = rho**2 / (1 - rho)
W_analytique = 1 / (mu * (1 - rho))
Wq_analytique = rho / (mu * (1 - rho))

# Simulation
arrivees = np.cumsum(a)  # Temps d'arrivée des pièces
b = np.zeros(num_pieces)  # Temps de début de service
c = np.zeros(num_pieces)  # Temps de fin de service

timeline = np.arange(0, simulation_temps, 0.1)
clients_dans_file = np.zeros(len(timeline))
clients_dans_systeme = np.zeros(len(timeline))
serveur_occupe = np.zeros(len(timeline))

for i in range(num_pieces):
    if i == 0:
        b[i] = arrivees[i]
    else:
        b[i] = max(arrivees[i], c[i - 1])
    c[i] = b[i] + s[i]
    if c[i] > simulation_temps:
        c[i] = simulation_temps

    for t_idx, t in enumerate(timeline):
        if arrivees[i] <= t < b[i]:
            clients_dans_file[t_idx] += 1
        if arrivees[i] <= t < c[i]:
            clients_dans_systeme[t_idx] += 1
        if b[i] <= t < c[i]:
            serveur_occupe[t_idx] = 1

# Estimations par simulation
proportion_serveur_libre_sim = 1 - np.mean(serveur_occupe)
moy_clients_dans_file_sim = np.mean(clients_dans_file)
moy_clients_dans_systeme_sim = np.mean(clients_dans_systeme)
moy_duree_sejour_sim = np.mean([c[i] - arrivees[i] for i in range(num_pieces)])

# Affichage des résultats
st.subheader("Résultats analytiques avec formules")
st.write(f"**Proportion de temps où le serveur est libre (analytique) :** {P0_analytique:.2f}")
st.write(f"**Nombre moyen de clients dans le système (analytique) :** {L_analytique:.2f}")
st.write(f"**Nombre moyen de clients dans la file (analytique) :** {Lq_analytique:.2f}")
st.write(f"**Durée moyenne de séjour dans le système (analytique) :** {W_analytique:.2f} minutes")
st.write(f"**Durée moyenne de séjour dans la file (analytique) :** {Wq_analytique:.2f} minutes")

st.subheader("Résultats par simulation")
st.write(f"**Proportion de temps où le serveur est libre (simulation) :** {proportion_serveur_libre_sim:.2f}")
st.write(f"**Nombre moyen de clients dans le système (simulation) :** {moy_clients_dans_systeme_sim:.2f}")
st.write(f"**Nombre moyen de clients dans la file (simulation) :** {moy_clients_dans_file_sim:.2f}")
st.write(f"**Durée moyenne de séjour dans le système (simulation) :** {moy_duree_sejour_sim:.2f} minutes")

# Courbes d'évolution
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(timeline, clients_dans_file, label="Clients dans la file", color="orange")
ax.plot(timeline, clients_dans_systeme, label="Clients dans le système", color="blue")
ax.plot(timeline, serveur_occupe, label="État du serveur (1=occupé)", color="green")
ax.set_xlabel("Temps (minutes)")
ax.set_ylabel("Nombre de clients / État")
ax.set_title("Évolution des métriques du système M/M/1")
ax.legend()
ax.grid(True)
st.pyplot(fig)
