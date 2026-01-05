import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from scipy import stats
import joblib
import time
from io import BytesIO
from sklearn.metrics import mean_squared_error, r2_score

def show():
   

    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>
            🔬 Estimasi PGA
        </h1>
    </div>
    """, unsafe_allow_html=True)
   
    
   
    # Penjelasan Metode
    
    st.markdown("## 📚 Metodologi Estimasi PGA")
    st.markdown("""
    Sistem ini menggunakan dua pendekatan untuk estimasi Peak Ground Acceleration (PGA):
    """)
    
    # === Tab untuk kedua metode ===
    tab_gmpe, tab_ml = st.tabs(["Metode GMPE", "Metode Machine Learning"])
    
    # TAB Penjelasan Metode GMPE

    with tab_gmpe:  
        st.markdown("### Ground Motion Prediction Equations (GMPE)")
        
        # Semua informasi digabung dalam satu blockquote agar menyatu dalam satu box
        st.markdown("""
        **Metode Utama:** Boore-Atkinson 2008
        
        **Deskripsi:**
        
        GMPE adalah model matematis berbasis fisika yang digunakan untuk memprediksi seberapa kuat guncangan tanah di lokasi tertentu saat gempa terjadi. 
        Model Boore-Atkinson 2008 dipilih karena telah divalidasi secara global dan terbukti handal untuk wilayah dengan tektonik aktif seperti Aceh.
        
        **Parameter yang Dibutuhkan:**
                    
        Untuk menghasilkan estimasi yang akurat, metode ini memerlukan tiga data utama:
        - **Magnitudo ($M_w$)**: Skala kekuatan energi gempa di pusatnya.
        - **Jarak Joyner-Boore ($R_{jb}$)**: Jarak horizontal terdekat dari lokasi Anda ke titik di atas pusat gempa (km).
        - **$V_{S30}$**: Kondisi kekerasan tanah lokal (kecepatan gelombang geser hingga kedalaman 30 meter).
        
        **Formula:**
        
        $$ln(Y) = F_M(M) + F_D(M, R) + F_S(V_{S30}) + \epsilon$$
        
        Dengan:
        - **$F_M$ (Fungsi Magnitudo):** Menghitung pengaruh besarnya kekuatan gempa.
        - **$F_D$ (Fungsi Jarak):** Menghitung bagaimana guncangan melemah seiring bertambahnya jarak (atenuasi).
        - **$F_S$ (Fungsi Kondisi Tanah):** Menghitung penguatan guncangan jika tanah cenderung lunak (amplifikasi).
        - **$\epsilon$ (Variabel Error):** Mengakomodasi ketidakpastian alamiah dalam perhitungan.
        
        **Analisis Metode:**
        
        - **Kelebihan:** Sangat cepat untuk komputasi real-time, berbasis parameter fisik yang solid, dan efisien karena hanya membutuhkan input minimal.
        - **Keterbatasan:** Karena bersifat generalisasi dari data global, model ini mungkin tidak menangkap detail unik (variabilitas lokal) sesensitif model Machine Learning.
    
        
        **Referensi Ilmiah:**
        *Boore, D. M., & Atkinson, G. M. (2008). Earthquake Spectra, 24(1), 99-138.*
        
        
        """)
    
    # TAB Penjelasan Metode Hybrid
 
    with tab_ml:
        st.markdown("### Machine Learning (GMPE dan Neural Network)")

        
        st.markdown("""
        **Metode:** Multi-Layer Perceptron (MLP) Neural Network
        
        **Deskripsi:**
        
        Model machine learning ini menggunakan arsitektur Neural Network untuk menangkap 
        pola kompleks dalam data gempa Aceh yang mungkin tidak tertangkap oleh GMPE konvensional. 
        Model dilatih menggunakan data historis gempa USGS untuk wilayah Aceh (1900-2025).
        
        **Arsitektur Model:**
        - **Input Layer**: 23 fitur (Longitude, Latitude, depth, Nst, Gap, Rms, MagNST, DepthError, Soil_SA, Soil_SB, Soil_SC, Soil_SD, 
                    flag_outlier_depth, flag_outlier_Nst, flag_outlier_Gap, flag_outlier_Rms, flag_outlier_MagNst, flag_outlier_DepthError,
                    flag_missing_gap, flag_missing_rms, flag_missing_magNst, flag_missing_depthError, flag_missing_nst)
        - **Hidden Layers**: 2 Lapisan menggunakan 64 neurons untuk lapisan pertama dan 32 neurons untuk lapisan kedua
        - **Activation**: ReLU untuk hidden layers
        - **Output**: PGA prediction (g)
        
        **Parameter Input:**
        - **Magnitude**: Skala kekuatan energi gempa yang terjadi yang diukur dalam satuan Mw.
        - **Depth**: Kedalaman titik pusat gempa (hiposenter) di bawah permukaan bumi (km).
        - **Nst**: Jumlah total stasiun seismik yang berhasil merekam data kejadian gempa tersebut.
        - **Gap**: Celah sudut terbesar antar stasiun perekam; semakin kecil nilainya, semakin akurat penentuan lokasi gempa.
        - **RMS**: Rata-rata selisih waktu tempuh gelombang; nilai kecil menunjukkan data waktu yang sangat akurat.
        - **magNST**: Jumlah stasiun spesifik yang digunakan untuk menghitung nilai Magnitudo.
        - **depthError**: Tingkat ketidakpastian dalam penentuan kedalaman gempa (km).
        
        **Preprocessing:**
        - Standardization Proses menyamakan skala data agar semua variabel memiliki rata-rata 0 dan standar deviasi 1. 
        - Data split: Data dibagi menjadi dua bagian yaitu **80% untuk Training** (digunakan model untuk belajar pola) dan **20% untuk Testing** (digunakan untuk menguji seberapa pintar model menghadapi data baru yang belum pernah dilihat sebelumnya).
                
        **Performance Metrics:**
        - **RMSE (Root Mean Square Error)**: Ukuran standar deviasi dari residu prediksi
        - **R² Score**: Mengukur sebarapa mampu model menjelaskan variasi data.
        
        **Kelebihan:**
        - ✅ Mampu menangkap karakteristik unik dan variabilitas regional spesifik wilayah Aceh.
        - ✅ Dapat memproses hubungan non-linear antar parameter yang sulit dibaca oleh rumus matematika biasa.
        
        **Keterbatasan:**
        - ⚠️ Memerlukan input parameter yang lengkap (23 fitur) agar hasil estimasi maksimal.
        - ⚠️ Sangat bergantung pada kebersihan dan akurasi data historis yang dimasukkan.
        
               
        **Catatan:**
        
        Model ML ini **bukan pengganti GMPE**, melainkan **komplemen** yang memanfaatkan 
        informasi tambahan dari data gempa dengan harapan meningkatkan akurasi estimasi PGA.
        """)
           
    st.markdown("---")

    # Pengecekan Jika Data Belum Di Upload
       
    data_available = 'uploaded_data' in st.session_state
    
    if not data_available:
        
        # Info box warning
        st.info("""
        📊 **Data belum diupload.**
        
        Untuk melakukan estimasi PGA, silakan upload dataset terlebih dahulu di halaman **Data**.
        """)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn2:
            if st.button("📊 Ke Halaman Data", type="primary", use_container_width=True):
                st.session_state.page = 'Data'
                st.rerun()
        
        st.markdown("---")
        
        
        st.markdown("### Parameter Estimasi")
        st.caption("*Preview interface - aktif setelah upload data*")
        st.markdown("#### Lokasi Observasi")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude:", value="5.5483", disabled=True)
        with col2:
            st.text_input("Longitude:", value="95.3238", disabled=True)
        st.markdown("### Jalankan Estimasi")
        st.button("Mulai Estimasi PGA", type="primary", disabled=True, use_container_width=True)
        st.caption("*Upload data terlebih dahulu untuk mengaktifkan estimasi*")
        st.stop()
    
    # Jika Data Sudah Di Upload
    df = st.session_state['uploaded_data']  
    mapped_columns = st.session_state.get('mapped_columns', {})  # Mapping nama kolom
    
   
    # Check Metode yang dapat Dilakukan Kalkulasi
  
    # Check magnitudo untuk GMPE
    has_magnitude = 'magnitude' in mapped_columns
    
    # Check variabel untuk GMPE
    hybrid_columns = ['magnitude', 'depth', 'latitude', 'longitude', 
                      'nst', 'gap', 'rms', 'magnst', 'deptherror']
    
    # Check nama Kolom
    missing_hybrid = [col for col in hybrid_columns if col not in mapped_columns]
    
    
    is_gmpe_ready = has_magnitude  
    is_hybrid_ready = len(missing_hybrid) == 0  
    
 
    # Status Metode yang tersedia
 
    
    st.markdown("### 📋 Status Metode Estimasi")
    
    # kolom untuk status GMPE dan Hybrid
    col_status1, col_status2 = st.columns(2)
    
    # Status GMPE
    with col_status1:
        if is_gmpe_ready:
            # GMPE siap - tampilkan success box
            st.success("""**Metode GMPE Dapat Digunakan**""")
            if 'vs30' not in mapped_columns:
                st.warning("⚠️ VS30 menggunakan default SNI")
        else:
            # GMPE tidak siap - tampilkan error box
            st.error("""
            ❌ **Metode GMPE Tidak Dapat Digunakan**
                     
            - Kolom magnitude tidak ditemukan
            """)
    
    # Status Hybrid
    with col_status2:
        if is_hybrid_ready:
            st.success("✅ **Metode Hybrid Dapat Digunakan**")
            st.caption("Optimasi: Menggunakan Neural Network (MLP).")
        else:
            st.warning(f"""
            ⚠️ **Metode Hybrid Tidak Dapat Digunakan**
            
            - Kolom kurang: {', '.join(missing_hybrid)}
            - Hanya Metode GMPE yang akan dijalankan
            """)
    
    st.markdown("---")
    
    st.markdown("### Parameter Estimasi")

    # VS30 (SITE CONDITION)
    st.markdown("#### VS30 (Site Condition)")

    # Mapping VS30 Sesuai SNI
    tanah_mapping = {
        'SA - Batuan Keras': 1300,
        'SB - Batuan': 760,
        'SC - Tanah Keras': 520,
        'SD - Tanah Sedang': 250,
        'SE - Tanah Lunak': 180
    }
    
    st.markdown("""
    **VS30** adalah kecepatan gelombang geser rata-rata hingga kedalaman 30 meter.
    Nilai ini menggambarkan kondisi tanah di lokasi observasi.
    """)
    
    # Pengecekan Data VS30
    if 'vs30' in mapped_columns:
        vs30_col = mapped_columns['vs30'] 

        initial_rows = len(df)
        
        # Filter data: Only keep rows within Boore-Atkinson 2008 valid range (180 - 1300 m/s)
        df = df[(df[vs30_col] >= 180) & (df[vs30_col] <= 1300)].copy()
        
        final_rows = len(df)
        dropped_rows = initial_rows - final_rows
        
        if dropped_rows > 0:
            st.warning(f"⚠️ {dropped_rows} rows removed: VS30 values were outside BA08 valid range (180-1300 m/s).")
        
        # 
        if not df.empty:
            vs30_from_data = df[vs30_col].mean()
            st.success(f"✅ Using {final_rows} valid records (Mean VS30: {vs30_from_data:.1f} m/s)")
            
            st.session_state['run_mode'] = 'single'
            st.session_state['single_vs30'] = vs30_from_data
        else:
            st.error("❌ Critical Error: No valid VS30 data found within the 180-1300 m/s range!")
            st.stop()
            
    else:
    
        st.warning("⚠️ Kolom VS30 tidak ditemukan.")
        st.info("""
        **Mode Analisis Komparatif Aktif:** Sistem akan menghitung estimasi PGA untuk seluruh klasifikasi situs berdasarkan **SNI 1726:2019**. 
        Hasil akan ditampilkan dalam bentuk perbandingan antar kelas tanah.
        """)
    
        with st.expander("Lihat Referensi Nilai VS30 yang Digunakan"):
            st.table(pd.DataFrame({
                'Kelas Situs': tanah_mapping.keys(),
                'Nilai VS30 (m/s)': tanah_mapping.values()
            }))

        st.session_state['run_mode'] = 'multi'
        st.session_state['active_vs30_map'] = tanah_mapping
        
    st.markdown("<br>", unsafe_allow_html=True)
   
    
    
    # LOKASI OBSERVASI 
    st.markdown("#### Lokasi Target Estimasi")
    
    st.info("""
    Masukkan koordinat lokasi yang ingin Anda analisis (Lokasi Proyek/Kota). 
    Sistem akan menghitung dampak PGA di titik ini dari **seluruh kejadian gempa** yang ada dalam dataset Anda.
    """)

    col_lat, col_lon = st.columns(2)

    with col_lat:
    
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
    
    # Mulai Estimasi
    model_mlp = joblib.load('model_pga_mlp.pkl')
    scaler_x = joblib.load('scaler_x.pkl')
    scaler_y = joblib.load('scaler_y.pkl')

    def haversine(lat1, lon1, lat2, lon2):
            """Menghitung jarak episentral (km) antara dua koordinat"""
            R = 6371  
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
                
                new_df[f'flag_outlier_{col}'] = ((new_df[col] < lower_bound) | (new_df[col] > upper_bound)).astype(int)
            else:
                new_df[f'flag_outlier_{col}'] = 0
        return new_df
    
    def classify_vs30(vs30_val):
        """
        Mengklasifikasikan nilai VS30 ke dalam kategori SNI 1726:2019
        untuk diumpankan ke fitur One-Hot Encoding MLP (Soil_SA s/d Soil_SE)
        """
        if vs30_val >= 760:
            return 'SA' if vs30_val >= 1300 else 'SB'
        elif 360 <= vs30_val < 760:
            return 'SC'
        elif 180 <= vs30_val < 360:
            return 'SD'
        else:
            return 'SE'
    
    st.markdown("### Jalankan Estimasi")
    
    # Button untuk mulai kalkulasi
    if st.button("Mulai Estimasi PGA", type="primary", use_container_width=True):

        if target_latitude == 0.0:
            st.error("Mohon masukkan koordinat lokasi target Anda.")
            st.stop()

        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Mencari Jarak RJB
        status_text.text("Menghitung jarak episenter...")
        progress_bar.progress(10)  
        df_calc = df.copy()

        epi_lat_col = mapped_columns['latitude']
        epi_lon_col = mapped_columns['longitude']
        mag_col = mapped_columns['magnitude']
        dep_col = mapped_columns['depth']

        df_calc['RJB_km'] = df_calc.apply(
            lambda row: haversine(row[epi_lat_col], row[epi_lon_col], target_latitude, target_longitude), 
            axis=1
        )
        
        progress_bar.progress(20)  
        
        # Filtering Data VS30, depth dan mag
        status_text.text("Melakukan filtering data...")

        condition = (df_calc[mag_col] >= 5.0) & (df_calc[dep_col] > 0) & (df_calc['RJB_km'] <= 200)
        
        # Filter VS30 jika kolomnya ada (BA08 Range: 180 - 1300)
        if 'vs30' in mapped_columns:
            vs30_col = mapped_columns['vs30']
            condition &= (df_calc[vs30_col] >= 180) & (df_calc[vs30_col] <= 1300)
            
        data_clean = df_calc[condition].copy()
        
        if data_clean.empty:
            st.error("❌ Tidak ada data yang memenuhi kriteria validitas (M>=5, Dist<=200km, VS30 180-1300).")
            st.stop()

        progress_bar.progress(40)
       
     
        # Analisis Gutenberg Ritcher Law
       
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


        # Metode GMPE 
        status_text.text("🧬 Menghitung PGA GMPE...")
        
        tanah_mapping = {
            'SA': 1300, 'SB': 760, 'SC': 520, 'SD': 250, 'SE': 180
        }

        final_scenario = []
        for label, vs_val in tanah_mapping.items():
            subset = data_clean.copy()
            subset['Tipe_Tanah'] = label
            if 'vs30' in mapped_columns:
                subset['Vs30_m_s'] = subset[mapped_columns['vs30']]
            else:
                subset['Vs30_m_s'] = vs_val
            # Hitung PGA menggunakan fungsi BA08
            subset['PGA_GMPE'] = BA08(subset[mag_col], subset['RJB_km'], subset['Vs30_m_s'])
            final_scenario.append(subset)
        
    
        data_final = pd.concat(final_scenario, ignore_index=True)
        
        progress_bar.progress(70)
        status_text.text("✅ Estimasi Selesai!")

        st.markdown("### 📋 Dataset Hasil Estimasi (Multi-Skenario)")
        st.dataframe(data_final)
        

        # Estimasi GMPE + ML

        if is_hybrid_ready and ('model_mlp' in globals() or 'model_mlp' in locals()):
            
            # Kalkulasi Menggunakan neural Network
            status_text.text("Menjalankan model Machine Learning (MLP)...")

            nst_col = mapped_columns.get('nst')
            gap_col = mapped_columns.get('gap')
            rms_col = mapped_columns.get('rms')
            magnst_col = mapped_columns.get('magnst')
            deperr_col = mapped_columns.get('deptherror')
            epi_lat_col = mapped_columns.get('latitude')
            epi_lon_col = mapped_columns.get('longitude')
            dep_col = mapped_columns.get('depth')

            mlp_features_order = [
                'latitude', 'longitude', 'depth', 'nst', 'gap', 'rms', 'magNst',
                'Soil_SA', 'Soil_SB', 'Soil_SC', 'Soil_SD', 'Soil_SE',
                'flag_missing_gap', 'flag_missing_rms', 'flag_missing_magNst', 
                'flag_missing_depthError', 'flag_missing_nst',
                'flag_outlier_gap', 'flag_outlier_rms', 'flag_outlier_magNst', 
                'flag_outlier_depth', 'flag_outlier_depthError'
            ]

            hybrid_results = []
            for label in tanah_mapping.keys():
                subset = data_final[data_final['Tipe_Tanah'] == label].copy()
                if subset.empty: continue

                # Penentuan Tipe Tanah
                for idx, row in subset.iterrows():
                    # Tentukan kategori tanah berdasarkan VS30 asli
                    target_class = classify_vs30(row['Vs30_m_s'])
                    for s in tanah_mapping.keys():
                        subset.loc[idx, f'Soil_{s}'] = 1 if target_class == s else 0

                    rename_map = {
                    epi_lat_col: 'latitude',
                    epi_lon_col: 'longitude',
                    dep_col: 'depth',
                    nst_col: 'nst',
                    gap_col: 'gap',
                    rms_col: 'rms',
                    magnst_col: 'magNst', 
                    deperr_col: 'depthError' 
                }
                subset = subset.rename(columns=rename_map)

                cols_to_flag = ['gap', 'rms', 'magNst', 'depthError', 'nst']

                # Flag Missing & Outlier 
                for m in cols_to_flag:
                    subset[f'flag_missing_{m}'] = 0 

                # Outlier Detection (IQR)
                target_outliers = ['nst', 'gap', 'rms', 'magNst', 'depth', 'depthError']
                for feat in target_outliers:
                    Q1 = subset[feat].quantile(0.25)
                    Q3 = subset[feat].quantile(0.75)
                    IQR = Q3 - Q1
                    subset[f'flag_outlier_{feat}'] = np.where(
                        (subset[feat] < (Q1 - 1.5*IQR)) | (subset[feat] > (Q3 + 1.5*IQR)), 1, 0
                    )
                # Prediksi MLP
                # Pastikan urutan mlp_features_order SAMA dengan saat training!
                X_input = subset[mlp_features_order]
                X_scaled = scaler_x.transform(X_input)
                y_pred_scaled = model_mlp.predict(X_scaled)
                pga_inv = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
                subset['PGA_MLP'] = np.maximum(pga_inv, 0.0001)
                
                hybrid_results.append(subset)

            data_final = pd.concat(hybrid_results, ignore_index=True)
            progress_bar.progress(95)
            status_text.text("✅ Estimasi Hybrid Selesai!")
            
        
        else:
            status_text.text("✅ Estimasi GMPE Selesai (Fitur Hybrid tidak lengkap)")
            progress_bar.progress(100)
                    

        # Kalkulasi Selesai
        status_text.text("✅ Kalkulasi selesai!")
        progress_bar.progress(100)
        

        st.session_state['hasil_estimasi'] = data_final
        st.session_state['is_gmpe_done'] = True

        if 'PGA_MLP' in data_final.columns:
            st.session_state['is_hybrid_done'] = True
        else:
            st.session_state['is_hybrid_done'] = False
        
        
        time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
        
        st.success("Estimasi PGA berhasil!")
        st.rerun()

        if st.session_state.get('is_gmpe_done'):
            st.subheader("Visualisasi Hasil Estimasi")
            df_hasil = st.session_state['hasil_estimasi']
            
            st.dataframe(df_hasil.head())
            
            if st.session_state.get('is_hybrid_done'):
                st.info("💡 Data ini mencakup perbandingan metode Empiris (GMPE) dan Neural Network (MLP).")

   
    # Hasil Estimasi
    if 'hasil_estimasi' in st.session_state:
        st.markdown("---")
        st.header("Hasil Analisis Estimasi PGA")
        
        # Load hasil dari session state
        df_result = st.session_state['hasil_estimasi']
        
        # Validasi Kolom
        if 'PGA_GMPE' not in df_result.columns:
            if 'PGA_g' in df_result.columns:
                df_result = df_result.rename(columns={'PGA_g': 'PGA_GMPE'})
            else:
                st.error("Kolom 'PGA_GMPE' tidak ditemukan.")
                st.stop()

        is_gmpe_done = st.session_state.get('is_gmpe_done', False)
        is_hybrid_done = st.session_state.get('is_hybrid_done', False)


        st.markdown("### Ringkasan Rata-Rata PGA")
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("PGA GMPE (Mean)", f"{df_result['PGA_GMPE'].mean():.4f} g")
        
        with col_m2:
            if is_hybrid_done:
                diff_mean = df_result['PGA_MLP'].mean() - df_result['PGA_GMPE'].mean()
                st.metric("PGA MLP (Mean)", f"{df_result['PGA_MLP'].mean():.4f} g", 
                        delta=f"{diff_mean:.4f}", delta_color="off")
        
        with col_m3:
            st.metric("Total Data Skenario", f"{len(df_result)}")


        # Filter Hasil Tabel
        st.markdown("### Dataset Hasil Estimasi")
        
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            soil_options = df_result['Tipe_Tanah'].unique().tolist()
            selected_soil = st.multiselect("Pilih Tipe Tanah:", soil_options, default=soil_options)
        with f_col2:
            mag_col = mapped_columns['magnitude']
            mag_min, mag_max = float(df_result[mag_col].min()), float(df_result[mag_col].max())
            selected_mag = st.slider("Filter Rentang Magnitude:", mag_min, mag_max, (mag_min, mag_max))

        # Terapkan Filter Berdasarkan tanah
        df_filtered = df_result[
            (df_result['Tipe_Tanah'].isin(selected_soil)) &
            (df_result[mag_col].between(selected_mag[0], selected_mag[1]))
        ].copy()


        display_cols = ['Tipe_Tanah', mag_col, mapped_columns['depth'], 'RJB_km', 'PGA_GMPE']
        if is_hybrid_done: display_cols.append('PGA_MLP')
        
        rename_map = {mag_col: 'Magnitude', mapped_columns['depth']: 'Kedalaman (km)', 
                    'RJB_km': 'Jarak JB (km)', 'PGA_GMPE': 'PGA GMPE (g)', 'PGA_MLP': 'PGA MLP (g)'}
        
        st.dataframe(df_filtered[display_cols].rename(columns=rename_map), use_container_width=True, height=400)
        st.caption(f"Menampilkan {len(df_filtered)} skenario.")


        # RMSE dan R^2 data User
        if is_hybrid_done:
            st.markdown("---")
            st.subheader("Validasi Akurasi pada Data Anda")
            st.write("Statistik ini mengukur seberapa presisi Neural Network dalam mereplikasi model GMPE pada dataset ini:")

            from sklearn.metrics import mean_squared_error, mean_absolute_error
            
            y_true = df_filtered['PGA_GMPE']
            y_pred = df_filtered['PGA_MLP']
            
            # Menghitung Metrik Absolut
            user_rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            user_mae = mean_absolute_error(y_true, y_pred)
            avg_corr = (y_pred - y_true).abs().mean()

            u_col1, u_col2, u_col3 = st.columns(3)
            with u_col1:
                st.metric("MAE (Rata-rata Error)", f"{user_mae:.5f} g")
                st.caption("Semakin kecil MAE, semakin dekat MLP dengan GMPE.")
            with u_col2:
                st.metric("RMSE (Deviasi Error)", f"{user_rmse:.5f} g")
                st.caption("Mengukur penyebaran error prediksi.")
            with u_col3:
                st.metric("Avg. Correction", f"{avg_corr:.5f} g")
                st.caption("Rata-rata penyesuaian oleh variabel tambahan.")

            st.info("ℹ️ **Keterangan:** Nilai RMSE dan R² di atas menunjukkan tingkat keselarasan model MLP terhadap standar GMPE. "
                    "Adanya selisih (Correction) menunjukkan peran variabel tambahan (NST, GAP, dll) dalam menyesuaikan nilai estimasi.")
        
       
        # Visualisasi
        st.markdown("---")
        st.markdown("### Visualisasi Perbandingan Metode")

        # Buat Main Tabs
        tab_gmpe, tab_ml = st.tabs(["Metode GMPE ", "Metode Hybrid (GMPE + Neural Network)"])

        # Visualisasi GMPE
        with tab_gmpe:
            st.subheader("Analisis Klasik Boore-Atkinson (2008)")
            
            # Peta Sebaran PGA GMPE
            st.markdown("#### Peta Distribusi Spasial PGA (GMPE)")
            fig_map_gmpe = px.scatter_mapbox(df_result, 
                                        lat=mapped_columns['latitude'], 
                                        lon=mapped_columns['longitude'],
                                        color='PGA_GMPE', size='PGA_GMPE',
                                        color_continuous_scale='Reds',
                                        hover_data=[mapped_columns['magnitude'], 'RJB_km', 'Tipe_Tanah'],
                                        zoom=4, center={"lat": -2.5, "lon": 118.0},
                                        mapbox_style="open-street-map",
                                        title="Intensitas PGA (GMPE) di Wilayah Target")
            st.plotly_chart(fig_map_gmpe, use_container_width=True)

            # Visualisasi Pola (Mag, RJB, Tipe Tanah)
            st.markdown("#### Analisis Pola Parameter GMPE")
            c1, c2 = st.columns(2)
            with c1:
                # Magnitude vs PGA
                fig_mag = px.scatter(df_result, x=mapped_columns['magnitude'], y='PGA_GMPE',
                                color='Tipe_Tanah', title="Magnitude vs PGA GMPE")
                st.plotly_chart(fig_mag, use_container_width=True)
            with c2:
                # Jarak (RJB) vs PGA
                fig_rjb = px.scatter(df_result, x='RJB_km', y='PGA_GMPE',
                                color='Tipe_Tanah', title="Jarak (RJB) vs PGA GMPE")
                st.plotly_chart(fig_rjb, use_container_width=True)

        # Visualisasi Hybrid
        with tab_ml:
            st.subheader("Analisis Inteligensi Buatan (Neural Network)")
            
            # Peta Sebaran PGA ML
            st.markdown("#### Peta Distribusi Spasial PGA (Neural Network)")
            fig_map_mlp = px.scatter_mapbox(df_result, 
                                        lat=mapped_columns['latitude'], 
                                        lon=mapped_columns['longitude'],
                                        color='PGA_MLP', size='PGA_MLP',
                                        color_continuous_scale='Bluered', 
                                        hover_data=[mapped_columns['magnitude'], 'RJB_km', 'Tipe_Tanah'],
                                        zoom=4, center={"lat": -2.5, "lon": 118.0},
                                        mapbox_style="open-street-map",
                                        title="Intensitas PGA (MLP) di Wilayah Target")
            st.plotly_chart(fig_map_mlp, use_container_width=True)

            # Visualisasi RMSE & MAE
            st.markdown("#### Metrik Akurasi Model terhadap GMPE")
            y_true = df_result['PGA_GMPE']
            y_pred = df_result['PGA_MLP']
            u_rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            u_mae = mean_absolute_error(y_true, y_pred)

            col_acc1, col_acc2 = st.columns(2)
            with col_acc1:
                fig_r2 = go.Figure(go.Indicator(
                    mode = "gauge+number", value = u_mae,
                    title = {'text': "MAE (Mean Absolute Error)"},
                    gauge = {'axis': {'range': [0, 1]}, 'bar': {'color': "darkblue"}}))
                st.plotly_chart(fig_r2, use_container_width=True)
            with col_acc2:
                fig_rmse = go.Figure(go.Indicator(
                    mode = "gauge+number", value = u_rmse,
                    title = {'text': "RMSE (Root Mean Square Error)"},
                    gauge = {'axis': {'range': [0, 0.2]}, 'bar': {'color': "darkred"}}))
                st.plotly_chart(fig_rmse, use_container_width=True)

            # Feature Importance
            st.markdown("#### Kontribusi Variabel terhadap Prediksi")
            try:
                weights = np.abs(model_mlp.coefs_[0]).sum(axis=1)

                feature_names = [
                    'Latitude', 'Longitude', 'Depth', 'Nst', 'Gap', 'RMS', 'MagNst',
                    'Soil_SA', 'Soil_SB', 'Soil_SC', 'Soil_SD', 'Soil_SE',
                    'F_Miss_Gap', 'F_Miss_RMS', 'F_Miss_MagNst', 'F_Miss_DErr', 'F_Miss_Nst',
                    'F_Out_Gap', 'F_Out_RMS', 'F_Out_MagNst', 'F_Out_Dep', 'F_Out_DErr'
                ]
                df_imp = pd.DataFrame({'Fitur': feature_names, 'Importance': weights}).sort_values(by='Importance', ascending=True)
                
                fig_imp = px.bar(df_imp.tail(12), x='Importance', y='Fitur', orientation='h',
                                title="Top 12 Fitur Paling Berpengaruh",
                                color='Importance', color_continuous_scale='Viridis')
                st.plotly_chart(fig_imp, use_container_width=True)
            except Exception as e:
                st.warning(f"Feature Importance tidak dapat dimuat: {e}")

            # Notes
            st.warning("""
            ⚠️ **Catatan Penting:** Hasil estimasi menggunakan metode **Neural Network (MLP)** ini dikembangkan sebagai model pendukung untuk mengoreksi atau memperhalus hasil dari metode empiris. 
                       
                       Metode ini **tidak ditujukan untuk menggantikan standar peraturan bangunan tahan gempa** (seperti SNI 1726) yang berlaku, 
                       melainkan sebagai instrumen analisis tambahan untuk melihat pengaruh kualitas data seismik terhadap nilai percepatan tanah.
            """)

        # Export Hasil
        st.markdown("---")
        st.markdown("### Export Hasil")

        st.info(f"Data yang akan diunduh mencakup {len(df_filtered)} baris hasil estimasi berdasarkan filter yang Anda terapkan.")

        col_exp1, col_exp2 = st.columns(2)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Download CSV
        with col_exp1:
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Hasil (CSV)",
                data=csv,
                file_name=f"pga_hybrid_export_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Download Excel
        with col_exp2:
            output = BytesIO()
            try:
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtered.to_excel(writer, index=False, sheet_name='Hasil Estimasi PGA')
                
                excel_data = output.getvalue()
                st.download_button(
                    label="Download Hasil (Excel)",
                    data=excel_data,
                    file_name=f"pga_hybrid_export_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Gagal membuat file Excel. Pastikan library 'openpyxl' terinstall. Error: {e}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Button Reset
        if st.button("Estimasi Ulang dengan Parameter Berbeda", use_container_width=True, type="secondary"):
            keys_to_delete = ['hasil_estimasi', 'is_gmpe_done', 'is_hybrid_done']
            
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()