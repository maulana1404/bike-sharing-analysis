import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# --- 1. KONFIGURASI & SETUP ---
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- 2. DATA LOADING & CLEANING ---
path = os.path.dirname(__file__)
main_data_path = os.path.join(path, "main_data.csv")
df_day = pd.read_csv(main_data_path)

# Pastikan tipe data benar
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Mapping kategori (Sesuai tahap Cleaning Data)
df_day['season'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_day['weathersit'] = df_day['weathersit'].map({
    1: 'Clear', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'
})
df_day['workingday'] = df_day['workingday'].map({0: 'Holiday/Weekend', 1: 'Working Day'})

# --- 3. SIDEBAR (FILTERS) ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.markdown("### Filter Analisis")
    min_date, max_date = df_day["dteday"].min(), df_day["dteday"].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter data berdasarkan input
main_df = df_day[(df_day["dteday"] >= str(start_date)) & (df_day["dteday"] <= str(end_date))]

# --- 4. DASHBOARD HEADER ---
st.title('Bike Sharing Analysis Dashboard 🚲')
st.markdown("Menampilkan hasil analisis data penyewaan sepeda berdasarkan parameter lingkungan dan waktu.")

# --- 5. SECTION: EXPLORATORY DATA ANALYSIS (EDA) UMUM ---
# Reviewer ingin EDA umum sebagai fondasi sebelum masuk ke pertanyaan bisnis
st.header("A. Exploratory Data Analysis (EDA)")
col_metrics1, col_metrics2, col_metrics3 = st.columns(3)

with col_metrics1:
    st.metric("Total Penyewaan", value=f"{main_df.cnt.sum():,}")
with col_metrics2:
    st.metric("Rata-rata Harian", value=f"{round(main_df.cnt.mean()):,}")
with col_metrics3:
    st.metric("Max Penyewaan Harian", value=f"{main_df.cnt.max():,}")

with st.expander("Lihat Statistik Deskriptif Data"):
    st.write(main_df.describe(include="all"))

st.divider()

# --- 6. SECTION: VISUALIZATION & EXPLANATORY ANALYSIS ---
st.header("B. Analisis Pertanyaan Bisnis")

# Definisi Warna Standar (Color Significance)
dark_blue = "#1565C0"
light_blue = "#90CAF9"

# --- PERTANYAAN 1: MUSIM ---
st.subheader("Q1: Pengaruh Musim terhadap Rata-rata Penyewaan")
# Proses Agregasi (Terpisah dari plotting)
season_df = main_df.groupby("season").cnt.mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
colors_s = [dark_blue if v == season_df.cnt.max() else light_blue for v in season_df.cnt]
sns.barplot(x="season", y="cnt", data=season_df, palette=colors_s, ax=ax1)

# Decluttering
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.set_ylabel(None)
ax1.set_xlabel(None)
ax1.tick_params(axis='y', left=False, labelleft=False)

for p in ax1.patches:
    ax1.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                fontsize=11, fontweight='bold')

st.pyplot(fig1)
st.info("Insight: Musim **Fall** mencatatkan rata-rata penyewaan tertinggi dibandingkan musim lainnya.")

# --- PERTANYAAN 2: CUACA ---
st.subheader("Q2: Dampak Kondisi Cuaca terhadap Jumlah Pengguna")
# Proses Agregasi
weather_df = main_df.groupby("weathersit").cnt.mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
colors_w = [dark_blue if v == weather_df.cnt.max() else light_blue for v in weather_df.cnt]
sns.barplot(x="weathersit", y="cnt", data=weather_df, palette=colors_w, ax=ax2)

# Decluttering
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_ylabel(None)
ax2.set_xlabel(None)
ax2.tick_params(axis='y', left=False, labelleft=False)

for p in ax2.patches:
    ax2.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                fontsize=11, fontweight='bold')

st.pyplot(fig2)
st.info("Insight: Cuaca **Clear** sangat mendominasi penggunaan sepeda secara signifikan.")

# --- PERTANYAAN 3: HARI KERJA ---
st.subheader("Q3: Pola Penyewaan Hari Kerja vs Hari Libur")
# Proses Agregasi
day_df = main_df.groupby("workingday").cnt.mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(10, 5))
colors_d = [dark_blue if v == day_df.cnt.max() else light_blue for v in day_df.cnt]
sns.barplot(x="workingday", y="cnt", data=day_df, palette=colors_d, ax=ax3)

# Decluttering
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.set_ylabel(None)
ax3.set_xlabel(None)
ax3.tick_params(axis='y', left=False, labelleft=False)

for p in ax3.patches:
    ax3.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                fontsize=11, fontweight='bold')

st.pyplot(fig3)
st.info("Insight: Rata-rata penyewaan di **Working Day** sedikit lebih tinggi, menunjukkan fungsi sebagai moda komuter.")

st.divider()

# --- SECTION: KESIMPULAN & REKOMENDASI STRATEGIS ---
st.divider()
st.header("C. Kesimpulan & Rekomendasi Bisnis")

col_cons, col_recom = st.columns(2)

with col_cons:
    st.subheader("📌 Kesimpulan Utama")
    st.markdown("""
    1. **Dominasi Musim**: Musim **Fall** adalah periode emas dengan rata-rata harian tertinggi (**5.644 unit**).
    2. **Sensitivitas Cuaca**: Cuaca buruk (Hujan/Salju) menurunkan potensi penyewaan hingga **63%**.
    3. **Profil Pengguna**: Mayoritas pengguna adalah **Komuter** yang aktif pada hari kerja (rata-rata **4.585 unit**).
    """)

with col_recom:
    st.subheader("🚀 Action Items")
    
    with st.expander("Strategi Operasional (Maintenance)"):
        st.write("""
        Lakukan pemeliharaan armada besar-besaran pada musim **Spring**. 
        Ini adalah waktu dengan permintaan terendah (~2.600 unit), sehingga tidak akan mengganggu 
        operasional saat puncak permintaan di musim Fall tiba.
        """)
        
    with st.expander("Strategi Marketing (Weather-Based)"):
        st.write("""
        Implementasikan **Dynamic Pricing** atau diskon harian pada aplikasi 
        saat kondisi cuaca terdeteksi hujan ringan. Hal ini untuk menjaga minat pengguna 
        yang memiliki kebutuhan mendesak.
        """)

    with st.expander("Strategi Produk (Subscription)"):
        st.write("""
        Luncurkan paket **'Commuter Pass'** khusus hari kerja. Karena data menunjukkan 
        penggunaan tinggi di hari kerja, paket ini akan meningkatkan loyalitas pelanggan 
        tetap dan menjamin pendapatan harian yang stabil.
        """)

st.caption('Copyright © 2026 | Proyek Analisis Data - Andika Maulana Putra')