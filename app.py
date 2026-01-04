# ============================================
# IMPORT LIBRARIES
# ============================================
import streamlit as st

# ============================================
# PAGE CONFIGURATION
# EDITABLE: Ubah title, icon, layout sesuai kebutuhan
# ============================================
st.set_page_config(
    page_title="TerraML",  # EDITABLE: Title di browser tab
    page_icon="",                            # EDITABLE: Icon di browser tab (emoji atau path ke image)
    layout="wide",                             # EDITABLE: "wide" atau "centered"
    initial_sidebar_state="expanded"           # EDITABLE: "expanded" atau "collapsed"
)

# # ============================================
# # LOAD CSS STYLING
# # ============================================
# def load_css(file_path):
#     """Load external CSS file"""
#     with open(file_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # EDITABLE: Path ke file CSS
# load_css("Style/main.css")

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'page' not in st.session_state:
    st.session_state.page = 'Beranda'  # EDITABLE: Default halaman pertama kali load

# ============================================
# SIDEBAR NAVIGATION
# EDITABLE: Ubah logo, title, menu, copyright
# ============================================
with st.sidebar:
    
    # === LOGO & TITLE ===
    # EDITABLE: Ganti emoji logo dan text title
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h1 style='margin: 0; font-size: 2rem;'>🌍</h1>
        <h2 style='margin: 0.5rem 0 0 0; font-size: 1.3rem;'>Sistem PGA</h2>
    </div>
    """, unsafe_allow_html=True)
    # EDITABLE: Ganti 🌍 dengan emoji lain
    # EDITABLE: Ganti "Sistem PGA" dengan text lain
    
    st.markdown("---")
    
    # === NAVIGATION BUTTONS ===
    # EDITABLE: Tambah/hapus/ubah menu sesuai kebutuhan
    
    # MENU 1: BERANDA
    if st.button(
        "🏠 Beranda",                          # EDITABLE: Label menu
        use_container_width=True, 
        type="primary" if st.session_state.page == 'Beranda' else "secondary"
    ):
        st.session_state.page = 'Beranda'      # EDITABLE: Nama state (harus sama dengan routing)
        st.rerun()
    
    # MENU 2: DATA
    if st.button(
        "📊 Data",                             # EDITABLE: Label menu
        use_container_width=True,
        type="primary" if st.session_state.page == 'Data' else "secondary"
    ):
        st.session_state.page = 'Data'         # EDITABLE: Nama state
        st.rerun()
    
    # MENU 3: ESTIMASI PGA
    if st.button(
        "🔬 Estimasi PGA",                     # EDITABLE: Label menu
        use_container_width=True,
        type="primary" if st.session_state.page == 'Estimasi PGA' else "secondary"
    ):
        st.session_state.page = 'Estimasi PGA' # EDITABLE: Nama state
        st.rerun()
    
    # EDITABLE: Tambah menu baru dengan copy-paste block button di atas
    # Contoh:
    # if st.button("📈 Visualisasi", ...):
    #     st.session_state.page = 'Visualisasi'
    #     st.rerun()
    
    st.markdown("---")
    
    # === COPYRIGHT ===
    st.caption("© 2025 QuakeAceh")     # EDITABLE: Text copyright
    # EDITABLE: Bisa tambah link atau info lain

# ============================================
# PAGE ROUTING
# EDITABLE: Sesuaikan dengan menu yang dibuat di atas
# ============================================

if st.session_state.page == 'Beranda':         # EDITABLE: Nama state (harus sama dengan button)
    from Page import beranda           # EDITABLE: Nama file module
    beranda.show()                              # Panggil function show()

elif st.session_state.page == 'Data':
    from Page import data
    data.show()

elif st.session_state.page == 'Estimasi PGA':
    from Page import estimasi
    estimasi.show()

# EDITABLE: Tambah routing baru kalau ada menu baru
# Contoh:
# elif st.session_state.page == 'Visualisasi':
#     from page_modules import visualisasi
#     visualisasi.show()

# ============================================
# CATATAN:
# - Setiap menu butuh 2 tempat edit:
#   1. Button di sidebar
#   2. Routing di bawah
# - Nama state harus PERSIS SAMA di kedua tempat
# - File module harus ada di folder page_modules/
# ============================================