import streamlit as st
import matplotlib.pyplot as plt

def berechne_altersvorsorge_rate(rentenluecke, rente_ab, zins, einsparjahre):
    rentendauer_monate = (85 - rente_ab) * 12
    monatlicher_zins = zins / 12
    anzahl_monate = einsparjahre * 12
    monatliche_rate = (rentenluecke * rentendauer_monate * monatlicher_zins) / (
        (1 + monatlicher_zins) ** anzahl_monate - 1
    )
    return monatliche_rate

# App-Layout
st.title("📊 Altersvorsorge-Rechner")
st.write("Willkommen! Mit diesem Rechner kannst du ermitteln, wie viel du monatlich sparen musst, um deine Rentenlücke zu schließen.")
st.write("---")  # Trennlinie

# Eingabewerte in Spalten
col1, col2 = st.columns(2)
with col1:
    rentenluecke = st.number_input("Rentenlücke (€):", min_value=0.0, step=100.0)
    rente_ab = st.number_input("Rente ab (Alter):", min_value=0, step=1)
with col2:
    zins = st.number_input("Zinssatz (%):", min_value=0.0, step=0.1) / 100
    einsparjahre = st.number_input("Einsparjahre:", min_value=0, step=1)

# Ergebnisberechnung
if st.button("Berechnen"):
    rate = berechne_altersvorsorge_rate(rentenluecke, rente_ab, zins, einsparjahre)
    st.success(f"🎉 Die monatliche Sparrate beträgt: {rate:.2f} €")

    # Visualisierung
    jahre = list(range(1, einsparjahre + 1))
    beitraege = [rate * 12 * jahr for jahr in jahre]

    plt.figure(figsize=(8, 4))
    plt.plot(jahre, beitraege, marker="o")
    plt.title("Gesamte Sparsumme über die Jahre")
    plt.xlabel("Jahre")
    plt.ylabel("Sparsumme (€)")
    st.pyplot(plt)


