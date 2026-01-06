import streamlit as st

def show():
    st.markdown("---")
    st.markdown("## 📖 Panduan Penggunaan Aplikasi")
    
    with st.expander("Langkah 1: Unggah Data", expanded=True):
        st.write("""
        1. Pastikan file Anda berformat **CSV** ataupun **Excel**.
        2. Pastikan datasetnya memiliki variabel-variabel sesuai dengan syarat modelnya.
        """)

    with st.expander("Langkah 2: Pengaturan Parameter"):
        st.write("""
        * **Lokasi Target:** Tentukan koordinat lokasi yang ingin dihitung PGA-nya.
        """)

    with st.expander("Langkah 3: Interpretasi Hasil"):
        st.write("""
        Aplikasi akan menampilkan dua hasil utama:
        1. **PGA GMPE:** Perhitungan murni berdasarkan rumus matematik Boore-Atkinson.
        2. **PGA MLP (Hybrid):** Hasil koreksi kecerdasan buatan yang mempertimbangkan kualitas data sensor.
        
        **Metrik Akurasi:**
        * **MAE & RMSE:** Menunjukkan nilai Error yang didapatkan oleh metode pembelajaran mesin. Semakin kecil nilai, maka semakin bagus.
        """)

    with st.expander("Langkah 4: Ekspor Data"):
        st.write("""
        * Anda dapat mengunduh hasil estimasi dalam format **CSV** atau **Excel**.
        """)