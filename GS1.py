import random
import matplotlib.pyplot as plt
import streamlit as st
import re
strategies = [(10, 40), (20, 60), (30, 70), (40, 80)]  
h = 2   
p = 5   
L = 220 
c = 23  
N = 12  
demande = [15, 45, 15, 20, 15, 30, 45, 50, 10, 15, 20, 30]
def simulation(s, S):
    stock_t = S  
    cout_possession = 0
    cout_penurie = 0
    cout_passation = 0

    evolution_stock = []  
    quantites_commandees = []  
    couts_totaux = []  
    for t in range(N):
        demande_t = demande[t]  
        stock_t -= demande_t  
        if stock_t <= s:
            quantite_commandee = S - stock_t
            cout_passation += L
            stock_t = S 
        else:
            quantite_commandee = 0
        if stock_t < 0:
            cout_penurie += abs(stock_t) * p
            stock_t = 0  
        cout_possession += stock_t * h
        evolution_stock.append(stock_t)
        quantites_commandees.append(quantite_commandee)
        cout_total = cout_possession + cout_penurie + cout_passation
        couts_totaux.append(cout_total)

    return {
        "evolution_stock": evolution_stock,
        "quantites_commandees": quantites_commandees,
        "couts_totaux": couts_totaux,
        "cout_possession": cout_possession,
        "cout_penurie": cout_penurie,
        "cout_passation": cout_passation,
    }
st.title("Analyse des stratégies de gestion des stocks (s, S)")
st.markdown("""
    <style>
        .signature {
            font-size: 24px;
            font-weight: bold;
            color: #2e3a87;
            text-align: center;
            font-family: 'Arial', sans-serif;
            padding: 20px;
            border-top: 3px solid #2e3a87;
            margin-top: 20px;
        }
    </style>
    <div class="signature">par MOHAMED ABID</div>
""", unsafe_allow_html=True)
s = st.number_input("Entrez la valeur de s", min_value=0, value=10)
S = st.number_input("Entrez la valeur de S", min_value=0, value=40)
resultats = {}
for strategy in strategies + [(s, S)]:
    resultats[strategy] = simulation(*strategy)
view_all = st.checkbox("Afficher toutes les stratégies simultanément")
if view_all:
    fig_stock, ax_stock = plt.subplots(figsize=(12, 8))
    for strategy in strategies + [(s, S)]:
        label = f"(s={strategy[0]}, S={strategy[1]})"
        ax_stock.plot(range(1, N+1), resultats[strategy]["evolution_stock"], marker='o', label=label)
    ax_stock.set_title("Évolution du stock pour toutes les stratégies")
    ax_stock.set_xlabel("Période")
    ax_stock.set_ylabel("Niveau de stock")
    ax_stock.legend()
    ax_stock.grid()
    st.pyplot(fig_stock)
    fig_cost, ax_cost = plt.subplots(figsize=(12, 8))
    total_costs = [sum(resultats[strategy]["couts_totaux"]) for strategy in strategies + [(s, S)]]
    labels = [f"(s={strategy[0]}, S={strategy[1]})" for strategy in strategies + [(s, S)]]
    ax_cost.bar(labels, total_costs, color='skyblue', alpha=0.8)
    ax_cost.set_title("Coûts totaux pour toutes les stratégies")
    ax_cost.set_xlabel("Stratégie (s, S)")
    ax_cost.set_ylabel("Coût total")
    ax_cost.set_xticklabels(labels, rotation=45, ha="right")
    st.pyplot(fig_cost)
else:
    strategies_labels = [f"(s={s}, S={S})" for s, S in strategies + [(s, S)]]
    selected_strategy = st.selectbox("Choisissez une stratégie à visualiser", strategies_labels)
    match = re.search(r"\(s=(\d+), S=(\d+)\)", selected_strategy)
    if match:
        selected_strategy_values = (int(match.group(1)), int(match.group(2)))
    else:
        st.error("Erreur : Impossible d'extraire les valeurs de la stratégie sélectionnée.")
    data = resultats[selected_strategy_values]
    fig, axes = plt.subplots(3, 1, figsize=(12, 16))
    axes[0].plot(range(1, N+1), data["evolution_stock"], marker='o', color='blue')
    axes[0].set_title("Évolution du stock au cours des périodes")
    axes[0].set_xlabel("Période")
    axes[0].set_ylabel("Niveau de stock")
    axes[0].grid()
    axes[1].bar(range(1, N+1), data["quantites_commandees"], color='green', alpha=0.7)
    axes[1].set_title("Quantités commandées à chaque période")
    axes[1].set_xlabel("Période")
    axes[1].set_ylabel("Quantité commandée")
    axes[1].grid()
    axes[2].plot(range(1, N+1), data["couts_totaux"], marker='o', color='red')
    axes[2].set_title("Évolution des coûts totaux au cours des périodes")
    axes[2].set_xlabel("Période")
    axes[2].set_ylabel("Coût total")
    axes[2].grid()
    st.pyplot(fig)
    st.write(f"**Résumé des coûts pour la stratégie {selected_strategy}:**")
    st.write(f"- Coût total de possession : {data['cout_possession']}")
    st.write(f"- Coût total de pénurie    : {data['cout_penurie']}")
    st.write(f"- Coût total de passation  : {data['cout_passation']}")
    st.write(f"- **Coût total global**    : {sum(data['couts_totaux'])}")
comparaison = []
for strategy, data in resultats.items():
    cout_total = sum(data["couts_totaux"])
    cout_moyen = cout_total / N
    nb_penuries = len([stock for stock in data["evolution_stock"] if stock == 0])
    taux_satisfaction = (sum(demande) - sum([abs(stock) for stock in data["evolution_stock"] if stock < 0])) / sum(demande)
    comparaison.append({
        "Stratégie": strategy,
        "Coût total": cout_total,
        "Coût moyen": cout_moyen,
        "Nb pénuries": nb_penuries,
        "Taux satisfaction": taux_satisfaction,
    })

st.write("**Comparaison des stratégies :**")
st.table(comparaison)

meilleure_strategie = min(comparaison, key=lambda x: x["Coût total"])
st.write(f"**Meilleure stratégie (selon le coût total) : {meilleure_strategie['Stratégie']}**")


