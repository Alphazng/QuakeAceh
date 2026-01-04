# ============================================
# IMPORT LIBRARIES
# ============================================
import streamlit as st
import pandas as pd
import numpy as np

# ============================================
# FUNCTION HALAMAN DATA
# ============================================
def show():
    """
    Halaman Data - Upload & Validasi Dataset
    
    Fitur:
    1. Penjelasan dataset yang baik
    2. Upload file (CSV/Excel)
    3. Validasi missing values
    4. Preview data
    """
    
    # ============================================
    # HEADER HALAMAN
    # EDITABLE: Judul halaman
    # ============================================
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f2937; font-size: 2.5rem; margin-bottom: 0.5rem;'>
            Upload Data Gempa
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>
            Unggah dataset gempa Anda untuk estimasi PGA
        </p>
    </div>
    """, unsafe_allow_html=True)
    # EDITABLE: Ganti judul dan subtitle
    
    # ============================================
    # SECTION 1: PENJELASAN DATASET YANG BAIK
    # EDITABLE: Kriteria dataset, contoh, tips
    # ============================================
    
    st.markdown("### Kriteria Dataset untuk Estimasi PGA")
    # EDITABLE: Title section
    
    st.markdown("""
    Untuk mendapatkan **estimasi PGA yang tinggi dan akurat**, dataset gempa Anda harus memenuhi kriteria berikut:
    """)
    # EDITABLE: Penjelasan intro
    
    # === Info Box: Kriteria Dataset ===
    st.info("""
    **Indikator Wajib Dalam Dataset**
    
    1. **Perhitungan Menggunakan GMPE:**
       - `Magnitudo`: Magnitudo gempa dalam skala Moment Magnitude (M_w)   
    2. **Perhitungan Menggunakan GMPE dan Machine Learning:**
       - `Nilai PGA`: Nilai estimasi percepatan tanah puncak yang dihitung menggunakan rumus GMPE. 
       - `NST`: Jumlah total stasiun seismik yang digunakan untuk menentukan parameter lokasi gempa (pusat gempa).
       - `Gap`: Celah sudut terbesar antar stasiun perekam relatif terhadap pusat gempa
       - `RMS`: Nilai sisa (residual) rata-rata dari waktu tempuh gelombang.
       - `magNST`: Jumlah stasiun yang secara spesifik berkontribusi dalam menentukan nilai Magnitudo gempa.
       - `Depth`: Kedalaman sumber gempa (hiposenter) di bawah permukaan bumi (dalam km).
       - `DepthError`: PNilai ketidakpastian atau kesalahan estimasi pada parameter kedalaman (dalam km).
                
    """)
    # EDITABLE: Ganti kriteria sesuai kebutuhan sistem Anda
    # EDITABLE: Ubah range nilai (magnitude, depth, dll)
    
    # # === Expander: Contoh Format Dataset ===
    # with st.expander("📄 Lihat Contoh Format Dataset"):
    #     # EDITABLE: Contoh data dummy
    #     st.markdown("**Contoh format CSV yang benar:**")
        
    #     # Buat sample data
    #     sample_data = pd.DataFrame({
    #         'magnitude': [5.2, 6.1, 5.8, 4.9, 6.5],
    #         'depth': [10.5, 35.2, 15.0, 8.3, 45.6],
    #         'latitude': [5.55, 5.48, 5.62, 5.41, 5.53],
    #         'longitude': [95.32, 95.28, 95.35, 95.25, 95.30]
    #     })
    #     # EDITABLE: Ganti dengan sample data yang sesuai
    #     # EDITABLE: Tambah kolom lain jika diperlukan (contoh: time, place, dll)
        
    #     st.dataframe(sample_data, use_container_width=True)
        
    #     st.markdown("""
    #     **Penjelasan kolom:**
    #     - `magnitude`: Kekuatan gempa (skala Richter/Moment)
    #     - `depth`: Kedalaman fokus gempa dari permukaan (km)
    #     - `latitude`: Koordinat lintang lokasi gempa
    #     - `longitude`: Koordinat bujur lokasi gempa
    #     """)
    #     # EDITABLE: Tambah penjelasan kolom tambahan jika ada
    
    # # === Expander: Tips Dataset Berkualitas ===
    # with st.expander("💡 Tips Mendapatkan Dataset Berkualitas"):
    #     st.markdown("""
    #     **Sumber Data Terpercaya:**
        
    #     1. **USGS Earthquake Catalog**
    #        - Website: https://earthquake.usgs.gov/earthquakes/search/
    #        - Data global, real-time, akurat
    #        - Format: CSV download langsung
        
    #     2. **BMKG Indonesia**
    #        - Website: https://www.bmkg.go.id/
    #        - Data gempa wilayah Indonesia
    #        - Fokus untuk gempa lokal Aceh
        
    #     3. **ISC Bulletin**
    #        - Website: http://www.isc.ac.uk/
    #        - Data gempa global yang sudah diverifikasi
        
    #     **Preprocessing Data:**
    #     - Hapus duplikat data
    #     - Filter magnitude ≥ 4.0 (untuk konsistensi)
    #     - Filter region yang relevan (contoh: Aceh dan sekitarnya)
    #     - Konversi satuan jika perlu (contoh: depth dalam km)
    #     """)
    #     # EDITABLE: Tambah/hapus sumber data sesuai kebutuhan
    #     # EDITABLE: Ubah tips preprocessing
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 2: FILE UPLOADER
    # EDITABLE: Tipe file, max size
    # ============================================
    
    st.markdown("### Upload Dataset Gempa")
    # EDITABLE: Title section
    
    st.markdown("""
    Silakan upload file dataset gempa Anda dalam format **CSV** atau **Excel**.
    """)
    # EDITABLE: Instruksi upload
    
    # === File Uploader ===
    uploaded_file = st.file_uploader(
        "Pilih file dataset",                          # EDITABLE: Label uploader
        type=['csv', 'xlsx', 'xls'],                   # EDITABLE: Tipe file yang diterima
        help="Upload file CSV atau Excel yang berisi data gempa"  # EDITABLE: Help text
    )
    # EDITABLE: Tambah type lain jika perlu (contoh: 'txt', 'json')
    
    # ============================================
    # SECTION 3: VALIDASI & PREVIEW DATA
    # ============================================

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"File **{uploaded_file.name}** berhasil diupload!")
            st.markdown("---")
            
            # 1. LOGIKA ALIASING KOLOM (Mendeteksi variasi nama kolom)
            # Mendefinisikan variasi nama yang mungkin diinput user
            column_aliases = {
                'magnitude': ['magnitude', 'mag', 'm', 'mw', 'mag_mw'],
                'vs30': ['vs30', 'v_s30', 's-wave_velocity'],
                'depth': ['depth', 'kedalaman', 'd', 'dep'],
                'latitude': ['latitude', 'lat', 'lintang', 'y'],
                'longitude': ['longitude', 'lon', 'long', 'bujur', 'x'],
                'nst': ['nst', 'number_of_stations', 'stn_count'],
                'magnst': ['magnst', 'mag_nst'],
                'gap': ['gap', 'azimuthal_gap'],
                'rms': ['rms', 'root_mean_square'],
                'deptherror': ['deptherror', 'depth_error', 'err_depth']
            }

            # Fungsi untuk memetakan kolom user ke standar sistem
            actual_columns = {col.lower(): col for col in df.columns}
            mapped_columns = {}
            for key, aliases in column_aliases.items():
                for alias in aliases:
                    if alias in actual_columns:
                        mapped_columns[key] = actual_columns[alias]
                        break

            # 2. ANALISIS KESIAPAN METODE
            st.markdown("### 🔍 Analisis Kesiapan Metode")
            
            # Syarat minimal GMPE: Magnitude (Vs30 bisa opsional dengan nilai standar)
            has_mag = 'magnitude' in mapped_columns
            is_gmpe_ready = has_mag # Minimal ada Magnitudo dan Jarak (Jarak dihitung dari Lat/Lon nanti)

            # Syarat Hybrid: Semua kolom teknis tersedia
            missing_hybrid = [k for k in column_aliases.keys() if k not in mapped_columns]
            is_hybrid_ready = is_gmpe_ready and (len(missing_hybrid) == 0)

            col_st1, col_st2 = st.columns(2)
            with col_st1:
                if is_gmpe_ready:
                    st.success("✅ **Metode GMPE**")
                else:
                    st.error("❌ **Metode GMPE: TIDAK SIAP**")
                    st.caption("Pastikan ada kolom 'Magnitude'")

            with col_st2:
                if is_hybrid_ready:
                    st.success("✅ **Metode Hybrid (ML)**")
                else:
                    st.warning("⚠️ **Metode Hybrid**")
                    st.caption(f"Kolom tidak ditemukan: {', '.join(missing_hybrid)}")

            # 3. PENANGANAN VS30 (STANDAR SNI)
            if 'vs30' not in mapped_columns:
                st.info("💡 **Info VS30:** Kolom VS30 tidak ditemukan. Sistem akan menggunakan nilai standar **SNI 1726:2019** sebagai asumsi.")
                # Di tahap kalkulasi nanti, Anda tinggal mengisi df['vs30'] = 350

            # 4. DETEKSI MISSING VALUES (PER BARIS)
            st.markdown("---")
            st.markdown("### Validasi Isi Data")
            
            if df.isnull().values.any():
                # Cari baris mana saja yang ada nilai kosongnya
                rows_with_nan = df[df.isnull().any(axis=1)].index.tolist()
                # Ubah index menjadi nomor baris (mulai dari 1 atau sesuai urutan CSV)
                rows_display = [r + 1 for r in rows_with_nan] 
                
                st.error(f"⚠️ **Ditemukan Missing Values!**")
                st.write(f"Data kosong ditemukan pada baris ke: `{rows_display[:10]}`" + ("..." if len(rows_display) > 10 else ""))
                
                # Tampilkan detail kolom yang kosong
                nan_details = df.isnull().sum()
                st.dataframe(nan_details[nan_details > 0], column_config={0: "Jumlah Kosong"})
                st.stop()
            else:
                st.success("✅ Tidak ada nilai kosong. Data siap diproses.")

            # 5. PREVIEW DATA
            st.markdown("---")
            st.markdown("### Preview Dataset")
            st.dataframe(df.head(10), use_container_width=True)

            # Simpan ke session state
            st.session_state['uploaded_data'] = df
            st.session_state['mapped_columns'] = mapped_columns # Penting untuk tahu nama kolom asli user

            if is_gmpe_ready:
                if st.button(" Lanjut ke Estimasi PGA", type="primary"):
                    st.session_state.page = 'Estimasi PGA'
                    st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")

    else:
        st.info("Silakan upload file dataset gempa Anda untuk memulai validasi.")