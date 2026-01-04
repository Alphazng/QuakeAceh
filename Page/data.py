import streamlit as st
import pandas as pd
import numpy as np


def show():   
    # HEADER HALAMAN
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style = font-size: 2.5rem; margin-bottom: 0.5rem;'>
            Data Gempa
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    
    # PENJELASAN DATASET

    st.markdown("### Kriteria Dataset untuk Estimasi PGA")
    
    st.info("""
    1. **Perhitungan Menggunakan GMPE:**
       - `Magnitudo`: Magnitudo gempa dalam skala Moment Magnitude (M_w)   
    2. **Perhitungan Menggunakan GMPE dan Machine Learning:**
       - `Nilai PGA`: Nilai estimasi percepatan tanah puncak yang dihitung menggunakan rumus GMPE. 
       - `NST`: Jumlah total stasiun seismik yang digunakan untuk menentukan parameter lokasi gempa (pusat gempa).
       - `Gap`: Celah sudut terbesar antar stasiun perekam relatif terhadap pusat gempa
       - `RMS`: Nilai sisa (residual) rata-rata dari waktu tempuh gelombang.
       - `MagNST`: Jumlah stasiun yang secara spesifik berkontribusi dalam menentukan nilai Magnitudo gempa.
       - `Depth`: Kedalaman sumber gempa (hiposenter) di bawah permukaan bumi (dalam km).
       - `DepthError`: Nilai ketidakpastian atau kesalahan estimasi pada parameter kedalaman (dalam km).
                
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Data
    st.markdown("### Upload Dataset Gempa")
        
    st.markdown("""
    Silakan upload file dataset gempa Anda dalam format **CSV** atau **Excel**.
    """)

    uploaded_file = st.file_uploader(
        "Pilih file dataset",                          
        type=['csv', 'xlsx', 'xls'],                   
        help="Unggah file CSV atau Excel yang berisi data gempa"  
    )
    
    # Valdasi dan Preview Data

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"File **{uploaded_file.name}** berhasil diupload!")
            st.markdown("---")
            
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

            # Pengecekan kolom
            actual_columns = {col.lower(): col for col in df.columns}
            mapped_columns = {}
            for key, aliases in column_aliases.items():
                for alias in aliases:
                    if alias in actual_columns:
                        mapped_columns[key] = actual_columns[alias]
                        break

            # Pemilihan Metode
            st.markdown("### Validasi Kualitas Data")


            # Cek Data Hilang
            if df.isnull().values.any():
                st.error("### 🛑 Ditemukan Data Hilang (Missing Values)")
                nan_details = df.isnull().sum()
                nan_cols = nan_details[nan_details > 0]

                # Baris yang mengandung NA
                rows_with_nan = df[df.isnull().any(axis=1)].index.tolist()
                rows_display = [r + 1 for r in rows_with_nan]
                
                col_err1, col_err2 = st.columns([1, 2])
                
                with col_err1:
                    st.write("**Ringkasan Kolom Kosong:**")
                    st.dataframe(nan_cols.rename("Jumlah Kosong"), use_container_width=True)
                
                with col_err2:
                    st.write("**Lokasi Baris:**")
                    baris_teks = ", ".join(map(str, rows_display[:20]))
                    if len(rows_display) > 20:
                        baris_teks += " ... dan seterusnya."
                    
                    st.warning(f"Data kosong ditemukan pada baris: \n\n `{baris_teks}`")
                
                st.info("💡 **Saran:** Silakan lengkapi data yang kosong pada dataset Anda atau hapus baris tersebut sebelum upload ulang.")
                st.stop()
            
            # Cek Tipe Data 
            cols_to_check = [v for k, v in mapped_columns.items()]
            error_log = []
            for col in cols_to_check:
                converted = pd.to_numeric(df[col], errors='coerce')
                if converted.isnull().any():
                    invalid_rows = df[converted.isnull()].index.tolist()
                    invalid_values = df.loc[converted.isnull(), col].tolist()
                    error_log.append({
                        "Kolom": col, 
                        "Baris": [r + 1 for r in invalid_rows[:5]], 
                        "Nilai Salah": invalid_values[:5]
                    })

            if error_log:
                st.error("### ❌ Kesalahan Tipe Data (Bukan Angka)")
                st.dataframe(pd.DataFrame(error_log), use_container_width=True, hide_index=True)
                st.info("💡 **Saran:** Pastikan semua kolom parameter berisi angka numerik.")
                st.stop()


            st.success("✅ Data Valid")


            for col in cols_to_check:
                df[col] = pd.to_numeric(df[col])


            # Analisis Kesiapan Metode
            st.markdown("---")
            st.markdown("### Pengecekan Metode")

            essential_cols = ['magnitude', 'latitude', 'longitude']
            missing_essential = [k for k in essential_cols if k not in mapped_columns]
            is_gmpe_ready = len(missing_essential) == 0

            missing_hybrid = [k for k in column_aliases.keys() if k not in mapped_columns]
            is_hybrid_ready = is_gmpe_ready and (len(missing_hybrid) == 0)

            col_st1, col_st2 = st.columns(2)
            with col_st1:
                if is_gmpe_ready:
                    st.success("**Metode GMPE Dapat Digunakan**")
                else:
                    st.error("**Metode GMPE Tidak Dapat Digunakan**")
                    st.caption(f"Butuh kolom: {', '.join(missing_essential)}")

            with col_st2:
                if is_hybrid_ready:
                    st.success("**Metode Hibrida  Dapat Digunakan**")
                elif is_gmpe_ready:
                    st.warning("**Metode Hibrida Tidak Dapat Digunakan**")
                    st.caption(f"Lengkapi: {', '.join(missing_hybrid)}")
                else:
                    st.error("**Metode Hibrida Tidak Dapat Digunakan**")
                    st.caption("Syarat utama GMPE belum terpenuhi. Karena nilai PGA didapatkan dari metode GMPE ")

            # Penanganan VS30
            if is_gmpe_ready and 'vs30' not in mapped_columns:
                st.info("💡 **Catatan VS30:** Kolom VS30 tidak terdeteksi. Sistem akan mengaktifkan opsi **Asumsi Tipe Tanah (SNI 1726:2019)** pada tahap estimasi nanti.")

            # Preview & Button
            st.markdown("---")
            st.markdown("### Preview Dataset")
            st.dataframe(df.head(10), use_container_width=True)

            if is_gmpe_ready:
                if st.button("Lanjut ke Estimasi PGA", type="primary", use_container_width=True):
                    st.session_state['uploaded_data'] = df
                    st.session_state['mapped_columns'] = mapped_columns 
                    st.session_state.page = 'Estimasi PGA'
                    st.rerun()
            else:
                st.error("Data Tidak Valid")

        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {str(e)}")


