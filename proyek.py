import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu

def tampilkan_proyek():
    # Jalankan animasi hanya sekali
    if "tampilkan_animasi" not in st.session_state:
        st.session_state.tampilkan_animasi = True

    if st.session_state.tampilkan_animasi:
        custom_html = """
        <div id="typewriter" style="
            font-family: monospace;
            font-size: 20px;
            color: #4A90E2;
            width: 90%;
            margin: 0px auto;
            border-right: 2px solid #4A90E2;
            white-space: pre-wrap;
            overflow: hidden;
        "></div>

        <script>
            const text = `Let's see my project`;
            let i = 0;
            const speed = 50;

            function typeWriter() {
                if (i < text.length) {
                    document.getElementById("typewriter").innerHTML += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            }

            typeWriter();
        </script>
        """
        html(custom_html, height=150)
        # Setelah animasi pertama, set False agar tidak muncul lagi
        st.session_state.tampilkan_animasi = False
    else:
        # Jika animasi sudah ditampilkan sebelumnya, langsung tampilkan teks biasa
        st.markdown('<div style="font-family: monospace; font-size: 20px; color: #4A90E2; text-align: center;">Lets see my project</div>', unsafe_allow_html=True)

    # Gunakan session_state untuk tombol toggle
    if "proyek_ditampilkan" not in st.session_state:
        st.session_state.proyek_ditampilkan = False

    if st.button("Project List", key="button_project_list"):
        st.session_state.proyek_ditampilkan = True

    # Tampilkan daftar proyek jika tombol ditekan
    if st.session_state.proyek_ditampilkan:
        st.markdown("---")
        st.subheader("My Project")

        sub = option_menu(
            menu_title=None,
            options=["Shopping Trends", "Warehouse", "Employee"],
            icons=["cart", "archive", "person"],
            orientation="vertical",
            key="menu_proyek"
        )

        if sub == "Shopping Trends":
            import shopping
            shopping.tampilkan_shopping()
        elif sub == "Warehouse":
            st.info("Warehouse project is still under development.")
        elif sub == "Employee":
            import employee
            employee.tampilkan_employee()
    
    st.markdown("""
---
<p style='text-align:center;'>
    Made with ❤️ by Debora Maryanti | Powered by Streamlit
</p>
""", unsafe_allow_html=True)
