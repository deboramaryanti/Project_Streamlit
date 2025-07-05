import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Debora's Portfolio", layout="centered")

selected2 = option_menu(None, ["Home", "Project", "About Me", "Prediction"], 
                        icons=['house', 'list-task', "person", "search"], 
                        menu_icon="cast", default_index=0, orientation="horizontal")

# Tampilkan halaman About Me jika dipilih
if selected2 == "About Me":
    import about
    about.tampilkan_about()
elif selected2 == "Project":
    import proyek
    proyek.tampilkan_proyek()
elif selected2 == "Prediction":
    import prediction
    prediction.tampilkan_prediction()
elif selected2 == "Home":
    import home
    home.tampilkan_home()

st.markdown("""
---
<p style='text-align:center;'>
    by Debora Maryanti | Powered by Streamlit
</p>
""", unsafe_allow_html=True)