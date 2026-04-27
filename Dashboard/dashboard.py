import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    day_df = pd.read_csv("df_day_clean.csv")
    hour_df = pd.read_csv("df_hour_clean.csv")
    
    # Memastikan format tanggal
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    # Mengatasi KeyError temp_bins jika tidak ada di CSV
    if 'temp_bins' not in day_df.columns:
        bins = [0, 0.4, 0.7, 1]
        labels = ['Cold', 'Moderate', 'Hot']
        day_df['temp_bins'] = pd.cut(day_df['temp'], bins=bins, labels=labels)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filter Data")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

try:
    start_date, end_date = st.sidebar.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except ValueError:
    start_date, end_date = min_date, max_date

# Filter data berdasarkan tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# --- MAIN PAGE ---
st.title("🚲 Bike Sharing Data Dashboard")
st.markdown("Dashboard ini menampilkan analisis performa penyewaan sepeda berdasarkan tren waktu, perilaku pengguna, dan kondisi lingkungan.")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df["cnt"].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    total_registered = main_df["registered"].sum()
    st.metric("Pengguna Terdaftar", value=f"{total_registered:,}")
with col3:
    total_casual = main_df["casual"].sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

st.divider()

# --- PERTANYAAN 1: TREN PERBANDINGAN TAHUNAN ---
st.subheader("1. Perbandingan Total Penyewaan Sepeda Per Bulan (2011 vs 2012)")

# Persiapan Data
monthly_trend_df = main_df.groupby(by=["yr", "mnth"], observed=True).agg({"cnt": "sum"}).reset_index()
monthly_trend_df['yr'] = monthly_trend_df['yr'].astype(str).replace({'0': '2011', '1': '2012', '0.0': '2011', '1.0': '2012'})
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_trend_df['mnth'] = pd.Categorical(monthly_trend_df['mnth'], categories=month_order, ordered=True)
monthly_trend_df = monthly_trend_df.sort_values(['yr', 'mnth'])

# Visualisasi
fig1, ax1 = plt.subplots(figsize=(20, 10)) 
colors1 = {'2011': '#2471A3', '2012': '#E67E22'}
sns.barplot(data=monthly_trend_df, x='mnth', y='cnt', hue='yr', palette=colors1, ax=ax1)

for container in ax1.containers:
    ax1.bar_label(container, fmt='{:,.0f}', padding=3, fontsize=10, fontweight='bold', rotation=45)   

ax1.set_title('Perbandingan Total Penyewaan Sepeda Per Bulan (2011 vs 2012)', fontsize=22, pad=30)
ax1.set_ylabel('Total Penyewaan', fontsize=14)
ax1.set_xlabel(None)
ax1.set_ylim(0, monthly_trend_df['cnt'].max() * 1.15)
ax1.legend(title='Tahun', loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
sns.despine()
st.pyplot(fig1)

# Insight 1
with st.expander("Lihat Insight Data Selama Rentang Waktu 01-01-2011 sampai 31-12-2012"):
    st.markdown("""
    - Sepanjang tahun **2012 (batang oranye)**, jumlah penyewaan menunjukkan tren pertumbuhan yang sangat positif sejak awal tahun. Dimulai dari 96.744 pada bulan Januari, volume penyewaan terus meningkat hingga melampaui angka 200.000 di bulan Juni dan mencapai puncaknya di bulan September. Setelah itu, volume mulai melandai pada kuartal terakhir tahun 2012.
    - Tahun 2012 menunjukkan performa yang secara konsisten jauh lebih tinggi dibandingkan tahun **2011 (batang biru)**. Tidak ada satu bulan pun di tahun 2012 yang jumlah penyewaannya lebih rendah daripada bulan yang sama di tahun sebelumnya.
    - **Lonjakan paling mencolok** dibandingkan tahun sebelumnya terlihat pada bulan **September 2012**. Pada bulan ini, jumlah penyewaan mencapai angka tertinggi sepanjang periode, yaitu 218.573, yang berarti terdapat selisih sebesar 91.155 penyewaan dibandingkan dengan bulan September 2011 (127.418).
    - Selain September, bulan **Maret** juga menunjukkan lonjakan pertumbuhan yang luar biasa. Jumlah penyewaan meningkat drastis dari 64.045 di tahun 2011 menjadi 164.875 di tahun 2012, yang mengindikasikan pertumbuhan volume lebih dari dua kali lipat.
    """)

st.divider()

# --- PERTANYAAN 2: POLA AKTIVITAS JAM SIBUK ---
st.subheader("2. Pola Aktivitas Pengguna pada Jam Sibuk di Hari Kerja")

working_day_hour = hour_df[(hour_df["workingday"] == "Working Day") & 
                           (hour_df["dteday"] >= str(start_date)) & 
                           (hour_df["dteday"] <= str(end_date))]
hourly_pattern = working_day_hour.groupby("hr").agg({"casual": "mean", "registered": "mean"}).reset_index()

fig2, ax2 = plt.subplots(figsize=(15, 7))
sns.lineplot(data=hourly_pattern, x='hr', y='registered', label='Registered', marker='o', linewidth=3, color='#2471A3', ax=ax2)
sns.lineplot(data=hourly_pattern, x='hr', y='casual', label='Casual', marker='o', linewidth=3, color='#E67E22', ax=ax2)

ax2.axvspan(7, 9, color='gray', alpha=0.15, label='Rush Hour Pagi')
ax2.axvspan(17, 19, color='gray', alpha=0.15, label='Rush Hour Sore')
ax2.set_xticks(range(0, 24))
ax2.set_ylabel("Rata-rata Jumlah Penyewaan")
ax2.set_xlabel("Jam (24 Jam)")
ax2.grid(axis='both', linestyle='--', alpha=0.3)
ax2.legend(title='Tipe Pengguna')
sns.despine()
st.pyplot(fig2)

# Insight 2
with st.expander("Lihat Insight Data Selama Rentang Waktu 01-01-2011 sampai 31-12-2012"):
    st.markdown("""
    - **Garis biru (Registered)** menunjukkan pola "Double Peak" yang sangat tajam. Lonjakan penyewaan terjadi tepat di dalam kotak abu-abu (pukul 08:00 dan 17:00). Ini membuktikan bahwa pengguna terdaftar adalah pekerja atau pelajar yang menggunakan sepeda sebagai alat transportasi rutin untuk berkomuter.
    - **Garis oranye (Casual)** memiliki tren yang jauh lebih landai. Tidak ada lonjakan drastis di jam 8 pagi. Aktivitas mereka justru meningkat perlahan saat hari mulai siang dan mencapai puncaknya di sore hari (sekitar jam 17:00). Ini mengindikasikan penggunaan untuk tujuan rekreasi atau kebutuhan non-rutin.
    - **Perbedaan volume yang sangat besar**: Pengguna Registered mendominasi total penyewaan di setiap jamnya, terutama saat jam sibuk di mana perbandingannya bisa mencapai lebih dari 8 kali lipat dibandingkan pengguna Casual.
    - **Aktivitas di Luar Jam Sibuk**: Di antara dua jam sibuk (sekitar pukul 10:00 - 15:00), jumlah pengguna Registered menurun drastis namun tetap stabil di angka tertentu. Hal ini menunjukkan adanya kelompok pengguna rutin yang tetap menggunakan sepeda di luar jam berangkat/pulang kantor.
    - **Highlight Area (Kotak Abu-abu)**: Merupakan penanda Jam Sibuk (*Rush Hours*) pada hari kerja (Pagi 07:00-09:00 & Sore 17:00-19:00). Area ini mempermudah pembaca melihat bahwa lonjakan data terjadi tepat di dalam jendela waktu tersebut.
    """)

st.divider()

# --- PERTANYAAN 3: ANALISIS SUHU ---
st.subheader("3. Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu")

temp_bin_df = main_df.groupby("temp_bins", observed=True).agg({"cnt": "mean"}).reset_index()

fig3, ax3 = plt.subplots(figsize=(12, 7))
sns.barplot(data=temp_bin_df, x='temp_bins', y='cnt', palette=['#AED6F1', '#F7DC6F', '#E67E22'], hue='temp_bins', legend=False, ax=ax3)

for container in ax3.containers:
    ax3.bar_label(container, fmt='{:,.0f}', padding=3, fontsize=12, fontweight='bold')

ax3.set_ylabel("Rata-rata Jumlah Penyewaan")
ax3.set_xlabel("Kategori Suhu")
ax3.set_ylim(0, temp_bin_df['cnt'].max() * 1.15)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
sns.despine()
st.pyplot(fig3)

# Insight 3
with st.expander("Lihat Insight Data Selama Rentang Waktu 01-01-2011 sampai 31-12-2012"):
    st.markdown("""
    - **Pengguna cenderung paling aktif bersepeda pada kategori suhu Hot, dengan rata-rata penyewaan mencapai angka tertinggi sebesar 5.664. Hal ini menunjukkan bahwa cuaca yang cenderung panas/hangat bukanlah penghalang, melainkan pendorong utama orang untuk beraktivitas di luar ruangan menggunakan sepeda.
    - **Terdapat tren kenaikan yang konsisten seiring dengan meningkatnya suhu udara. Dari suhu Cold (2.966) ke Moderate (5.244), terjadi lonjakan penggunaan yang cukup tinggi. Ini membuktikan bahwa suhu udara adalah variabel krusial yang menentukan volume bisnis.
    - **Kategori Cold memiliki angka penyewaan paling rendah (2.966). Ini menunjukkan bahwa pengguna memiliki resistansi yang tinggi untuk bersepeda saat suhu udara menurun drastis, kemungkinan karena faktor kenyamanan fisik atau risiko cuaca yang menyertainya.
    - **Perbedaan antara kategori Moderate (5,244) dan Hot (5,664) tidak terlalu ekstrem dibandingkan selisih dari kategori Cold. Ini mengindikasikan bahwa selama suhu berada di level yang "tidak dingin", minat pengguna tetap terjaga di level yang tinggi.
    - ** Berdasarkan data ini, perusahaan dapat mengoptimalkan jadwal pemeliharaan sepeda (maintenance) pada periode suhu Cold karena beban penggunaan sedang rendah, dan memastikan ketersediaan sepeda maksimal pada hari-hari dengan prakiraan cuaca Moderate hingga Hot.
    """)