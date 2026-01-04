# ============================================
# IMPORT LIBRARIES
# ============================================
import streamlit as st
from streamlit_folium import st_folium
import folium

# ============================================
# FUNCTION HALAMAN BERANDA
# ============================================
def show():
    """
    Halaman Beranda - Landing Page
    """
    
    # ============================================
    # HEADER HALAMAN
    # EDITABLE: Judul dan subtitle halaman
    # ============================================
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f2937; font-size: 2.5rem; margin-bottom: 0.5rem;'>
            Nama Website
        </h1>
        <p style='color: #6b7280; font-size: 1.2rem; font-weight: 400;'>
            Peak Ground Acceleration untuk Wilayah Indonesia
        </p>
    </div>
    """, unsafe_allow_html=True)
    # EDITABLE: Ganti "Sistem Estimasi PGA" dengan judul Anda
    # EDITABLE: Ganti subtitle sesuai kebutuhan
    # EDITABLE: Ubah warna (#1f2937 = dark gray, #6b7280 = medium gray)
    # EDITABLE: Ubah font-size (2.5rem, 1.2rem)
    
    # ============================================
    # SECTION 1: MAP INDONESIA (INTERACTIVE)
    # EDITABLE: Koordinat, zoom, marker, circle
    # ============================================
    
    st.markdown("### Wilayah Studi")  # EDITABLE: Title section
    
    # === Buat Interactive Map ===
    m = folium.Map(
        location=[-0.7893, 113.9213],    # EDITABLE: Koordinat center [lat, lon]
                                          # Indonesia: [-0.7893, 113.9213]
                                          # Aceh: [5.5483, 95.3238]
        zoom_start=5,                     # EDITABLE: Zoom level (1-20)
                                          # 5 = lihat Indonesia lengkap
                                          # 7 = fokus Aceh
                                          # 10 = sangat zoom in
        tiles='OpenStreetMap',            # EDITABLE: Map style
                                          # 'OpenStreetMap' (default)
                                          # 'CartoDB positron' (minimalist)
                                          # 'CartoDB dark_matter' (dark theme)
                                          # 'Stamen Terrain' (topografi)
    )
    
    # # === Tambah Marker untuk Aceh ===
    # # EDITABLE: Koordinat, popup text, tooltip, icon color
    # folium.Marker(
    #     location=[5.5483, 95.3238],           # EDITABLE: Koordinat marker [lat, lon]
    #     popup='<b>Aceh</b><br>Wilayah Studi', # EDITABLE: Text saat marker diklik
    #     tooltip='Aceh - Focus Area',          # EDITABLE: Text saat hover
    #     icon=folium.Icon(
    #         color='red',                      # EDITABLE: Warna icon
    #                                           # 'red', 'blue', 'green', 'purple', 'orange'
    #         icon='info-sign'                  # EDITABLE: Icon type
    #                                           # 'info-sign', 'home', 'star', 'heart'
    #     )
    # ).add_to(m)
    
    # # === Tambah Circle untuk highlight area ===
    # # EDITABLE: Koordinat, radius, warna
    # folium.Circle(
    #     location=[5.5483, 95.3238],      # EDITABLE: Center circle [lat, lon]
    #     radius=100000,                    # EDITABLE: Radius dalam meter (100km = 100000)
    #     color='red',                      # EDITABLE: Warna border
    #     fill=True,
    #     fillColor='red',                  # EDITABLE: Warna fill
    #     fillOpacity=0.2,                  # EDITABLE: Transparansi (0-1, 0.2 = 20%)
    #     popup='Area Studi Aceh'          # EDITABLE: Popup text
    # ).add_to(m)
    
    # EDITABLE: Tambah marker/circle lain dengan copy-paste block di atas
    # Contoh tambah marker untuk Jakarta:
    # folium.Marker(
    #     location=[-6.2088, 106.8456],
    #     popup='Jakarta',
    #     icon=folium.Icon(color='blue')
    # ).add_to(m)
    
    # === Tampilkan Map ===
    st_folium(
        m,
        width=None,                       # EDITABLE: None = auto width
        height=400,                       # EDITABLE: Tinggi map dalam pixels
        returned_objects=[]
    )
    
    st.caption("Peta interaktif wilayah Indonesia")
    # EDITABLE: Caption di bawah map
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 2: PENJELASAN SISTEM
    # EDITABLE: Semua text penjelasan
    # ============================================
    
    st.markdown("### Tentang Sistem")  # EDITABLE: Section title
    
    # === Deskripsi Sistem ===
    st.markdown("""
    **Nama Website** adalah aplikasi web untuk mengestimasi nilai 
    **Peak Ground Acceleration (PGA)** akibat gempa bumi di sebuah wilayah.
    """)
    # EDITABLE: Ganti dengan deskripsi sistem Anda
    
    # === Expander: Apa itu PGA? ===
    with st.expander("Penjelasan PGA"):  # EDITABLE: Label expander
        st.markdown("""
        **PGA (Peak Ground Acceleration)** adalah parameter penting dalam rekayasa gempa yang mengukur:
        
        - **Percepatan tanah maksimum** saat gempa terjadi
        - Diukur dalam satuan **g** (gravitasi) atau **cm/s²**
        - Digunakan untuk **desain bangunan tahan gempa**
        - Penting untuk **pemetaan bahaya seismik**
        
        Semakin tinggi nilai PGA, semakin kuat guncangan yang dialami.
        """)
       
    
    # EDITABLE: Tambah expander lain dengan copy-paste block di atas
    # Contoh:
    # with st.expander("🔬 Metodologi"):
    #     st.markdown("Penjelasan metodologi...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # # ============================================
    # # SECTION 3: KEGUNAAN SISTEM
    # # EDITABLE: Text untuk praktisi dan peneliti
    # # ============================================
    
    # st.markdown("### 🎯 Kegunaan Sistem")  # EDITABLE: Section title
    
    # col1, col2 = st.columns(2)  # EDITABLE: Ubah jadi st.columns(3) untuk 3 kolom
    
    # with col1:
    #     st.markdown("""
    #     **🏗️ Untuk Praktisi:**
    #     - Estimasi PGA untuk desain struktur
    #     - Pemetaan zona bahaya gempa
    #     - Perencanaan mitigasi bencana
    #     - Analisis risiko seismik
    #     """)
    #     # EDITABLE: Ganti icon (🏗️) dan text sesuai target user Anda
    
    # with col2:
    #     st.markdown("""
    #     **🎓 Untuk Peneliti:**
    #     - Studi karakteristik gempa Aceh
    #     - Perbandingan metode GMPE vs ML
    #     - Validasi model prediksi
    #     - Publikasi ilmiah
    #     """)
    #     # EDITABLE: Ganti icon (🎓) dan text sesuai kebutuhan
    
    # EDITABLE: Tambah kolom ke-3 kalau pakai st.columns(3)
    # with col3:
    #     st.markdown("Konten kolom 3...")
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 4: METODE ESTIMASI
    # EDITABLE: Penjelasan metode yang digunakan
    # ============================================
    
    st.markdown("### Metode Estimasi")  # EDITABLE: Section title
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.info("""
        **GMPE (Ground Motion Prediction Equations)**
        
        - Metode berbasis fisika gempa
        - Menggunakan Boore-Atkinson 2008
        - Akurasi proven untuk Aceh
        """)
        # EDITABLE: Ganti dengan metode Anda
        # st.info() = box biru
        # Bisa ganti jadi st.success() (hijau) atau st.warning() (kuning)
    
    with col_b:
        st.success("""
        **Machine Learning**
        
        - Metode berbasis data dan pola
        - Menggunakan Neural Network (MLP)
        - Dapat tangkap pola kompleks
        """)
        # EDITABLE: Ganti dengan metode Anda
        # st.success() = box hijau
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 5: CALL TO ACTION (BUTTON MULAI)
    # EDITABLE: Text ajakan dan label button
    # ============================================
    
    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_center:
        # st.markdown("""
        # <div style='text-align: center; margin-bottom: 1rem;'>
        #     <p style='color: #374151; font-size: 1.1rem; font-weight: 500;'>
        #         Siap untuk memulai estimasi PGA?
        #     </p>
        # </div>
        # """, unsafe_allow_html=True)
        # EDITABLE: Ganti text ajakan
        
        # === BUTTON MULAI ===
        if st.button(
            "MULAI SEKARANG",              # EDITABLE: Label button
            type="primary",
            use_container_width=True,
            key="btn_mulai_beranda"
        ):
            st.session_state.page = 'Data'     # EDITABLE: Halaman tujuan
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ============================================
    # FOOTER INFORMASI
    # EDITABLE: Info sumber data, metode, region
    # ============================================
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
        <p>
            <b>Sumber Data:</b> USGS Earthquake Catalog (1900-2025) | 
            <b>Metode:</b> Boore-Atkinson 2008 GMPE & Neural Network MLP | 
            <b>Region:</b> Aceh dan sekitarnya
        </p>
    </div>
    """, unsafe_allow_html=True)
    # EDITABLE: Ganti dengan info footer Anda
    # EDITABLE: Ubah warna text (#6b7280)
    # EDITABLE: Ubah font-size (0.9rem)