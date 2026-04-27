# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan hasil analisis mendalam terhadap dataset penyewaan sepeda (Bike Sharing). Fokus utama proyek ini adalah memahami tren pertumbuhan bisnis, pola perilaku pengguna berdasarkan waktu, serta pengaruh faktor lingkungan (suhu) terhadap volume penyewaan. Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan **Streamlit**.

## 📌 Pertanyaan Bisnis
1. **Tren Pertumbuhan:** Bagaimana perbandingan performa penyewaan tahun 2011 vs 2012 dan kapan lonjakan paling signifikan terjadi?
2. **Pola Aktivitas:** Bagaimana perbedaan pola aktivitas antara pengguna *Casual* dan *Registered* pada jam-jam sibuk (*rush hours*) di hari kerja?
3. **Analisis Lanjutan:** Bagaimana pengaruh pengelompokan suhu udara (*Temperature Binning*) terhadap total penyewaan sepeda?

## 📂 Struktur Folder
```text
.
├── dashboard/
│   ├── dashboard.py       # Kode utama aplikasi Streamlit
│   ├── df_day_clean.csv      # Dataset harian yang sudah dibersihkan
│   └── df_hour_clean.csv     # Dataset per jam yang sudah dibersihkan
├── data/
│   ├── day.csv            # Dataset asli harian
│   └── hour.csv           # Dataset asli per jam
├── notebook.ipynb         # File analisis (Wrangling, EDA, Visualization)
├── requirements.txt       # Daftar library yang diperlukan
└── README.md              # Dokumentasi proyek
└── url.txt                # Url dashboard streamlit cloud

Tentu, Andika. Ini adalah versi README.md yang paling lengkap dan terpadu. Saya sudah menyatukan semua bagian agar kamu bisa langsung copy-paste seluruh blok kode di bawah ini ke dalam file README.md kamu.

Markdown

# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan hasil analisis mendalam terhadap dataset penyewaan sepeda (Bike Sharing). Fokus utama proyek ini adalah memahami tren pertumbuhan bisnis, pola perilaku pengguna berdasarkan waktu, serta pengaruh faktor lingkungan (suhu) terhadap volume penyewaan. Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan **Streamlit**.

## 📌 Pertanyaan Bisnis
1. **Tren Pertumbuhan:** Bagaimana perbandingan performa penyewaan tahun 2011 vs 2012 dan kapan lonjakan paling signifikan terjadi?
2. **Pola Aktivitas:** Bagaimana perbedaan pola aktivitas antara pengguna *Casual* dan *Registered* pada jam-jam sibuk (*rush hours*) di hari kerja?
3. **Analisis Lanjutan:** Bagaimana pengaruh pengelompokan suhu udara (*Temperature Binning*) terhadap total penyewaan sepeda?

## 📂 Struktur Folder
```text
.
├── dashboard/
│   ├── dashboard.py       # Kode utama aplikasi Streamlit
│   ├── day_clean.csv      # Dataset harian yang sudah dibersihkan
│   └── hour_clean.csv     # Dataset per jam yang sudah dibersihkan
├── data/
│   ├── day.csv            # Dataset asli harian
│   └── hour.csv           # Dataset asli per jam
├── notebook.ipynb         # File analisis (Wrangling, EDA, Visualization)
├── requirements.txt       # Daftar library yang diperlukan
└── README.md              # Dokumentasi proyek

## 🛠️ Cara Menjalankan Dashboard
""
Ikuti langkah-langkah berikut untuk menjalankan dashboard di komputer lokal Anda:

1. Persiapan Lingkungan
Buka terminal atau Command Prompt dan masuk ke direktori proyek ini. Sangat disarankan untuk menggunakan Virtual Environment:
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

2. Instalasi Library
Instal semua library yang dibutuhkan dengan satu perintah:
pip install -r requirements.txt

3. Menjalankan Aplikasi
Jalankan dashboard dengan mengetik perintah berikut:
streamlit run dashboard/dashboard.py

