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

# Titel und Sub-Headline
st.title("📊 Altersvorsorge-Rechner")
st.markdown("### Haben Sie sich schon mal mit Ihrer Alterslücke beschäftigt? 🤔💸")
st.markdown(
    """
    Ich errechne Ihnen jetzt ganz genau, was Sie bezahlen müssen, um Ihre Lücke zu schließen. 
    **Bitte gönnen Sie 90% auf lock!** 🚀✨
    """
)

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

    # Berechnungen für die Visualisierung
    jahre = list(range(1, einsparjahre + 1))
    eigenbeitraege = [rate * 12 * jahr for jahr in jahre]
    gesamtkapital = [(rate * ((1 + (zins / 12)) ** (jahr * 12) - 1) / (zins / 12)) for jahr in jahre]
    zinsen = [gesamtkapital[i] - eigenbeitraege[i] for i in range(len(jahre))]

    # Visualisierung
    plt.figure(figsize=(10, 6))
    plt.plot(jahre, gesamtkapital, label="Gesamtkapital", color="green", marker="o")
    plt.plot(jahre, eigenbeitraege, label="Eigenbeitrag", color="blue", linestyle="--")
    plt.fill_between(jahre, eigenbeitraege, gesamtkapital, color="orange", alpha=0.3, label="Zinsen")
    plt.title("Gesamtes angespartes Kapital über die Jahre", fontsize=16)
    plt.xlabel("Jahre", fontsize=12)
    plt.ylabel("Kapital (€)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    st.pyplot(plt)

    # Zusätzliche Textausgabe für das Endkapital
    st.markdown(f"### Ergebnis")
    st.markdown(f"- **Angespartes Gesamtkapital:** {gesamtkapital[-1]:,.2f} €")
    st.markdown(f"- **Eigenbeiträge:** {eigenbeitraege[-1]:,.2f} €")
    st.markdown(f"- **Erwirtschaftete Zinsen:** {zinsen[-1]:,.2f} €")

