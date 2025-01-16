import streamlit as st

def berechne_altersvorsorge_rate(rentenluecke, rente_ab, zins, einsparjahre):
    rentendauer_monate = (85 - rente_ab) * 12
    monatlicher_zins = zins / 12
    anzahl_monate = einsparjahre * 12
    monatliche_rate = (rentenluecke * rentendauer_monate * monatlicher_zins) / (
        (1 + monatlicher_zins) ** anzahl_monate - 1
    )
    return monatliche_rate

st.title("Altersvorsorge-Rechner")
rentenluecke = st.number_input("Rentenlücke (€):", min_value=0.0, step=100.0)
rente_ab = st.number_input("Rente ab (Alter):", min_value=0, step=1)
zins = st.number_input("Zinssatz (%):", min_value=0.0, step=0.1) / 100
einsparjahre = st.number_input("Einsparjahre:", min_value=0, step=1)

if st.button("Berechnen"):
    rate = berechne_altersvorsorge_rate(rentenluecke, rente_ab, zins, einsparjahre)
    st.write(f"Die monatliche Rate beträgt: {rate:.2f} €")
