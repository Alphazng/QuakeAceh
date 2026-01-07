# IMPORT LIBRARIES
import streamlit as st
from streamlit_folium import st_folium
import folium

# HALAMAN BERANDA

def show():
    
    # HEADER HALAMAN
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 font-size: 2.5rem; margin-bottom: 0.5rem;'>
            QuakeAceh
        </h1>
        <p font-size: 1.2rem; font-weight: 400;'>
            Peak Ground Acceleration untuk Wilayah Aceh dan Sekitarnya
        </p>
    </div>
    """, unsafe_allow_html=True)
   
    # MAP INDONESIA (INTERACTIVE)
    
    st.markdown("### Wilayah Studi")  
    
   
    #  Interactive Map - ZOOM KE ACEH
    m = folium.Map(
        location=[5.5483, 95.3238],       # Koordinat center Aceh [lat, lon]
        zoom_start=8,                     # Zoom level lebih dekat ke Aceh
    )
    
    # Marker Untuk Aceh
    folium.Marker(
        location=[5.5483, 95.3238],           # Koordinat marker [lat, lon]
        popup='<b>Aceh</b><br>Wilayah Studi', # Text saat marker diklik
        tooltip='Aceh - Focus Area',          
        icon=folium.Icon(
            color='red',                      
            icon='info-sign'                  
        )
    ).add_to(m)
    
    # Highligh bulatan untuk wilayah studi di map 
    # EDITABLE: Koordinat, radius, warna
    folium.Circle(
        location=[5.5483, 95.3238],      # Center circle [lat, lon]
        radius=100000,                    
        color='red',                      
        fill=True,
        fillColor='red',                  
        fillOpacity=0.2,                  # Transparansi (0-1, 0.2 = 20%)
        popup='Area Studi Aceh'           # Popup text
    ).add_to(m)
    
        
    # Tampilkan Map
    st_folium(
        m,
        width=None,                       
        height=400,                       
        returned_objects=[]
    )
    
    st.caption("Peta interaktif wilayah Indonesia")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PENJELASAN SISTEM dan PGA
    
    st.markdown("### Tentang Sistem")  
    
    # === Deskripsi Sistem ===
    st.markdown("""
    **QuakeAceh** adalah aplikasi web untuk mengestimasi nilai 
    **Peak Ground Acceleration (PGA)** akibat gempa bumi di sebuah wilayah menggunakan metode hibrida Ground Motion Prediction Equation (GMPE) dan Pembelajaran Mesin.
    """, text_alignment = "justify")
    
    # === Expander: Apa itu PGA? ===
    with st.expander("Penjelasan PGA"):  # EDITABLE: Label expander
        st.markdown("""
        Peak Ground Accelaration (PGA) merupakan parameter yang mempresentasikan nilai 
        percepatan tanah maksimum yang terjadi di suatu lokasi akibat guncangan gempa bumi. 
        Berbeda dengan Magnitudo yang mengukur total energi gempa di pusatnya, PGA secara spesifik menggambarkan seberapa kuat getaran tanah di permukaan, 
        yang biasanya diukur dalam satuan gravitasi (g) atau cm/s². Nilai ini menjadi ambang batas  bagi para ahli konstruksi dalam merancang standar 
        bangunan tahan gempa karena semakin tinggi nilai PGA yang tercatat, semakin besar  beban struktural dan risiko kerusakan yang harus diantisipasi 
        pada gedung atau infrastruktur di wilayah tersebut.
        """, text_alignment = "justify")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Button Untuk Mulai
      
    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_center:        
        if st.button(
            "MULAI SEKARANG",              
            type="primary",
            use_container_width=True,
            key="btn_mulai_beranda"
        ):
            st.session_state.page = 'Data' 
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    