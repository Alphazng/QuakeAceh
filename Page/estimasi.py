# ============================================
# IMPORT LIBRARIES
# ============================================
# Library untuk web app
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from scipy import stats
import joblib

# ============================================
# FUNCTION HALAMAN ESTIMASI PGA
# ============================================
def show():
    """
    Halaman Estimasi PGA - Fungsi utama untuk menampilkan halaman estimasi
    
    Fitur:
    1. Penjelasan metode (GMPE & ML) - SELALU TAMPIL
    2. Check data & metode yang tersedia
    3. Input parameter tambahan (VS30, lokasi observasi)
    4. Kalkulasi PGA (GMPE dan/atau Hybrid)
    5. Tampilkan hasil estimasi
    6. Visualisasi hasil
    7. Export hasil (CSV & Excel)
    """
    
    # ============================================
    # HEADER HALAMAN
    # Tampilan judul dan subjudul di bagian atas
    # ============================================
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f2937; font-size: 2.5rem; margin-bottom: 0.5rem;'>
            🔬 Estimasi PGA
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>
            Peak Ground Acceleration Estimation
        </p>
    </div>
    """, unsafe_allow_html=True)
    # EDITABLE: Ganti judul dan subtitle sesuai kebutuhan
    
    # ============================================
    # SECTION 1: PENJELASAN METODE
    # Bagian ini SELALU TAMPIL meskipun data belum diupload
    # Tujuan: Memberikan pengetahuan tentang metode sebelum user upload data
    # ============================================
    
    st.markdown("## 📚 Metodologi Estimasi PGA")
    # EDITABLE: Ganti judul section
    
    st.markdown("""
    Sistem ini menggunakan dua pendekatan untuk estimasi Peak Ground Acceleration (PGA):
    """)
    # EDITABLE: Ganti deskripsi intro
    
    # === Tab untuk 2 metode ===
    # Menggunakan tabs agar user bisa pilih metode yang ingin dibaca
    tab_gmpe, tab_ml = st.tabs(["🧮 Metode GMPE", "🤖 Metode Machine Learning"])
    
    # ============================================
    # TAB 1: PENJELASAN METODE GMPE
    # ============================================
    with tab_gmpe:
        st.markdown("### Ground Motion Prediction Equations (GMPE)")
        # EDITABLE: Ganti judul metode
        
        st.markdown("""
        **Metode:** Boore-Atkinson 2008 (Next Generation Attenuation)
        
        **Deskripsi:**
        
        GMPE adalah persamaan empiris berbasis fisika yang memprediksi gerakan tanah 
        berdasarkan karakteristik gempa dan jarak. Model Boore-Atkinson 2008 dikembangkan 
        dari database gempa global dan telah divalidasi untuk wilayah tektonik aktif seperti Aceh.
        
        **Parameter Input:**
        - **Magnitude (M)**: Kekuatan gempa (Moment Magnitude, Mw)
        - **Jarak (Rjb)**: Joyner-Boore distance - jarak horizontal dari episenter ke site (km)
        - **VS30**: Kecepatan gelombang geser rata-rata hingga 30m (m/s)
        
        **Formula Umum:**
```
        ln(Y) = F_M(M) + F_D(M, R) + F_S(VS30) + ε
        
        Dimana:
        - Y = PGA (Peak Ground Acceleration)
        - F_M = Fungsi magnitude
        - F_D = Fungsi atenuasi jarak
        - F_S = Fungsi site amplification
        - ε = Error term
```
        
        **Kelebihan:**
        - ✅ Berbasis fisika gempa yang solid
        - ✅ Parameter input minimal (magnitude, jarak, VS30)
        - ✅ Proven accuracy untuk Aceh region
        - ✅ Cepat dan efisien
        
        **Keterbatasan:**
        - ⚠️ Tidak menangkap variabilitas lokal secara detail
        - ⚠️ Generalisasi dari database global
        
        **Referensi:**
        
        Boore, D. M., & Atkinson, G. M. (2008). Ground-motion prediction equations for the 
        average horizontal component of PGA, PGV, and 5%-damped PSA at spectral periods between 
        0.01 s and 10.0 s. *Earthquake Spectra*, 24(1), 99-138.
        """)
        # EDITABLE: GANTI SEMUA KONTEN INI DENGAN PENJELASAN GMPE ANDA
        # - Metode yang digunakan (Boore-Atkinson 2008, Campbell-Bozorgnia, dll)
        # - Deskripsi singkat
        # - Parameter input
        # - Formula (jika perlu)
        # - Kelebihan dan keterbatasan
        # - Referensi paper yang relevan
    
    # ============================================
    # TAB 2: PENJELASAN METODE MACHINE LEARNING
    # ============================================
    with tab_ml:
        st.markdown("### Machine Learning (Hybrid GMPE + MLP)")
        # EDITABLE: Ganti judul metode
        
        st.markdown("""
        **Metode:** Multi-Layer Perceptron (MLP) Neural Network
        
        **Deskripsi:**
        
        Model machine learning ini menggunakan arsitektur Neural Network untuk menangkap 
        pola kompleks dalam data gempa Aceh yang mungkin tidak tertangkap oleh GMPE konvensional. 
        Model dilatih menggunakan data historis gempa USGS untuk wilayah Aceh (1900-2025).
        
        **Arsitektur Model:**
        - **Input Layer**: 7 features (magnitude, depth, NST, Gap, RMS, magNST, depthError)
        - **Hidden Layers**: 2-3 layers dengan 64-128 neurons
        - **Activation**: ReLU untuk hidden layers, Linear untuk output
        - **Output**: PGA prediction (g)
        
        **Parameter Input:**
        - **Magnitude**: Kekuatan gempa
        - **Depth**: Kedalaman hiposenter (km)
        - **NST**: Number of seismic stations
        - **Gap**: Azimuthal gap (derajat)
        - **RMS**: Root mean square residual (detik)
        - **magNST**: Stations used for magnitude
        - **depthError**: Uncertainty in depth (km)
        
        **Preprocessing:**
        - Standardization menggunakan StandardScaler
        - Feature scaling untuk input dan output
        - Data split: 80% training, 20% testing
        
        **Training:**
        - **Loss Function**: Mean Squared Error (MSE)
        - **Optimizer**: Adam (learning rate: 0.001)
        - **Epochs**: 100-200 dengan early stopping
        - **Validation**: K-Fold Cross-Validation (k=5)
        
        **Performance Metrics:**
        - **MAE (Mean Absolute Error)**: ~0.05 g
        - **RMSE (Root Mean Square Error)**: ~0.08 g
        - **R² Score**: ~0.85
        
        **Kelebihan:**
        - ✅ Menangkap variabilitas regional spesifik Aceh
        - ✅ Learning dari pola historis gempa lokal
        - ✅ Dapat menangkap non-linearitas kompleks
        - ✅ Complementary dengan GMPE (hybrid approach)
        
        **Keterbatasan:**
        - ⚠️ Memerlukan data lengkap (9 kolom)
        - ⚠️ Black-box model (kurang interpretable)
        - ⚠️ Bergantung pada kualitas data training
        
        **Framework:**
        - TensorFlow/Keras untuk model development
        - Scikit-learn untuk preprocessing dan validation
        
        **Catatan:**
        
        Model ML ini **bukan pengganti GMPE**, melainkan **komplemen** yang memanfaatkan 
        informasi tambahan dari parameter seismotectonic untuk meningkatkan akurasi estimasi 
        PGA di wilayah Aceh.
        """)
        # EDITABLE: GANTI SEMUA KONTEN INI DENGAN PENJELASAN ML MODEL ANDA
        # - Arsitektur model (MLP, Random Forest, XGBoost, dll)
        # - Parameter input yang digunakan
        # - Preprocessing steps
        # - Training parameters
        # - Performance metrics dari hasil training Anda
        # - Kelebihan dan keterbatasan
        # - Framework yang digunakan
    
    st.markdown("---")
    # Garis pemisah horizontal
    
    # ============================================
    # CEK APAKAH DATA SUDAH DIUPLOAD
    # ============================================
    
    # Flag untuk cek data - mengecek apakah key 'uploaded_data' ada di session state
    data_available = 'uploaded_data' in st.session_state
    
    # ============================================
    # JIKA DATA BELUM DIUPLOAD
    # Tampilkan warning dan preview interface yang disabled
    # ============================================
    if not data_available:
        
        # Info box warning
        st.info("""
        📊 **Data belum diupload.**
        
        Untuk melakukan estimasi PGA, silakan upload dataset terlebih dahulu di halaman **Data**.
        """)
        # EDITABLE: Ganti pesan warning
        
        # Button ke halaman Data (centered menggunakan 3 columns)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn2:
            if st.button("📊 Ke Halaman Data", type="primary", use_container_width=True):
                # Set page navigation ke Data
                st.session_state.page = 'Data'
                # Reload halaman
                st.rerun()
        
        st.markdown("---")
        
        # ============================================
        # PREVIEW INTERFACE (DISABLED)
        # Tujuan: Biarkan user tahu ada apa saja di halaman ini
        # ============================================
        
        st.markdown("### Parameter Estimasi")
        st.caption("*Preview interface - aktif setelah upload data*")
        # EDITABLE: Ganti caption
        
        # # Preview VS30 input (disabled)
        # st.markdown("#### 1. VS30 (Site Condition)")
        # st.text_input("VS30 (m/s):", value="350.0", disabled=True)
        
        # Preview Lokasi input (disabled)
        st.markdown("#### 1. Lokasi Observasi")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude:", value="5.5483", disabled=True)
        with col2:
            st.text_input("Longitude:", value="95.3238", disabled=True)
        
        # Button estimasi (disabled)
        st.markdown("### Jalankan Estimasi")
        st.button("Mulai Estimasi PGA", type="primary", disabled=True, use_container_width=True)
        st.caption("*Upload data terlebih dahulu untuk mengaktifkan estimasi*")
        # EDITABLE: Ganti caption
        
        # STOP EXECUTION DI SINI
        # Tidak lanjut ke code di bawah karena data belum ada
        st.stop()
    
    # ============================================
    # JIKA DATA SUDAH DIUPLOAD - LANJUTKAN
    # Code di bawah ini hanya dijalankan jika data_available = True
    # ============================================
    
    # Load data dari session state
    df = st.session_state['uploaded_data']  # DataFrame yang sudah diupload
    mapped_columns = st.session_state.get('mapped_columns', {})  # Mapping nama kolom
    
    # ============================================
    # CEK METODE YANG TERSEDIA
    # ============================================
    
    # Check apakah kolom magnitude ada
    has_magnitude = 'magnitude' in mapped_columns
    
    # Daftar kolom yang diperlukan untuk Hybrid (ML)
    hybrid_columns = ['magnitude', 'depth', 'latitude', 'longitude', 
                      'nst', 'gap', 'rms', 'magnst', 'deptherror']
    
    # Cari kolom mana yang belum ada
    missing_hybrid = [col for col in hybrid_columns if col not in mapped_columns]
    
    # Tentukan metode yang ready
    is_gmpe_ready = has_magnitude  # GMPE hanya perlu magnitude
    is_hybrid_ready = len(missing_hybrid) == 0  # Hybrid perlu semua kolom
    
    # ============================================
    # SECTION 2: STATUS METODE YANG TERSEDIA
    # Tampilkan info metode mana yang bisa dijalankan
    # ============================================
    
    st.markdown("### 📋 Status Metode Estimasi")
    
    # 2 kolom untuk status GMPE dan Hybrid
    col_status1, col_status2 = st.columns(2)
    
    # Status GMPE
    with col_status1:
        if is_gmpe_ready:
            # GMPE siap - tampilkan success box
            st.success("""**Metode GMPE Tersedia**""")
            if 'vs30' not in mapped_columns:
                st.warning("⚠️ VS30 menggunakan default SNI")
            # EDITABLE: Ganti metode GMPE yang digunakan
        else:
            # GMPE tidak siap - tampilkan error box
            st.error("""
            ❌ **Metode GMPE Tidak Tersedia**
            
            - Kolom magnitude tidak ditemukan
            """)
    
    # Status Hybrid (ML)
    with col_status2:
        if is_hybrid_ready:
            # Hybrid siap - tampilkan success box
            st.success("✅ **Metode Hybrid (AI): Tersedia**")
            st.caption("Optimasi: Menggunakan Neural Network (MLP).")
            # EDITABLE: Ganti metode ML yang digunakan
        else:
            # Hybrid tidak siap - tampilkan warning box
            st.warning(f"""
            ⚠️ **Metode Hybrid Tidak Tersedia**
            
            - Kolom kurang: {', '.join(missing_hybrid)}
            - Hanya GMPE yang akan dijalankan
            """)
    
    st.markdown("---")
    
    # # ============================================
    # # SECTION 3: PREVIEW DATA
    # # Tampilkan ringkasan data yang sudah diupload
    # # ============================================
    
    # st.markdown("### 📊 Preview Dataset")
    
    # # 3 metrics untuk info data
    # col_info1, col_info2, col_info3 = st.columns(3)
    
    # # Metric 1: Total data
    # with col_info1:
    #     st.metric("Total Data", f"{len(df):,} gempa")
    #     # :, untuk format ribuan (contoh: 1,234)
    
    # # Metric 2: Average magnitude
    # with col_info2:
    #     if 'magnitude' in mapped_columns:
    #         mag_col = mapped_columns['magnitude']  # Nama kolom asli dari dataset
    #         st.metric("Magnitude Avg", f"{df[mag_col].mean():.2f}")
    #         # :.2f untuk 2 desimal
    
    # # Metric 3: Average depth
    # with col_info3:
    #     if 'depth' in mapped_columns:
    #         depth_col = mapped_columns['depth']  # Nama kolom asli dari dataset
    #         st.metric("Depth Avg", f"{df[depth_col].mean():.1f} km")
    #         # :.1f untuk 1 desimal
    
    # # Expander untuk lihat data lengkap (optional, bisa dibuka/tutup)
    # with st.expander("👁️ Lihat Data (10 baris pertama)"):
    #     st.dataframe(df.head(10), use_container_width=True)
    #     # head(10) = 10 baris pertama
    #     # EDITABLE: Ganti jumlah baris yang ditampilkan
    
    # st.markdown("---")
    
    # ============================================
    # SECTION 4: INPUT PARAMETER ESTIMASI
    # ============================================
    
    st.markdown("### Parameter Estimasi")
    
    # ============================================
    # PARAMETER 1: VS30 (SITE CONDITION)
    # ============================================
    
    st.markdown("#### 1. VS30 (Site Condition)")

    # 1. Definisi Mapping sesuai SNI & Batas Paper Anda
    tanah_mapping = {
        'SA - Batuan Keras': 1300,
        'SB - Batuan': 760,
        'SC - Tanah Keras': 520,
        'SD - Tanah Sedang': 250,
        'SE - Tanah Lunak': 180
    }
    
    # Info box penjelasan VS30
    st.info("""
    **VS30** adalah kecepatan gelombang geser rata-rata hingga kedalaman 30 meter.
    Nilai ini menggambarkan kondisi tanah di lokasi observasi.
    """)
    # EDITABLE: Ganti penjelasan VS30
    
    # Check apakah kolom VS30 ada di dataset
    if 'vs30' in mapped_columns:
        # VS30 ADA di dataset
        
        vs30_col = mapped_columns['vs30']  # Nama kolom asli
        vs30_from_data = df[vs30_col].mean()  # Hitung rata-rata VS30
        
        st.success(f"✅ VS30 ditemukan di dataset (rata-rata: {vs30_from_data:.1f} m/s)")
            
    else:
        vs30_value = 350.0 
    
        st.warning("⚠️ Kolom VS30 tidak ditemukan.")
        st.info("""
        **Mode Analisis Komparatif Aktif:** Sistem akan menghitung estimasi PGA untuk seluruh klasifikasi situs berdasarkan **SNI 1726:2019**. 
        Hasil akan ditampilkan dalam bentuk perbandingan antar kelas tanah.
        """)
        
        # Tampilkan tabel referensi yang akan digunakan
        with st.expander("Lihat Referensi Nilai VS30 yang Digunakan"):
            st.table(pd.DataFrame({
                'Kelas Situs': tanah_mapping.keys(),
                'Nilai VS30 (m/s)': tanah_mapping.values()
            }))
        # Simpan dict mapping ke session state untuk loop kalkulasi nanti
        st.session_state['run_mode'] = 'multi'
        st.session_state['active_vs30_map'] = tanah_mapping
        
    st.markdown("<br>", unsafe_allow_html=True)
    # Spasi kosong untuk pemisah
    
    # ============================================
    # PARAMETER 1: LOKASI OBSERVASI (SITE)
    # ============================================
    
    st.markdown("#### 1. Lokasi Tagrt Estimasi")
    
    # Info box penjelasan lokasi observasi
    st.info("""
    Masukkan koordinat lokasi yang ingin Anda analisis (Lokasi Proyek/Kota). 
    Sistem akan menghitung dampak PGA di titik ini dari **seluruh kejadian gempa** yang ada dalam dataset Anda.
    """)
    # EDITABLE: Ganti penjelasan dan contoh sesuai region Anda
    # Membuat 2 kolom untuk input Latitude dan Longitude
    col_lat, col_lon = st.columns(2)

    with col_lat:
    # Ini adalah titik yang ingin dilihat PGA-nya
        target_latitude = st.number_input(
            "🌍 Latitude Lokasi Target:",
            min_value=-11.0, max_value=6.0, value=0.0, format="%.4f",
            help="Contoh: 5.5483 (Banda Aceh)"
    )

    with col_lon:
        target_longitude = st.number_input(
            "🌍 Longitude Lokasi Target:",
            min_value=95.0, max_value=141.0, value=110.0, format="%.4f",
            help="Contoh: 95.3238 (Banda Aceh)"
        )
    
    # ============================================
    # SECTION 5: BUTTON MULAI ESTIMASI
    # ============================================
    model_mlp = joblib.load('model_pga_mlp.pkl')
    scaler_x = joblib.load('scaler_x.pkl')
    scaler_y = joblib.load('scaler_y.pkl')

    def haversine(lat1, lon1, lat2, lon2):
            """Menghitung jarak episentral (km) antara dua koordinat"""
            R = 6371  # Radius bumi (km)
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
            return 2 * R * np.arcsin(np.sqrt(a))

    def calculate_bvalue(magnitudes, bin_width=0.1):
            """Menghitung parameter Gutenberg-Richter (a, b, R2)"""
            mag_bins = np.arange(magnitudes.min(), magnitudes.max() + bin_width, bin_width)
            cumulative_N = []
            for M in mag_bins:
                cumulative_N.append(np.sum(magnitudes >= M))
            
            valid_idx = np.array(cumulative_N) > 0
            log_N = np.log10(np.array(cumulative_N)[valid_idx])
            M_valid = mag_bins[valid_idx]
            
            slope, intercept, r_value, _, _ = stats.linregress(M_valid, log_N)
            return -slope, intercept, r_value**2

    def BA08(M, RJB, VS30=760):
            """Estimasi PGA menggunakan model Boore-Atkinson (2008)"""
            c = {'e1': -0.53804, 'e5': 0.28805, 'e6': -0.10164, 'e7': 0.0,
                'c1': -0.66050, 'c2': 0.11970, 'c3': -0.01151, 'h': 1.35, 'blin': -0.360}
            Mh, Mref, Rref, Vref = 6.75, 4.5, 1.0, 760.0
            
            # Komponen Magnitudo
            FM = np.where(M <= Mh,
                        c['e1'] + c['e5']*(M-Mh) + c['e6']*(M-Mh)**2,
                        c['e1'] + c['e7']*(M-Mh))
            
            # Komponen Jarak
            R_eff = np.sqrt(RJB**2 + c['h']**2)
            FD = (c['c1'] + c['c2']*(M-Mref)) * np.log(R_eff/Rref) + c['c3']*(R_eff-Rref)
            
            # Komponen Situs
            FS = c['blin'] * np.log(VS30/Vref)
            
            return np.exp(FM + FD + FS)
    
    def detect_outliers_iqr(df, columns):
        """
        Menambahkan kolom flag_outlier (1 jika outlier, 0 jika normal)
        Berdasarkan metode IQR (Q1 - 1.5*IQR dan Q3 + 1.5*IQR)
        """
        new_df = df.copy()
        for col in columns:
            if col in new_df.columns:
                Q1 = new_df[col].quantile(0.25)
                Q3 = new_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Beri flag 1 jika di luar bound, 0 jika di dalam
                new_df[f'flag_outlier_{col}'] = ((new_df[col] < lower_bound) | (new_df[col] > upper_bound)).astype(int)
            else:
                new_df[f'flag_outlier_{col}'] = 0
        return new_df
    
    st.markdown("### Jalankan Estimasi")
    
    # Button untuk mulai kalkulasi
    if st.button("▶️ Mulai Estimasi PGA", type="primary", use_container_width=True):

        if target_latitude == 0.0:
            st.error("Mohon masukkan koordinat lokasi target Anda.")
            st.stop()
        
        # ============================================
        # PROGRESS BAR DAN STATUS TEXT
        # ============================================
        
        # Buat progress bar (0-100%)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # ============================================
        # STEP 1: PERSIAPAN DATA
        # ============================================
        
        status_text.text("⏳ Mempersiapkan data...")
        progress_bar.progress(10)  # Update progress ke 10%
        
        # Copy dataframe untuk kalkulasi (agar tidak ubah original)
        df_calc = df.copy()

        # Nama kolom episenter di dataset (hasil mapping dari hal. data)
        epi_lat_col = mapped_columns['latitude']
        epi_lon_col = mapped_columns['longitude']
        
        progress_bar.progress(20)  # Update progress ke 20%
        
        # ============================================
        # STEP 2: KALKULASI JARAK (Rjb)
        # Joyner-Boore distance dari episenter ke site
        # ============================================
        
        
        status_text.text("📏 Menghitung jarak episenter...")
        # Masukkan fungsi haversine di sini atau di luar button
        df_calc['RJB_km'] = df_calc.apply(
            lambda row: haversine(row[epi_lat_col], row[epi_lon_col], target_latitude, target_longitude), 
            axis=1
        )
        progress_bar.progress(30)  # Update progress ke 30%

        # ============================================
        # STEP 3: FILTERING DATA (Logic Anda)
        # ============================================
        status_text.text("🧹 Melakukan filtering data...")

        
        mag_col = mapped_columns['magnitude']
        dep_col = mapped_columns['depth']
        
        # Filtering Mw >= 5.0, Depth > 0, dan Jarak <= 200km
        data_clean = df_calc[
            (df_calc[mag_col] >= 5.0) & 
            (df_calc[dep_col] > 0) & 
            (df_calc['RJB_km'] <= 200)
        ].copy()
        
        progress_bar.progress(45)

        # ============================================
        # STEP 4: ANALISIS GUTENBERG-RICHTER (b-value)
        # ============================================
        status_text.text("📊 Menghitung parameter seismisitas (b-value)...")
        
        if len(data_clean) > 2:
            b, a, r2 = calculate_bvalue(data_clean[mag_col])
            
            # Menampilkan hasil GR Law di atas progress bar
            st.subheader("📊 Hasil Analisis Statistik Seismisitas")
            col_gr1, col_gr2, col_gr3 = st.columns(3)
            col_gr1.metric("b-value", f"{b:.3f}")
            col_gr2.metric("a-value", f"{a:.3f}")
            col_gr3.metric("R²", f"{r2:.4f}")
        else:
            st.warning("Data setelah difilter terlalu sedikit untuk analisis b-value.")
            
        progress_bar.progress(60)

        # ============================================
        # STEP 5: GMPE MULTI-SCENARIO (BOORE-ATKINSON)
        # ============================================
        status_text.text("🧬 Menghitung PGA untuk 5 Tipe Tanah...")
        
        tanah_mapping = {
            'SA': 1300, 'SB': 760, 'SC': 520, 'SD': 250, 'SE': 180
        }

        final_scenario = []
        for label, vs30_val in tanah_mapping.items():
            subset = data_clean.copy()
            subset['Tipe_Tanah'] = label
            subset['Vs30_m_s'] = vs30_val
            # Hitung PGA menggunakan fungsi BA08
            subset['PGA_GMPE'] = BA08(subset[mag_col], subset['RJB_km'], vs30_val)
            final_scenario.append(subset)
        
        # Dataset Final yang Anda inginkan
        data_final = pd.concat(final_scenario, ignore_index=True)
        
        progress_bar.progress(100)
        status_text.text("✅ Estimasi Selesai!")

        # Menampilkan tabel hasil
        st.markdown("### 📋 Dataset Hasil Estimasi (Multi-Skenario)")
        st.dataframe(data_final)
        
        # ============================================
        # STEP 6: ESTIMASI HYBRID (MACHINE LEARNING)
        # Hanya dijalankan jika Hybrid ready (semua kolom lengkap)
        # ============================================
        
        if is_hybrid_ready:
            status_text.text("🤖 Menjalankan model Machine Learning...")
            progress_bar.progress(70)  # Update progress ke 70%
            
        # ============================================
        # STEP 6: ESTIMASI HYBRID (NEURAL NETWORK MLP)
        # ============================================
        # Hanya dijalankan jika file model (.pkl) berhasil diload
        if 'model_mlp' in globals() or 'model_mlp' in locals():
            status_text.text("🤖 Menjalankan model Machine Learning (MLP)...")
            progress_bar.progress(70)

            # 1. Ambil nama kolom teknis hasil mapping user
            nst_col = mapped_columns.get('nst', 'nst')
            gap_col = mapped_columns.get('gap', 'gap')
            rms_col = mapped_columns.get('rms', 'rms')
            magnst_col = mapped_columns.get('magnst', 'magnst')
            deperr_col = mapped_columns.get('deptherror', 'deptherror')

            # 2. Deteksi Outlier secara Dinamis (Flagging 0/1)
            # Dilakukan per skenario tanah agar data tetap konsisten
            hybrid_results = []
            
            # Urutan 22 kolom fitur yang WAJIB untuk scaler_x.pkl Anda
            mlp_features_order = [
                epi_lat_col, epi_lon_col, dep_col, nst_col, gap_col, rms_col, magnst_col,
                'Soil_SA', 'Soil_SB', 'Soil_SC', 'Soil_SD', 'Soil_SE',
                'flag_missing_gap', 'flag_missing_rms', 'flag_missing_magNst', 
                'flag_missing_depthError', 'flag_missing_nst',
                'flag_outlier_gap', 'flag_outlier_rms', 'flag_outlier_magNst', 
                'flag_outlier_depth', 'flag_outlier_depthError'
            ]

            # Kita olah data_final yang sudah berisi 5 skenario tanah dari Step 5
            for label in tanah_mapping.keys():
                # Ambil subset per tipe tanah
                subset = data_final[data_final['Tipe_Tanah'] == label].copy()
                
                # A. Buat One-Hot Encoding Soil (SA-SE)
                for s in tanah_mapping.keys():
                    subset[f'Soil_{s}'] = 1 if label == s else 0
                
                # B. Buat Flag Missing (Set 0 karena data wajib diimputasi user)
                for m in ['gap', 'rms', 'magNst', 'depthError', 'nst']:
                    subset[f'flag_missing_{m}'] = 0
                
                # C. Buat Flag Outlier (Dinamis dengan IQR)
                # cols_to_check = {
                #     'gap': gap_col, 'rms': rms_col, 'magNst': magnst_col, 
                #     'depth': dep_col, 'depthError': deperr_col
                # }
                # for feat, col_name in cols_to_check.items():
                #     if col_name in subset.columns:
                #         Q1, Q3 = subset[col_name].quantile(0.25), subset[col_name].quantile(0.75)
                #         IQR = Q3 - Q1
                #         subset[f'flag_outlier_{feat}'] = ((subset[col_name] < (Q1 - 1.5*IQR)) | 
                #                                          (subset[col_name] > (Q3 + 1.5*IQR))).astype(int)
                #     else:
                #         subset[f'flag_outlier_{feat}'] = 0
                # C. Flag Outlier (SINKRON DENGAN KODE IQR ANDA)
                outlier_features = ['gap', 'rms', 'magNst', 'depth', 'depthError']
                cols_mapping = {
                    'gap': gap_col, 'rms': rms_col, 'magNst': magnst_col, 
                    'depth': dep_col, 'depthError': deperr_col
                }

                for feat in outlier_features:
                    col_name = cols_mapping[feat]
                    Q1 = subset[col_name].quantile(0.25)
                    Q3 = subset[col_name].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    # Persis kodingan Python Anda
                    subset[f'flag_outlier_{feat}'] = np.where(
                        (subset[col_name] < lower_bound) | (subset[col_name] > upper_bound), 1, 0
                    )
                if not subset.empty:
                    X_input = subset[mlp_features_order]
                    X_scaled = scaler_x.transform(X_input)
                    y_pred_scaled = model_mlp.predict(X_scaled)
                    # Kembalikan ke nilai asli 'g'
                    pga_inv = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
                    # Clipping untuk mencegah nilai negatif secara fisik
                    subset['PGA_MLP'] = np.maximum(pga_inv, 0.0001)
                hybrid_results.append(subset)
            data_final = pd.concat(hybrid_results, ignore_index=True)

                # D. Jalankan Prediksi MLP
                # Pastikan semua kolom teknis yang mungkin tidak ada diisi 0
            #     for col in mlp_features_order:
            #         if col not in subset.columns:
            #             subset[col] = 0
                
            #     X_input = subset[mlp_features_order]
            #     X_scaled = scaler_x.transform(X_input)
            #     y_pred_scaled = model_mlp.predict(X_scaled)
                
            #     # Inverse transform ke satuan asli 'g'
            #     subset['PGA_MLP'] = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
                
            #     hybrid_results.append(subset)

            # # Gabungkan kembali hasil akhir
            # data_final = pd.concat(hybrid_results, ignore_index=True)
        
            
            progress_bar.progress(90)
            status_text.text("✅ Estimasi Hybrid Selesai!")
        else:
            st.error("Model MLP tidak ditemukan. Pastikan file .pkl sudah di-load.")
                    
        # ============================================
        # STEP 5: KALKULASI SELESAI
        # ============================================
        # data_final = pd.concat(temp_results, ignore_index=True)
        
        status_text.text("✅ Kalkulasi selesai!")
        progress_bar.progress(100)  # Update progress ke 100%
        
        # Simpan hasil ke session state untuk ditampilkan
        # SIMPAN HASIL KE SESSION STATE
        # Gunakan data_final (yang sudah ada GMPE & MLP untuk 5 tipe tanah)
        st.session_state['hasil_estimasi'] = data_final
        st.session_state['is_gmpe_done'] = True
        st.session_state['is_hybrid_done'] = True
        
        # Delay sebentar untuk animasi selesai
        import time
        time.sleep(0.5)
        
        # Clear progress bar dan status text
        progress_bar.empty()
        status_text.empty()
        
        # Success message
        st.success("🎉 Estimasi PGA berhasil!")
        
        # Reload halaman untuk tampilkan hasil
        st.rerun()
    
    # ============================================
    # SECTION 6: TAMPILKAN HASIL ESTIMASI
    # Bagian ini hanya tampil SETELAH estimasi selesai
    # ============================================
    
    # ============================================
    # SECTION 6: TAMPILKAN HASIL ESTIMASI
    # ============================================
    if 'hasil_estimasi' in st.session_state:
        st.markdown("---")
        st.header("📊 Hasil Analisis Estimasi PGA")
        
        # Load hasil dari session state
        df_result = st.session_state['hasil_estimasi']
        # Cek apakah kolom ada, jika tidak ada (karena salah nama), beri peringatan yang jelas
        if 'PGA_GMPE' not in df_result.columns:
            # Coba cari apakah dia bernama 'PGA_g' lalu rename otomatis
            if 'PGA_g' in df_result.columns:
                df_result = df_result.rename(columns={'PGA_g': 'PGA_GMPE'})
            else:
                st.error("Kolom 'PGA_GMPE' tidak ditemukan dalam data. Periksa penamaan di Step 5.")
                st.stop() # Hentikan proses agar tidak error baris bawahnya

        is_gmpe_done = st.session_state.get('is_gmpe_done', False)
        is_hybrid_done = st.session_state.get('is_hybrid_done', False)

        # ============================================
        # SUB-SECTION 6A: METRICS SUMMARY
        # ============================================
        st.markdown("### 📈 Ringkasan Rata-Rata PGA")
        col_m1, col_m2, col_m3 = st.columns(3)
        
        # Ambil rata-rata global untuk perbandingan cepat
        with col_m1:
            st.metric("PGA GMPE (Mean)", f"{df_result['PGA_GMPE'].mean():.4f} g")
        
        with col_m2:
            if 'PGA_MLP' in df_result.columns:
                st.metric("PGA MLP (Mean)", f"{df_result['PGA_MLP'].mean():.4f} g", 
                          delta=f"{df_result['PGA_MLP'].mean() - df_result['PGA_GMPE'].mean():.4f}",
                          delta_color="off")
        
        with col_m3:
            st.metric("Total Data Skenario", f"{len(df_result)}")

        # ============================================
        # SUB-SECTION 6B: FILTERING VIEW
        # ============================================
        st.markdown("### 📋 Dataset Hasil Estimasi")
        
        # Buat kolom filter di dalam satu baris
        f_col1, f_col2 = st.columns(2)
        
        with f_col1:
            # Filter berdasarkan Tipe Tanah
            soil_options = df_result['Tipe_Tanah'].unique().tolist()
            selected_soil = st.multiselect("Pilih Tipe Tanah:", soil_options, default=soil_options)
            
        with f_col2:
            # Filter berdasarkan Magnitude (Slider)
            mag_min = float(df_result[mapped_columns['magnitude']].min())
            mag_max = float(df_result[mapped_columns['magnitude']].max())
            selected_mag = st.slider("Filter Rentang Magnitude:", mag_min, mag_max, (mag_min, mag_max))

        # Terapkan Filter
        df_filtered = df_result[
            (df_result['Tipe_Tanah'].isin(selected_soil)) &
            (df_result[mapped_columns['magnitude']].between(selected_mag[0], selected_mag[1]))
        ].copy()

        # ============================================
        # SUB-SECTION 6C: TABEL HASIL
        # ============================================
        
        # Tentukan kolom yang akan ditampilkan agar tidak terlalu lebar
        display_cols = ['Tipe_Tanah', mapped_columns['magnitude'], mapped_columns['depth'], 'RJB_km']
        
        if is_gmpe_done:
            display_cols.append('PGA_GMPE')
        if is_hybrid_done:
            display_cols.append('PGA_MLP')
            
        # Penamaan ulang kolom agar lebih cantik di aplikasi
        rename_map = {
            mapped_columns['magnitude']: 'Magnitude',
            mapped_columns['depth']: 'Kedalaman (km)',
            'RJB_km': 'Jarak JB (km)',
            'PGA_GMPE': 'PGA GMPE (g)',
            'PGA_MLP': 'PGA Neural Network (g)'
        }
        
        # Tampilkan DataFrame
        st.dataframe(
            df_filtered[display_cols].rename(columns=rename_map),
            use_container_width=True,
            height=450
        )
        
        st.caption(f"Menampilkan {len(df_filtered)} skenario dari total data.")

        # Tombol Download untuk Keperluan Skripsi
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Estimasi (CSV)",
            data=csv_data,
            file_name='hasil_estimasi_pga_hybrid.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        # ============================================
        # SUB-SECTION 6C: VISUALISASI
        # Grafik interaktif menggunakan Plotly
        # ============================================
        
        # ============================================
        # SUB-SECTION 6C: VISUALISASI HASIL
        # ============================================
        st.markdown("---")
        st.markdown("### 📊 Visualisasi Perbandingan Metode")
        
        # Buat Main Tabs
        tab_gmpe, tab_ml = st.tabs(["🏛️ Metode GMPE (Klasik)", "🤖 Metode Hybrid (Neural Network)"])

        # === TAB 1: VISUALISASI GMPE ===
        with tab_gmpe:
            st.subheader("Analisis Klasik Boore-Atkinson (2008)")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                # 1. Histogram Distribusi PGA GMPE
                fig_hist = px.histogram(df_result, x='PGA_GMPE', 
                                       title="Distribusi Nilai PGA (GMPE)",
                                       color_discrete_sequence=['#3366CC'],
                                       labels={'PGA_GMPE': 'PGA (g)'})
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with c2:
                # 2. Scatter Magnitude vs PGA GMPE
                fig_scat = px.scatter(df_result, x=mapped_columns['magnitude'], y='PGA_GMPE',
                                     color='Tipe_Tanah', title="Magnitude vs PGA GMPE",
                                     labels={'PGA_GMPE': 'PGA (g)'})
                st.plotly_chart(fig_scat, use_container_width=True)

            # 3. Peta Sebaran PGA Indonesia
            st.markdown("#### 🗺️ Peta Distribusi Spasial PGA (GMPE)")
            fig_map = px.scatter_mapbox(df_result, 
                                       lat=mapped_columns['latitude'], 
                                       lon=mapped_columns['longitude'],
                                       color='PGA_GMPE', size='PGA_GMPE',
                                       color_continuous_scale='Reds',
                                       hover_name='Tipe_Tanah',
                                       zoom=4, center={"lat": -2.5, "lon": 118.0}, # Center Indonesia
                                       mapbox_style="open-street-map",
                                       title="Sebaran Intensitas PGA di Wilayah Target")
            fig_map.update_layout(height=600)
            st.plotly_chart(fig_map, use_container_width=True)

        # === TAB 2: VISUALISASI HYBRID (MLP) ===
        with tab_ml:
            st.subheader("Analisis Inteligensi Buatan (Neural Network)")
            
            # 1. Feature Importance (Penting untuk Skripsi)
            # Karena MLPRegressor tidak punya feature_importances_ secara native, 
            # kita gunakan bobot absolut dari layer pertama sebagai representasi
            st.markdown("#### 🔑 Feature Importance (Kontribusi Variabel)")
            try:
                # Mengambil koefisien dari layer pertama model MLP
                weights = np.abs(model_mlp.coefs_[0]).sum(axis=1)
                # Nama fitur sesuai urutan yang kita buat tadi
                feature_names = [
                    'Latitude', 'Longitude', 'Depth', 'Nst', 'Gap', 'RMS', 'MagNst',
                    'Soil_SA', 'Soil_SB', 'Soil_SC', 'Soil_SD', 'Soil_SE',
                    'F_Miss_Gap', 'F_Miss_RMS', 'F_Miss_MagNst', 'F_Miss_DErr', 'F_Miss_Nst',
                    'F_Out_Gap', 'F_Out_RMS', 'F_Out_MagNst', 'F_Out_Dep', 'F_Out_DErr'
                ]
                
                df_imp = pd.DataFrame({'Fitur': feature_names, 'Importance': weights})
                df_imp = df_imp.sort_values(by='Importance', ascending=True).tail(10) # Ambil top 10
                
                fig_imp = px.bar(df_imp, x='Importance', y='Fitur', orientation='h',
                                title="10 Variabel Paling Berpengaruh pada Prediksi MLP",
                                color='Importance', color_continuous_scale='Viridis')
                st.plotly_chart(fig_imp, use_container_width=True)
                st.info("💡 Grafik ini menunjukkan variabel mana yang paling 'diperhatikan' oleh Neural Network dalam menentukan nilai PGA.")
            except:
                st.warning("Gagal memuat Feature Importance. Pastikan model MLP sudah terload sempurna.")

            # # 2. Scatter Perbandingan (Sangat penting untuk validasi)
            # st.markdown("#### 🔄 Perbandingan Langsung: GMPE vs MLP")
            # fig_comp = px.scatter(df_result, x='PGA_GMPE', y='PGA_MLP', 
            #                      color='Tipe_Tanah', opacity=0.6,
            #                      trendline="ols", # Menambahkan garis tren linear
            #                      title="Korelasi Prediksi: Metode Klasik vs Hybrid")
            # # Garis diagonal 45 derajat (Ideal)
            # max_val = max(df_result['PGA_GMPE'].max(), df_result['PGA_MLP'].max())
            # fig_comp.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
            #                   line=dict(color="Red", dash="dash"))
            # st.plotly_chart(fig_comp, use_container_width=True)
        
        # ============================================
        # SUB-SECTION 6D: EXPORT HASIL
        # Download hasil dalam format CSV atau Excel
        # ============================================
        
        # ============================================
        # SUB-SECTION 6D: EXPORT HASIL
        # ============================================
        st.markdown("---")
        st.markdown("### 💾 Export Hasil")
        
        # Gunakan df_filtered (dari Section 6B) agar yang di-download 
        # sesuai dengan apa yang difilter user di layar.
        # Atau gunakan df_result jika ingin men-download SEMUA data.
        
        # Tambahkan import ini di paling atas script: from datetime import datetime
        from datetime import datetime 
        from io import BytesIO

        col_exp1, col_exp2 = st.columns(2)
        
        # === DOWNLOAD CSV ===
        with col_exp1:
            # Kita gunakan df_filtered yang sudah kita buat di sub-section sebelumnya
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Hasil (CSV)",
                data=csv,
                file_name=f"pga_hybrid_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # === DOWNLOAD EXCEL ===
        with col_exp2:
            output = BytesIO()
            # Gunakan engine openpyxl (pastikan sudah terinstall: pip install openpyxl)
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Hasil Estimasi PGA')
            
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Download Hasil (Excel)",
                data=excel_data,
                file_name=f"pga_hybrid_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================
        # BUTTON RESET / ESTIMASI ULANG
        # ============================================
        # Tambahkan desain yang agak berbeda (misal: secondary) agar tidak tertukar dengan tombol download
        if st.button("🔄 Estimasi Ulang dengan Parameter Berbeda", use_container_width=True, type="secondary"):
            # Menghapus semua state agar kembali ke kondisi awal upload data
            keys_to_delete = ['hasil_estimasi', 'is_gmpe_done', 'is_hybrid_done']
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            
            # Reload halaman
            st.rerun()

# ============================================
# END OF FILE
# ============================================