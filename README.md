# Pacific Food and Beverage Trade Data Visualization (PFTD 2.1)

# Latar Belakang Proyek
Proyek ini ditujukan untuk pemenuhan tugas besar matakuliah Visualisasi Data, S1 Informatika, Telkom University. Dalam pengerjaan tugas ini saya berkolaborasi dengan kelompok saya, yaitu : 

- 1301223088 - Gede Bagus Krishnanditya Merta  
- 1301223169 - Andre Aditya Amann  
- 1301223129 - Yustinus Dwi Adyra  
- 1301223425 - Rangga Aldora Permadi  
- 1301223323 - Gusti Raka Ananto  

# Tentang Proyek 
**Pacific Food and Beverage Trade Data Visualization (PFTD 2.1)**  
Aplikasi Streamlit ini memvisualisasikan data perdagangan makanan & minuman di 18 negara/wilayah Pasifik (1995-2018) menggunakan data PFTD 2.1 (HS92). Tujuannya untuk mengidentifikasi pola perdagangan, ketergantungan, tren, dan wawasan untuk keamanan pangan regional.

dataset download : https://drive.google.com/uc?export=download&id=1wuz1IEEQpngIbCtXPgMVev0aYeCd_aGH

### Fitur:
- Informasi Kelompok & Deskripsi Proyek  
- Opsi Pembersihan & Filter Data (Tahun, Komoditas, Importir, Eksportir)  
- Ringkasan Data Terfilter  
- Tabel Pemetaan Kode Komoditas (HS92)  

### Visualisasi Interaktif:
- Volume Perdagangan per Komoditas & Tren Tahunan  
- Importir & Eksportir Terbesar  
- Distribusi Volume per Komoditas  
- Tren Volume per Importir (filter khusus)  
- Tampilan Data Mentah  

## 📌 Kesimpulan & Insight
Dari visualisasi ini, kami memperoleh beberapa insight penting, antara lain:
- Negara-negara Pasifik menunjukkan tren perdagangan yang dinamis terhadap komoditas pangan tertentu, khususnya beras, gula, dan produk susu.
- Beberapa negara sangat bergantung pada satu atau dua eksportir utama, menunjukkan risiko dalam ketahanan pasokan pangan.
- Volume impor cenderung meningkat dari tahun ke tahun, mencerminkan peningkatan kebutuhan pangan seiring pertumbuhan penduduk dan ekonomi.
- Visualisasi interaktif membantu mempermudah pemahaman terhadap kompleksitas data dan memberikan gambaran makro terhadap situasi perdagangan pangan di kawasan ini.

## 📁 Struktur Folder

Visualisasi_Data/
├── Pacific food and beverage trade_...csv # Dataset utama (PFTD 2.1)
├── README.md # Dokumentasi proyek
├── requirements.txt # Daftar dependensi Python
└── visdat.py # Script utama Streamlit

## 🧰 Instalasi & Menjalankan Aplikasi

1. **Clone repository**  
   ```bash
   git clone https://github.com/BagusKrishna/Visualisasi_Data.git
   cd Visualisasi_Data

2. **Install dependensi**  
   ```bash
   pip install -r requirements.txt

3. **Jalankan aplikasi Streamlit**  
   ```bash
   streamlit run visdat.py