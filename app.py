
import streamlit as st


# PAGE CONFIGURATION

st.set_page_config(
    page_title="QuakeAceh",  
    page_icon="🌍",                            
    layout="wide",                             
    initial_sidebar_state="expanded"          
)



# SESSION STATE INITIALIZATION

if 'page' not in st.session_state:
    st.session_state.page = 'Beranda' 


# SIDEBAR NAVIGATION

with st.sidebar:
    
    # LOGO (EMOJI) & TITLE 
    
    # Menggunakan Markdown standar agar warna teks adaptif
    st.markdown("<h1 style='text-align: center;font-size: 4rem; margin-bottom: 0;'>🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: -10px; font-size: 2rem; font-weight: bold;'>QuakeAceh</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; font-size: 1.1rem;'>Sistem PGA</p>", unsafe_allow_html=True)
       
    st.markdown("---")
    
    # === NAVIGATION BUTTONS ===
    
    # MENU 1: BERANDA
    if st.button(
        "🏠 Beranda",                          
        use_container_width=True, 
        type="primary" if st.session_state.page == 'Beranda' else "secondary"
    ):
        st.session_state.page = 'Beranda'      
        st.rerun()
    
    if st.button(
        "📖 Panduan",                          
        use_container_width=True, 
        type="primary" if st.session_state.page == 'Panduan' else "secondary"
    ):
        st.session_state.page = 'Panduan'      
        st.rerun()
    
    # MENU 2: DATA
    if st.button(
        "📊 Data",                             
        use_container_width=True,
        type="primary" if st.session_state.page == 'Data' else "secondary"
    ):
        st.session_state.page = 'Data'         
        st.rerun()
    
    # MENU 3: ESTIMASI PGA
    if st.button(
        "🔬 Estimasi PGA",                     
        use_container_width=True,
        type="primary" if st.session_state.page == 'Estimasi PGA' else "secondary"
    ):
        st.session_state.page = 'Estimasi PGA' 
        st.rerun()
    
   
    
    st.markdown("---")
    
    # COPYRIGHT
    st.caption("© 2025 QuakeAceh")     
    
# PAGE ROUTING

if st.session_state.page == 'Beranda':         
    from Page import beranda           
    beranda.show()

elif st.session_state.page == 'Panduan':         
    from Page import panduan           
    panduan.show()                              

elif st.session_state.page == 'Data':
    from Page import data
    data.show()

elif st.session_state.page == 'Estimasi PGA':
    from Page import estimasi
    estimasi.show()