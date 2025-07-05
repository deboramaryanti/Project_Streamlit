import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu

def tampilkan_prediction():
    # Jalankan animasi hanya sekali
    st.markdown("""
        <style>
        .pred-animation {
            font-size: 40px;
            font-weight: bold;
            color: #4A90E2;
            margin: 20px auto;
            text-align: center;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        </style>

        <div class="pred-animation">What do you want to predict?</div>
    """, unsafe_allow_html=True)

    # Gunakan session_state untuk menyimpan apakah tombol sudah ditekan
    if "prediction_ditampilkan" not in st.session_state:
        st.session_state.prediction_ditampilkan = False

    if st.session_state.prediction_ditampilkan:
        st.markdown("---")
        st.subheader("Prediction")

    sub = option_menu(
        menu_title=None,
        options=["Shopping Trends", "Warehouse", "Employee"],
        icons=["cart", "archive", "person"],
        orientation="vertical"
    )

    if sub == "Shopping Trends":
        import predshop
        predshop.tampilkan_predshop()
    elif sub == "Warehouse":
        st.info("Proyek Warehouse masih dalam pengerjaan.")
    elif sub == "Employee":
        import predemp
        predemp.tampilkan_predem()
    
    st.markdown("""
---
<p style='text-align:center;'>
    Made with ❤️ by Debora Maryanti | Powered by Streamlit
</p>
""", unsafe_allow_html=True)
