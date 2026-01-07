import streamlit as st

def show():
    
    st.markdown("### 🎯 Tentang Aplikasi QuakeAceh")
    st.info("""
    **QuakeAceh** adalah aplikasi web yang dirancang untuk mengestimasi nilai **Peak Ground Acceleration (PGA)** 
    di wilayah Aceh dan sekitarnya. Aplikasi ini menggunakan dua pendekatan utama:
    
    1. **GMPE (Ground Motion Prediction Equation)** - Metode berbasis persamaan fisika menggunakan model Boore-Atkinson 2008
    2. **Hibrida (GMPE + Machine Learning)** - Kombinasi GMPE dengan model Neural Network untuk meningkatkan akurasi
    
    Aplikasi ini cocok digunakan untuk keperluan penelitian akademis, analisis risiko gempa, dan studi kelayakan infrastruktur.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PANDUAN STEP BY STEP
    st.markdown("## 📋 Langkah-Langkah Penggunaan Aplikasi")
    
    # ========== STEP 1 ==========
    with st.expander("**LANGKAH 1: Melihat Informasi Aplikasi di Halaman Beranda** 🏠", expanded=True):
        st.markdown("### Memahami Aplikasi QuakeAceh")
        
        st.markdown("""
        Ketika pertama kali membuka aplikasi, Anda akan diarahkan ke **Halaman Beranda**. 
        Di halaman ini, Anda dapat melihat:
        """)
        
        st.markdown("#### 🔹 Peta Wilayah Studi")
        st.markdown("""
        - **Peta interaktif** yang menampilkan fokus wilayah Aceh dan sekitarnya
        - Area studi ditandai dengan **lingkaran merah** yang mencakup wilayah estimasi PGA
        - Terdapat **marker lokasi** untuk kota-kota penting seperti Banda Aceh, Lhokseumawe, Sabang, dan Meulaboh
        - Anda dapat **menggeser** (pan) dan **memperbesar** (zoom) peta untuk melihat detail wilayah
        - Klik pada marker untuk melihat informasi lebih lanjut tentang lokasi tersebut
        """)
        
        st.markdown("#### 🔹 Penjelasan Sistem")
        st.markdown("""
        - **Deskripsi singkat** tentang fungsi aplikasi QuakeAceh
        - **Penjelasan PGA** (Peak Ground Acceleration) - klik untuk membaca definisi lengkap:
          - Apa itu PGA dan mengapa penting
          - Satuan yang digunakan (g dan cm/s²)
          - Kegunaannya dalam desain bangunan tahan gempa
        - **Penjelasan Metode** yang digunakan dalam aplikasi ini
        """)
        
        st.markdown("#### 🔹 Memulai Aplikasi")
        st.markdown("""
        Setelah memahami informasi di halaman beranda, klik tombol **"🚀 MULAI SEKARANG"** 
        yang terletak di bagian bawah halaman untuk melanjutkan ke tahap input data.
        """)
    
    # ========== STEP 2 ==========
    with st.expander("**LANGKAH 2: Input Data Gempa dan Validasi** 📊"):
        st.markdown("### Mengunggah Dataset Gempa")
        
        st.markdown("""
        Setelah mengklik tombol "MULAI SEKARANG", Anda akan diarahkan ke **Halaman Data**. 
        Di halaman ini, Anda akan melakukan input dan validasi data gempa.
        """)
        
        st.markdown("#### Persiapan File Data")
        st.markdown("""
        Sebelum mengunggah, pastikan file data Anda memenuhi kriteria berikut:
        
        **Format File yang Didukung:**
        - File **CSV** (.csv)
        - File **Microsoft Excel** (.xlsx atau .xls)
        
        **Kolom-Kolom yang Diperlukan:**
        
        Aplikasi ini mendukung dua metode perhitungan dengan persyaratan data yang berbeda:
        """)
        
        # Tabel Metode GMPE
        st.markdown("**A. Untuk Metode GMPE (Minimal):**")
        st.markdown("""
        | Nama Kolom | Variasi Nama yang Diterima | Penjelasan | Contoh Nilai |
        |------------|---------------------------|------------|--------------|
        | Magnitude | magnitude, mag, m, mw | Magnitudo gempa (skala Mw) | 5.5, 6.2, 7.0 |
        | Latitude | latitude, lat, lintang | Lintang pusat gempa | 5.5483, 4.1234 |
        | Longitude | longitude, lon, long, bujur | Bujur pusat gempa | 95.3238, 96.4567 |
        | VS30 | vs30, v_s30 | Kecepatan gelombang geser (opsional) | 760, 300, 180 |
        
        **Catatan:** Jika kolom VS30 tidak tersedia, sistem akan memberikan opsi untuk memilih tipe tanah 
        berdasarkan standar SNI 1726:2019 pada tahap estimasi.
        """)
        
        # Tabel Metode Hibrida
        st.markdown("**B. Untuk Metode Hibrida (GMPE + Machine Learning):**")
        st.markdown("""
        Selain kolom di atas, diperlukan kolom tambahan berikut:
        
        | Nama Kolom | Variasi Nama yang Diterima | Penjelasan | Contoh Nilai |
        |------------|---------------------------|------------|--------------|
        | Depth | depth, kedalaman, d | Kedalaman gempa (km) | 10.0, 25.5, 150.2 |
        | NST | nst, number_of_stations | Jumlah stasiun pencatat lokasi | 15, 25, 48 |
        | Gap | gap, azimuthal_gap | Celah azimuth antar stasiun (°) | 45, 120, 180 |
        | RMS | rms, root_mean_square | Residual waktu tempuh gelombang | 0.15, 0.25, 0.50 |
        | MagNST | magnst, mag_nst | Jumlah stasiun pencatat magnitudo | 10, 20, 35 |
        | DepthError | deptherror, depth_error | Error estimasi kedalaman (km) | 1.5, 3.2, 5.0 |
        
        **Catatan:** Sistem akan otomatis mendeteksi variasi nama kolom, sehingga Anda tidak perlu 
        khawatir tentang format penulisan nama kolom (huruf besar/kecil).
        """)
        
        st.markdown("#### Cara Mengunggah File")
        st.markdown("""
        1. Klik tombol **"Browse files"** atau **"Pilih file dataset"**
        2. Pilih file CSV atau Excel dari komputer Anda
        3. Tunggu hingga proses upload selesai (ditandai dengan pesan sukses ✅)
        4. File Anda akan langsung divalidasi oleh sistem
        """)
        
        st.markdown("#### Proses Validasi Data")
        st.markdown("""
        Setelah file berhasil diunggah, sistem akan melakukan **validasi otomatis** dengan tahapan:
        
        **1. Pengecekan Data Hilang (Missing Values)**
        - Sistem akan memeriksa apakah ada sel kosong atau nilai yang hilang
        - Jika ditemukan data hilang:
          - Sistem akan menampilkan **kolom mana** yang bermasalah
          - Sistem akan menunjukkan **nomor baris** yang mengandung data kosong
          - Anda perlu memperbaiki file dan mengunggah ulang
        
        **2. Validasi Tipe Data**
        - Sistem memastikan semua nilai dalam kolom numerik adalah **angka**, bukan teks
        - Jika ditemukan kesalahan:
          - Sistem akan menampilkan lokasi kesalahan (kolom dan baris)
          - Sistem akan menunjukkan nilai yang salah
          - Anda perlu memperbaiki file dan mengunggah ulang
        
        **3. Pengecekan Kesesuaian Metode**
        - Sistem akan menentukan metode mana yang dapat digunakan berdasarkan kelengkapan data:
          - ✅ **Metode GMPE Dapat Digunakan** - jika kolom Magnitude, Latitude, Longitude tersedia
          - ✅ **Metode Hibrida Dapat Digunakan** - jika semua kolom lengkap tersedia
          - ⚠️ **Metode Tidak Dapat Digunakan** - jika ada kolom wajib yang kurang
        """)
        
        st.warning("""
        **⚠️ Tips Penting untuk Menghindari Kesalahan:**
        
        - Pastikan semua nilai numerik menggunakan **titik (.)** sebagai pemisah desimal, bukan koma (,)
          - ✅ Benar: 5.5, 6.2, 95.3238
          - ❌ Salah: 5,5 atau 6,2 atau 95,3238
        - Jangan ada sel yang kosong atau bernilai NULL
        - Pastikan tidak ada karakter khusus dalam angka (seperti: 5.5m, 6km, dll)
        - Format koordinat harus dalam **desimal** (bukan derajat-menit-detik)
        """)
        
        st.markdown("#### 🔹 Preview Data")
        st.markdown("""
        Setelah validasi berhasil, sistem akan menampilkan:
        - **Ringkasan Dataset:** Total baris, total kolom, dan jumlah kolom yang terdeteksi
        - **Preview Tabel:** 10 baris pertama dari dataset Anda
        - **Tombol Lanjut:** Untuk melanjutkan ke tahap estimasi PGA
        """)
        
        st.markdown("#### 🔹 Melanjutkan ke Tahap Estimasi")
        st.markdown("""
        Jika data Anda sudah valid dan minimal metode GMPE dapat digunakan, 
        klik tombol **"➡️ Lanjut ke Estimasi PGA"** untuk melanjutkan ke langkah berikutnya.
        """)
    
    # ========== STEP 3 ==========
    with st.expander("**LANGKAH 3: Input Lokasi Target untuk Estimasi PGA** 📍"):
        st.markdown("### Menentukan Koordinat Lokasi Target")
        
        st.markdown("""
        Setelah data gempa berhasil divalidasi, Anda akan masuk ke **Halaman Estimasi PGA**. 
        Di halaman ini, Anda perlu menentukan lokasi di mana nilai PGA akan dihitung.
        """)
        
        st.markdown("#### 🔹 Input Koordinat Lokasi Target")
        st.markdown("""
        Sistem menyediakan form untuk memasukkan koordinat geografis lokasi target:
        
        **A. Latitude (Lintang)**
        - Masukkan nilai lintang lokasi target
        - Contoh untuk wilayah Aceh: 5.5483, 4.1234, 5.7890
        - **Format:** Gunakan **titik (.)** sebagai pemisah desimal
          - ✅ Contoh benar: 5.5483
          - ❌ Contoh salah: 5,5483 (jangan gunakan koma!)
        
        **B. Longitude (Bujur)**
        - Masukkan nilai bujur lokasi target
        - Contoh untuk wilayah Aceh: 95.3238, 96.4567, 95.1234
        - **Format:** Gunakan **titik (.)** sebagai pemisah desimal
          - ✅ Contoh benar: 95.3238
          - ❌ Contoh salah: 95,3238 (jangan gunakan koma!)
        """)
        
        st.error("""
        **🚨 PENTING - Format Koordinat:**
        
        Sistem **HANYA menerima titik (.)** sebagai pemisah desimal, **BUKAN koma (,)**
        
        Jika Anda menggunakan koma, sistem akan menampilkan error atau hasil perhitungan 
        akan tidak akurat. Pastikan selalu menggunakan titik untuk nilai desimal!
        """)
        
        st.markdown("#### 🔹 Pengaturan VS30 (Jika Tidak Ada dalam Dataset)")
        st.markdown("""
        Jika dataset Anda tidak memiliki kolom VS30, sistem akan menampilkan opsi untuk 
        memilih **Kelas Situs** berdasarkan standar SNI 1726:2019.
        
        **Pilihan Kelas Situs:**
        
        | Kelas | VS30 (m/s) | Jenis Tanah |
        |-------|------------|-------------|
        | **SA** | 1300 | Batuan keras 
        | **SB** | 760 | Batuan sedang 
        | **SC** | 520 | Tanah keras, sangat padat 
        | **SD** | 250 | Tanah sedang 
        | **SE** | 180 | Tanah lunak 
        
        **Rekomendasi Pemilihan:**
        - Untuk **kota besar** (Banda Aceh, Lhokseumawe): Pilih **SD** atau **SE**
        - Untuk **area pegunungan**: Pilih **SB** atau **SC**
        - Untuk **pantai/pesisir**: Pilih **SE**
        - Jika **tidak yakin**: Gunakan **SD** sebagai pilihan konservatif
        """)
        
        st.markdown("#### 🔹 Pemilihan Metode Perhitungan")
        st.markdown("""
        Berdasarkan kelengkapan data yang Anda upload, sistem akan menampilkan metode yang tersedia:
        
        **1. Metode GMPE**
        - Menggunakan persamaan Boore-Atkinson 2008
        - Memerlukan: Magnitude, Latitude, Longitude, dan VS30
        - Cocok untuk estimasi cepat dengan data minimal
        
        **2. Metode Hibrida (GMPE + Machine Learning)**
        - Menggabungkan GMPE dengan model Neural Network
        - Memerlukan: Semua kolom lengkap (termasuk NST, Gap, RMS, dll)
        - Memberikan akurasi lebih tinggi karena mempertimbangkan kualitas data seismik
        - **Direkomendasikan** jika data Anda lengkap
        """)
        
        st.markdown("#### 🔹 Menjalankan Estimasi")
        st.markdown("""
        Setelah semua parameter diisi dengan benar:
        
        1. Periksa kembali nilai Latitude dan Longitude (pastikan menggunakan **titik**, bukan koma)
        2. Pastikan kelas situs VS30 sudah dipilih (jika diperlukan)
        3. Pilih metode perhitungan yang diinginkan
        4. Klik tombol **"Hitung PGA"** atau **"Estimasi PGA"**
        5. Tunggu proses perhitungan selesai (biasanya memerlukan beberapa detik hingga beberapa menit tergantung ukuran dataset)
        """)
    
    
    # ========== STEP 4 ==========
    with st.expander("**LANGKAH 4: Melihat Hasil dan Visualisasi** 📈"):
        st.markdown("### Memahami Output Estimasi PGA")
        
        st.markdown("""
        Setelah proses estimasi selesai, sistem akan menampilkan hasil perhitungan dalam bentuk 
        **tabel data** dan **visualisasi grafik**.
        """)
        
        st.markdown("#### 🔹 Hasil Estimasi GMPE")
        st.markdown("""
        Jika Anda menggunakan metode GMPE, sistem akan menampilkan kolom-kolom berikut dalam hasil:
        
        - **Data asli** dari dataset Anda (Magnitude, Latitude, Longitude, dll)
        - **distance_km**: Jarak horizontal dari epicenter gempa ke lokasi target (dalam kilometer)
        - **PGA_GMPE**: Nilai PGA hasil perhitungan GMPE dalam satuan **g** (gravitasi)
        
        """)
        
        st.markdown("#### 🔹 Hasil Estimasi Hibrida (GMPE + Machine Learning)")
        st.markdown("""
        Jika Anda menggunakan metode Hibrida, selain kolom-kolom GMPE di atas, 
        sistem akan menambahkan kolom:
        
        - **PGA_MLP**: Nilai PGA hasil prediksi model Neural Network dalam satuan **g**
        
        **Perbedaan GMPE dan MLP:**
        - **GMPE** menggunakan parameter fisika standar (Magnitude, Jarak, VS30)
        - **MLP** (Machine Learning) mempertimbangkan kualitas data seismik tambahan (NST, Gap, RMS, dll)
        - **MLP** dapat memberikan informasi tambahan terhadap nilai PGA yang telah dihasilkan oleh GMPE
        """)
        
        st.markdown("#### 🔹 Metrik Evaluasi Model (untuk Metode Hibrida)")
        st.markdown("""
        Untuk metode Hibrida, sistem akan menampilkan metrik evaluasi performa model:
        
        **1. MAE (Mean Absolute Error)**
        - Rata-rata kesalahan absolut dari prediksi
        - Satuan: sama dengan PGA (g atau cm/s²)
        - **Interpretasi:** Semakin kecil nilai MAE, semakin akurat model

        
        **2. RMSE (Root Mean Squared Error)**
        - Akar dari rata-rata kuadrat kesalahan
        - Lebih sensitif terhadap kesalahan besar (outlier)
        - **Interpretasi:** Semakin kecil nilai RMSE, semakin baik model

        
        **3. R² (Coefficient of Determination)**
        - Mengukur seberapa baik model menjelaskan variasi data
        - Rentang nilai: 0 hingga 1
        - **Interpretasi:** 
          - R² mendekati 1 = model sangat baik
          - R² = 0.85 berarti model menjelaskan 85% variasi data
          - R² < 0.5 = model kurang akurat
        
        """)
        
        st.markdown("#### 🔹 Visualisasi Grafik")
        st.markdown("""
        Sistem menyediakan beberapa jenis visualisasi untuk membantu Anda memahami hasil:
        
        **1. Grafik Scatter Plot (Prediksi vs Aktual)**
        - Menampilkan perbandingan antara nilai prediksi dan nilai aktual (jika tersedia)
        - **Interpretasi:** 
          - Titik yang dekat dengan garis diagonal = prediksi akurat
          - Titik yang tersebar jauh = model kurang fit
        
        **2. Grafik Distribusi PGA**
        - Menampilkan distribusi nilai PGA dari dataset
        - Membantu mengidentifikasi pola dan sebaran nilai PGA
        
        **3. Grafik Perbandingan GMPE vs MLP** (untuk Metode Hibrida)
        - Membandingkan hasil dari kedua metode
        - Membantu melihat perbedaan dan konsistensi antara GMPE dan ML
        """)
        
        st.markdown("#### 🔹 Download Hasil Estimasi")
        st.markdown("""
        Setelah melihat hasil dan visualisasi, Anda dapat mengunduh hasil estimasi dalam format:
        
        **Format yang Tersedia:**
        1. **CSV** - Format ringan, mudah dibuka di berbagai software (Excel, Python, R)
        2. **Excel** - Format dengan tampilan lebih rapi, cocok untuk laporan
        
        **Isi File Download:**
        - Semua kolom dari dataset asli Anda
        - Kolom jarak (distance_km)
        - Kolom hasil estimasi PGA (GMPE dan/atau MLP)
        - Metadata perhitungan (timestamp, parameter yang digunakan)
        
        **Cara Download:**
        1. Scroll ke bagian bawah halaman hasil
        2. Cari tombol **"Download Hasil"**
        3. Pilih format yang diinginkan (CSV atau Excel)
        4. Klik tombol download
        5. File akan tersimpan di folder Downloads browser Anda
        """)
    
    st.markdown("---")
    