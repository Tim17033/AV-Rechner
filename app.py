import streamlit as st
import matplotlib.pyplot as plt
import time

# Berechnung der Altersvorsorge
def berechne_altersvorsorge_rate(rentenluecke, rente_ab, zins, einsparjahre):
    rentendauer_monate = (85 - rente_ab) * 12
    monatlicher_zins = zins / 12
    anzahl_monate = einsparjahre * 12
    monatliche_rate = (rentenluecke * rentendauer_monate * monatlicher_zins) / (
        (1 + monatlicher_zins) ** anzahl_monate - 1
    )
    return monatliche_rate

# Berechnung der 12/62-Regel
def berechne_12_62_kapital(gesamtkapital, zins_ertrag):
    steuerfrei = zins_ertrag / 2  # Nur die Hälfte der Zinserträge wird versteuert
    steuerbelastung = steuerfrei * 0.25  # Kapitalertragssteuer von 25%
    netto_kapital = gesamtkapital - steuerbelastung
    return netto_kapital, steuerfrei, steuerbelastung

# Styling für rote, animierte Buttons
button_style = """
    <style>
    .red-button {
        background-color: #ff4b4b;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px 2px;
        cursor: pointer;
        border-radius: 5px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #ff4b4b; }
        50% { box-shadow: 0 0 20px #ff4b4b; }
        100% { box-shadow: 0 0 5px #ff4b4b; }
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

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
    rentenluecke = st.number_input("Rentenlücke (€):", min_value=0.0, step=100.0, key="rentenluecke")
    rente_ab = st.number_input("Rente ab (Alter):", min_value=0, step=1, key="rente_ab")
with col2:
    zins = st.number_input("Zinssatz (%):", min_value=0.0, step=0.1, key="zins") / 100
    einsparjahre = st.number_input("Einsparjahre:", min_value=0, step=1, key="einsparjahre")

# Berechnung starten
if st.button("🎯 Berechnung starten", key="berechnen"):
    with st.spinner("Berechnung Ihrer Alterslücke... Bitte warten! ⏳"):
        time.sleep(2)  # Simulierte Ladezeit

    # Altersvorsorgeberechnung
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

    # Berechnung der 12/62-Regel
    kapital_entnahme = gesamtkapital[-1]  # Gesamtkapital bei Renteneintritt
    netto_kapital, steuerfrei, steuerbelastung = berechne_12_62_kapital(kapital_entnahme, zinsen[-1])

    st.write("---")
    st.markdown("### Kapitalentnahme mit 12/62-Regel 💼")
    st.markdown(
        """
        #### Erklärung der 12/62-Regel
        Wenn Sie mindestens 12 Jahre in den Vertrag eingezahlt haben und zum Zeitpunkt der Kapitalentnahme mindestens 62 Jahre alt sind, wird nur **die Hälfte der Zinserträge** mit der Kapitalertragssteuer von 25% besteuert.
        """
    )
    st.markdown(f"- **Brutto-Kapital:** {kapital_entnahme:,.2f} €")
    st.markdown(f"- **Steuerfreie Zinserträge:** {steuerfrei:,.2f} €")
    st.markdown(f"- **Steuerbelastung auf Zinserträge:** {steuerbelastung:,.2f} €")
    st.markdown(f"### 💰 **Netto-Kapital (nach Steuern): {netto_kapital:,.2f} €**")
