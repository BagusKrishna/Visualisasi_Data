import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --- Bagian Informasi Kelompok & Judul (Sama seperti sebelumnya) ---
st.markdown("""
<div style='text-align: left; font-size: 22px; font-weight: bold;'>
    Kelompok 5<br>
</div>
<div style='text-align: left; font-size: 18px; margin-top: 10px;'>
    <ul style="list-style-type: none; padding: 0;">
        <li>1301223169 - Andre Aditya Amann</li>
        <li>1301223129 - Yustinus Dwi Adyra</li>
        <li>1301223425 - Rangga Aldora Permadi</li>
        <li>1301223323 - Gusti Raka Ananto</li>
        <li>1301223088 - Gede Bagus Krishnanditya Merta</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style='text-align: justify; font-size: 22px; font-weight: bold;'>
    Visualisasi Data Perdagangan Makanan dan Minuman Pasifik (PFTD 2.1)
</div>
<div style='text-align: justify; font-size: 16px; margin-top: 10px;'>
Perdagangan makanan dan minuman adalah tulang punggung ketahanan pangan di kawasan Pasifik. <b>Pacific Food Trade Database (PFTD) versi 2.1</b>—yang menjadi dasar visualisasi ini—menangkap dinamika perdagangan di <b>18 Negara dan Wilayah Pasifik</b> dari <b>1995 hingga 2018</b>. Data ini diklasifikasikan menggunakan sistem <b>HS92</b> untuk memastikan konsistensi analisis.
</div>
<div style='text-align: justify; font-size: 16px; margin-top: 10px;'>
Dengan geografi yang terfragmentasi dan sumber daya terbatas, banyak negara Pasifik bergantung pada impor pangan. Visualisasi berikut tidak hanya menunjukkan pola perdagangan, tetapi juga membantu mengidentifikasi kerentanan dan peluang dalam ketahanan pangan dan nutrisi—tujuan utama dari PFTD.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

@st.cache_data
def load_data():
    """Memuat data dari URL dan melakukan pra-pemrosesan awal."""
    try:
        url = "https://drive.google.com/uc?export=download&id=1wuz1IEEQpngIbCtXPgMVev0aYeCd_aGH"
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"Gagal memuat data dari URL: {e}")
        st.warning("Menggunakan data dummy untuk melanjutkan.")
        dummy_data_dict = {
            'Importer': ['Fiji', 'Kiribati', 'Fiji', 'Vanuatu', 'Samoa', 'Fiji', 'Tuvalu', 'Nauru', 'Palau', 'Micronesia', 'Marshall Islands'],
            'Exporter': ['Australia', 'New Zealand', 'Australia', 'Fiji', 'New Zealand', 'Australia', 'USA', 'China', 'Japan', 'Korea', 'Thailand'],
            'COMMODITY': [1001, 2002, 20, 3003, 2002, 2204, 4001, 5002, 6003, 7004, 8005], 
            'Commodity': ['Sereal (Gandum)', 'Daging (Sapi)', 'Produk Susu', 'Ikan (Segar)', 'Daging (Sapi)', 'Minuman (Anggur)', 'Kopi', 'Teh', 'Rempah', 'Buah', 'Sayur'],
            'TIME_PERIOD': [1995, 1995, 1996, 1997, 1998, 1995, 1999, 2000, 2001, 2002, 2003],
            'OBS_VALUE': [100, 200, 150, 50, 250, 300, 120, 130, 140, 160, 170],
            'UNIT_MEASURE': ['Tonnes', 'Tonnes', 'Tonnes', 'Tonnes', 'Tonnes', 'Litres', 'Tonnes', 'Tonnes', 'Tonnes', 'Tonnes', 'Tonnes'],
            'INDICATOR': ['Import', 'Import', 'Import', 'Import', 'Import', 'Import', 'Import', 'Import', 'Import', 'Import', 'Import']
        }
        df = pd.DataFrame(dummy_data_dict)

    rename_map = {
        "Importer": "importer", "Exporter": "exporter",
        "COMMODITY": "commodity_code", "TIME_PERIOD": "year",
        "OBS_VALUE": "value", "UNIT_MEASURE": "unit", "INDICATOR": "indicator"
    }
    df = df.rename(columns=rename_map)
    
    df['commodity_code'] = df['commodity_code'].astype(str)

    expected_core_cols = ["importer", "exporter", "commodity_code", "year", "value", "unit", "indicator"]
    
    if 'Commodity' in df.columns:
        df = df[expected_core_cols + ['Commodity']]
    else:
        df = df[expected_core_cols]
        st.sidebar.warning("Kolom deskripsi 'Commodity' tidak ditemukan. Mapping nama komoditas mungkin tidak lengkap.")

    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['year', 'value'], inplace=True)
    df['year'] = df['year'].astype(int)

    return df

def clean_data(df, drop_na_flag=True, remove_outliers_flag=True):
    df_cleaned = df.copy()
    if drop_na_flag:
        cols_to_check = ["importer", "exporter", "commodity_code", "year", "value"]
        if 'Commodity' in df_cleaned.columns:
             cols_to_check.append('Commodity')
        df_cleaned = df_cleaned.dropna(subset=cols_to_check, how='any')
    
    if remove_outliers_flag and 'value' in df_cleaned.columns and not df_cleaned['value'].empty:
        Q1 = df_cleaned["value"].quantile(0.25)
        Q3 = df_cleaned["value"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_cleaned = df_cleaned[(df_cleaned["value"] >= lower_bound) & (df_cleaned["value"] <= upper_bound)]
    return df_cleaned

data_loaded = load_data()
data_for_filtering = data_loaded.copy()

st.sidebar.title("⚙️ Opsi Pembersihan Data")
drop_na = st.sidebar.checkbox("Hapus Baris dengan Data Kosong (NaN)", value=True)
remove_outliers = st.sidebar.checkbox("Hapus Outlier (berdasarkan 'value')", value=True)

cleaned_for_filters = clean_data(data_for_filtering, drop_na_flag=drop_na, remove_outliers_flag=remove_outliers)

st.sidebar.title("🎛️ Filter Data")

selected_year_range_tuple = (None, None)
if not cleaned_for_filters.empty and 'year' in cleaned_for_filters.columns and not cleaned_for_filters['year'].empty:
    min_year = int(cleaned_for_filters["year"].min())
    max_year = int(cleaned_for_filters["year"].max())
    if min_year == max_year:
        st.sidebar.caption(f"Data hanya tersedia untuk tahun: {min_year}")
        selected_year_range_tuple = (min_year, max_year)
    elif min_year < max_year:
        selected_year_range_tuple = st.sidebar.slider(
            "Pilih Rentang Tahun:", min_value=min_year, max_value=max_year, value=(min_year, max_year)
        )
else:
    st.sidebar.warning("Tidak ada data tahun setelah pembersihan awal.")

data_after_year_filter = pd.DataFrame()
if selected_year_range_tuple != (None, None) and not cleaned_for_filters.empty:
    data_after_year_filter = cleaned_for_filters[
        (cleaned_for_filters["year"] >= selected_year_range_tuple[0]) &
        (cleaned_for_filters["year"] <= selected_year_range_tuple[1])
    ]
elif not cleaned_for_filters.empty:
    data_after_year_filter = cleaned_for_filters

if not data_after_year_filter.empty:
    available_commodities = sorted(data_after_year_filter["commodity_code"].unique())
    available_importers = sorted(data_after_year_filter["importer"].unique())
    available_exporters = sorted(data_after_year_filter["exporter"].unique())
else:
    available_commodities, available_importers, available_exporters = [], [], []

selected_commodity_codes = st.sidebar.multiselect(
    "Pilih Kode Komoditas (HS92):", available_commodities, default=available_commodities
)
selected_importers_filter = st.sidebar.multiselect("Pilih Negara Importer (untuk filter global):", available_importers, default=[]) # Diganti nama agar tidak konflik
selected_exporters = st.sidebar.multiselect("Pilih Negara Eksportir:", available_exporters, default=[])

filtered_data = data_after_year_filter.copy()

if selected_commodity_codes:
    filtered_data = filtered_data[filtered_data["commodity_code"].isin(selected_commodity_codes)]
if selected_importers_filter: # Menggunakan variabel filter yang baru
    filtered_data = filtered_data[filtered_data["importer"].isin(selected_importers_filter)]
if selected_exporters:
    filtered_data = filtered_data[filtered_data["exporter"].isin(selected_exporters)]

if filtered_data.empty:
    st.warning("⚠️ Tidak ada data yang cocok dengan kriteria filter yang Anda pilih. Silakan ubah pilihan filter di sidebar.")
else:
    st.markdown("### 🧾 Ringkasan Data Terfilter")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Baris Data:", f"{len(filtered_data):,}")
    total_value_sum = filtered_data['value'].sum()
    units_present = filtered_data['unit'].unique()
    display_unit = units_present[0] if len(units_present) == 1 else "(beragam)"
    col2.metric("Total Volume Perdagangan:", f"{total_value_sum:,.0f} {display_unit}")
    min_year_display = filtered_data['year'].min()
    max_year_display = filtered_data['year'].max()
    year_range_display = f"{min_year_display} - {max_year_display}" if min_year_display != max_year_display else str(min_year_display)
    col3.metric("Rentang Tahun (Data):", year_range_display)
    st.markdown("---")

    if 'Commodity' in filtered_data.columns and 'commodity_code' in filtered_data.columns:
        st.markdown("### 📋 Mapping Kode ke Nama Komoditas")
        
        mapping_df_temp = filtered_data[['commodity_code', 'Commodity']].drop_duplicates()
        mapping_df_temp['commodity_code_numeric_for_sort'] = pd.to_numeric(mapping_df_temp['commodity_code'], errors='coerce')
        mapping_data_final = mapping_df_temp.sort_values(
            by='commodity_code_numeric_for_sort', 
            na_position='last'
        ).drop(columns=['commodity_code_numeric_for_sort'])
        
        st.dataframe(mapping_data_final, 
                    column_config={
                        "commodity_code": st.column_config.TextColumn("Kode Komoditas (HS92)"),
                        "Commodity": st.column_config.TextColumn("Nama Komoditas")
                    },
                    hide_index=True, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        Tabel ini memetakan kode HS92 ke nama komoditas makanan dan minuman yang diperdagangkan. Diurutkan berdasarkan Kode Komoditas.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.info("Informasi nama komoditas (kolom 'Commodity') tidak tersedia atau tidak ada data 'commodity_code' untuk mapping.")
        st.markdown("---")

    st.markdown("### 📦 Volume Perdagangan per Kode Komoditas")
    if not filtered_data.empty and 'commodity_code' in filtered_data.columns:
        fig1_data = filtered_data.groupby("commodity_code")["value"].sum().reset_index()
        fig1_data = fig1_data.sort_values(by="value", ascending=False)
        
        fig1 = px.bar(fig1_data,
                    x="commodity_code", y="value", color="commodity_code",
                    title="Total Volume per Kode Komoditas (HS92)",
                    labels={"commodity_code": "Kode Komoditas (HS92)", "value": "Total Volume Perdagangan"})
        fig1.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        Visualisasi ini mengungkap dominasi komoditas tertentu (berdasarkan kode HS92). Diurutkan berdasarkan total volume.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("### 📊 Tren Volume Perdagangan Tahunan")
    if not filtered_data.empty and 'year' in filtered_data.columns:
        fig2_data = filtered_data.groupby("year")["value"].sum().reset_index()
        fig2 = px.line(fig2_data, x="year", y="value", markers=True, title="Tren Total Volume per Tahun",
                    labels={"year": "Tahun", "value": "Total Volume Perdagangan"})
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        Tren perdagangan dari tahun ke tahun menunjukkan fluktuasi yang dapat dipengaruhi berbagai faktor.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    # Visualisasi Eksportir Terbesar (FIG3)
    st.markdown("### 🌍 Eksportir Terbesar")
    if not filtered_data.empty and 'exporter' in filtered_data.columns:
        top_exporters = filtered_data.groupby("exporter")["value"].sum().reset_index().sort_values(by="value", ascending=False).head(10)
        if not top_exporters.empty:
            fig3 = px.bar(top_exporters, x="exporter", y="value", color="exporter", title="Top 10 Eksportir berdasarkan Volume",
                        labels={"exporter": "Negara Eksportir", "value": "Total Volume Ekspor"})
            st.plotly_chart(fig3, use_container_width=True)
            # Narasi untuk Eksportir Terbesar
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            Grafik ini menunjukkan 10 negara eksportir teratas berdasarkan total volume perdagangan dalam data yang difilter. Informasi ini membantu mengidentifikasi pemain kunci dalam penyediaan pangan ke kawasan Pasifik.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Tidak ada data eksportir untuk ditampilkan berdasarkan filter saat ini.")
        st.markdown("---")

    # --- PENAMBAHAN VISUALISASI: IMPORTIR TERBESAR (FIG6) ---
    st.markdown("### 🚢 Importir Terbesar")
    if not filtered_data.empty and 'importer' in filtered_data.columns:
        top_importers = filtered_data.groupby("importer")["value"].sum().reset_index().sort_values(by="value", ascending=False).head(10)
        if not top_importers.empty:
            fig6 = px.bar(top_importers, x="importer", y="value", color="importer", # Menggunakan 'importer' untuk warna
                        title="Top 10 Importir berdasarkan Volume",
                        labels={"importer": "Negara Importir", "value": "Total Volume Impor"})
            st.plotly_chart(fig6, use_container_width=True)
            # Narasi untuk Importir Terbesar
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            Grafik ini menampilkan 10 negara importir teratas berdasarkan total volume perdagangan dalam data yang difilter. Ini menyoroti negara-negara di Pasifik yang memiliki ketergantungan impor pangan tertinggi.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Tidak ada data importir untuk ditampilkan berdasarkan filter saat ini.")
        st.markdown("---")
    # --- AKHIR PENAMBAHAN VISUALISASI ---


    st.markdown("### 📈 Distribusi Volume per Kode Komoditas")
    if not filtered_data.empty and 'commodity_code' in filtered_data.columns:
        fig4 = px.box(filtered_data, 
                    x="commodity_code", y="value", color="commodity_code",
                    title="Sebaran Volume per Kode Komoditas (HS92)",
                    labels={"commodity_code": "Kode Komoditas (HS92)", "value": "Volume Perdagangan"})
        
        if 'fig1_data' in locals() and not fig1_data.empty: 
             fig4.update_xaxes(categoryorder='array', categoryarray=fig1_data['commodity_code'].tolist())
        
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        Sebaran volume perdagangan per kode komoditas. Urutan pada sumbu-X mengikuti urutan pada chart volume perdagangan di atas.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("### 📉 Tren Volume per Importer")
    # Menggunakan selected_importers_filter karena selected_importers sudah digunakan untuk grafik tren
    if selected_importers_filter: # Cek apakah filter global untuk importer dipilih
        # Data untuk tren tetap menggunakan semua importer yang ada di filtered_data, 
        # namun hanya akan di-highlight jika ada di selected_importers_filter
        # Jika ingin tren hanya untuk yang difilter, maka gunakan filtered_data langsung
        
        # Ambil data yang sudah difilter berdasarkan selected_importers_filter untuk tren ini
        trend_data_for_selected_importers = filtered_data[filtered_data["importer"].isin(selected_importers_filter)]

        if not trend_data_for_selected_importers.empty and 'importer' in trend_data_for_selected_importers.columns and 'year' in trend_data_for_selected_importers.columns:
            fig5_data = trend_data_for_selected_importers.groupby(["year", "importer"])["value"].sum().reset_index()
            fig5 = px.line(fig5_data, x="year", y="value", color="importer", markers=True,
                        title="Tren Volume Tahunan per Importer (yang difilter di sidebar)",
                        labels={"year": "Tahun", "value": "Total Volume Impor", "importer": "Negara Importer"})
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            Tren impor per negara (yang dipilih pada filter global importer di sidebar) menunjukkan pola ketergantungan pangan yang unik.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("Tidak ada data tren untuk importer yang dipilih pada filter global di sidebar.")
    else:
        st.info("ℹ️ Pilih minimal satu negara *Importer* pada filter global di sidebar untuk melihat tren tahunan per importer.")
    st.markdown("---")

    with st.expander("📋 Tampilkan Data Mentah yang Telah Difilter"):
        st.dataframe(filtered_data, use_container_width=True)