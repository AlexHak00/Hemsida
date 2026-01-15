import streamlit as st
import pandas as pd

from varderingsapp_v2 import value_stock, valuation_interval

st.set_page_config(page_title="Min Streamlit App", page_icon=":smiley:", layout="centered")

st.title(" :blue[Magiska] värderingsmodellen")

st.markdown("""
** Värderingsmodell baserad på: **
- Vinst per aktie (EPS)
- Vinsttillväxt (%)
- Avkastningskrav (%)
- Säkerhetsmarginal
""")
st.divider()

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

with st.container():
    st.header("Ange parametrar för värdering")
    st.markdown("Fyll i nedanstående fält för att beräkna det")

col1, col2 = st.columns(2)

with col1: 
    eps = st.number_input("Nuvarande EPS: (exempelvis 5.0)", min_value=1, value=1, max_value=500)
with col2: 
    growth = st.selectbox("Vinsttillväxt ett år framåt (%)", [5, 6 , 8, 10, 12, 15, 18, 20])
required_return = st.selectbox("Avkastningskrav (%)", [5, 6, 8, 10, 12, 15, 18, 20])
margin_of_safety = st.selectbox("Säkerhetsmarginal", [0.20, 0.25, 0.30, 0.35, 0.40])
stockprice = st.number_input("Vad är aktiekursen idag?", min_value=1, value=1, max_value=5000)

forward_eps = eps * (1 + growth /100 )

forward_PE = stockprice / forward_eps

st.divider()

result = value_stock(eps, growth, required_return, margin_of_safety)

st.markdown ("📈 Resultat")
st.markdown ("Alla värdern är uppskattningar, ej finansiell rådgivning.")
if result is None:
    st.error("Kombinationen finns inte i tabellen.")
else:
    pe, intrinsic_value, buy_price = result
    st.success(f"Motiverat P/E: {pe}")
    st.success(f"Motiverat aktiepris: {intrinsic_value:.2f}")
    st.success(f"Köp med Säkerhetsmarginal [{margin_of_safety * 100}%]: {buy_price:.2f}")
    st.success(f'ForwardPE är {forward_PE:.2f}')

interval = valuation_interval(
    eps,
    growth,
    required_return,
    margin_of_safety
)

if interval:
    data = []

    for g, value in interval.items():
        data.append({
            'Vinsttillväxt (%)': g,
            'Motiverat P/E': value['pe'],
            'Motiverat aktiepris': f"{value['intrinsic_value']:.2f}",
            f"Köp med Säkerhetsmarginal [{margin_of_safety * 100}%]": f"{value['buy_price']:.2f}"
        })

    df = pd.DataFrame(data).sort_values("Vinsttillväxt (%)")

    st.subheader("Värderingsintervall")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("Inga tillåtrna intervall för valda antaganden.")



## lägga in så man kan välja ticker 






