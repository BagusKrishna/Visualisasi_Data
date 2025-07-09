import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --- Bagian Informasi Kelompok & Judul (Sama seperti sebelumnya) ---
st.markdown("""
<div style='text-align: left; font-size: 22px; font-weight: bold;'>
    Group 5<br>
</div>
<div style='text-align: left; font-size: 18px; margin-top: 10px;'>
    <ul style="list-style-type: none; padding: 0;">
        <li>1301223088 - Gede Bagus Krishnanditya Merta</li>
        <li>1301223169 - Andre Aditya Amann</li>
        <li>1301223129 - Yustinus Dwi Adyra</li>
        <li>1301223425 - Rangga Aldora Permadi</li>
        <li>1301223323 - Gusti Raka Ananto</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style='text-align: justify; font-size: 22px; font-weight: bold;'>
    Pacific Food and Beverage Trade Data Visualization (PFTD 2.1)
</div>
<div style='text-align: justify; font-size: 16px; margin-top: 10px;'>
Food and beverage trade is the backbone of food security in the Pacific region. <b>Pacific Food Trade Database (PFTD) version 2.1</b> -on which this visualization is based- captures the dynamics of trade in<b> 18 Pacific Countries and Regions</b> from <b>1995 to 2018</b>. This data was classified using the <b>HS92</b> system to ensure consistency of analysis.
</div>
<div style='text-align: justify; font-size: 16px; margin-top: 10px;'>
With fragmented geographies and limited resources, many Pacific countries rely on food imports. The following visualization not only shows trade patterns, but also helps identify vulnerabilities and opportunities in food security and nutrition-a key objective of PFTD.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

import os # Tambahkan import os di bagian paling atas file

@st.cache_data
def load_data():
    """Memuat data dari file lokal dan melakukan pra-pemrosesan awal."""
    file_path = "Pacific food and beverage trade_ The Pacific Food Trade Database data.csv" # Nama file dataset lokal kamu

    if not os.path.exists(file_path):
        st.error(f"File data '{file_path}' tidak ditemukan di folder proyek.")
        st.warning("Menggunakan data dummy untuk melanjutkan.")
        # Data dummy akan tetap digunakan sebagai fallback jika file tidak ditemukan
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
    else:
        try:
            df = pd.read_csv(file_path)
            st.success(f"Data berhasil dimuat dari '{file_path}'.")
        except Exception as e:
            st.error(f"Gagal memuat data dari file lokal '{file_path}': {e}")
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

def clean_data(df, remove_outliers_flag=True):
    df_cleaned = df.copy()
    
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

st.sidebar.title("⚙️ Data Cleanup Options")
remove_outliers = st.sidebar.checkbox("Remove Outliers (based on ‘value’)", value=True)

cleaned_for_filters = clean_data(data_for_filtering, remove_outliers_flag=remove_outliers)

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
            "Select the Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year)
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
    "Select commodity code (HS92):", available_commodities, default=available_commodities
)
selected_importers_filter = st.sidebar.multiselect("Select Importer Country (for global filters):", available_importers, default=[]) # Diganti nama agar tidak konflik
selected_exporters = st.sidebar.multiselect("Select Exporting Country:", available_exporters, default=[])

filtered_data = data_after_year_filter.copy()

if selected_commodity_codes:
    filtered_data = filtered_data[filtered_data["commodity_code"].isin(selected_commodity_codes)]
if selected_importers_filter: # Menggunakan variabel filter yang baru
    filtered_data = filtered_data[filtered_data["importer"].isin(selected_importers_filter)]
if selected_exporters:
    filtered_data = filtered_data[filtered_data["exporter"].isin(selected_exporters)]

if filtered_data.empty:
    st.warning("⚠️ No data matches the filter criteria you selected. Please change the filter selection in the sidebar.")
else:
    st.markdown("### 🧾 Summary of Filtered Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Data Rows:", f"{len(filtered_data):,}")
    total_value_sum = filtered_data['value'].sum()
    units_present = filtered_data['unit'].unique()
    display_unit = units_present[0] if len(units_present) == 1 else "(beragam)"
    col2.metric("Total Trading Volume:", f"{total_value_sum:,.0f} {display_unit}")
    min_year_display = filtered_data['year'].min()
    max_year_display = filtered_data['year'].max()
    year_range_display = f"{min_year_display} - {max_year_display}" if min_year_display != max_year_display else str(min_year_display)
    col3.metric("Range of Years (Data):", year_range_display)
    st.markdown("---")

    if 'Commodity' in filtered_data.columns and 'commodity_code' in filtered_data.columns:
        st.markdown("### 📋 Mapping Code to Commodity Name")
        
        mapping_df_temp = filtered_data[['commodity_code', 'Commodity']].drop_duplicates()
        mapping_df_temp['commodity_code_numeric_for_sort'] = pd.to_numeric(mapping_df_temp['commodity_code'], errors='coerce')
        mapping_data_final = mapping_df_temp.sort_values(
            by='commodity_code_numeric_for_sort', 
            na_position='last'
        ).drop(columns=['commodity_code_numeric_for_sort'])
        
        st.dataframe(mapping_data_final, 
                    column_config={
                        "commodity_code": st.column_config.TextColumn("Commodity Code (HS92)"),
                        "Commodity": st.column_config.TextColumn("Commodity Name")
                    },
                    hide_index=True, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        The 'Mapping Code to Commodity Name' table serves as an essential reference guide within the PFTD 2.1 visualization environment. It provides a clear and direct translation between the standardized HS92 commodity codes, which are numerical and used for consistent data classification, and their corresponding human-readable descriptive names for various food and beverage products. This mapping is crucial for users to accurately interpret the data presented in other charts and analyses, ensuring that discussions about specific traded goods like 'Meat and edible meat offal' (Code 2) or 'Cereals' (Code 10) are unambiguous and well-understood. By bridging the technical codes with plain language, this table enhances the usability and comprehensibility of the entire trade data system for a wider audience.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.info("Commodity name information (column ‘Commodity’) is not available or there is no ‘commodity_code’ data for mapping.")
        st.markdown("---")

    st.markdown("### 📦 Trading Volume per Commodity Code")
    if not filtered_data.empty and 'commodity_code' in filtered_data.columns:
        fig1_data = filtered_data.groupby("commodity_code")["value"].sum().reset_index()
        fig1_data = fig1_data.sort_values(by="value", ascending=False)
        
        fig1 = px.bar(fig1_data,
                    x="commodity_code", y="value", color="commodity_code",
                    title="Total Volume per Commodity Code (HS92)",
                    labels={"commodity_code": "Commodity Code (HS92)", "value": "Total Volume of Trades"})
        fig1.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        This bar chart details the total trading volume for each specific commodity code (classified under the HS92 system), offering a clear comparison of the scale of trade across different food and beverage categories. By visualizing the aggregated volumes side-by-side, and typically sorting them from highest to lowest, it becomes immediately apparent which types of products (e.g., cereals, meats, fish, dairy, beverages) constitute the largest share of trade within the Pacific region according to the dataset. This information is vital for understanding the composition of food trade, identifying key commodities that drive regional food supply and dependency, and focusing food security initiatives or policy considerations on the most impactful areas.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("### 📊 Annual Trading Volume Trend")
    if not filtered_data.empty and 'year' in filtered_data.columns:
        fig2_data = filtered_data.groupby("year")["value"].sum().reset_index()
        fig2 = px.line(fig2_data, x="year", y="value", markers=True, title="Trend in Total Volume per Year",
                    labels={"year": "Tahun", "value": "Total Volume of Trades"})
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        The 'Annual Trading Volume Trend' visualization provides a longitudinal perspective on the total volume of food and beverage trades pertaining to the Pacific region, typically spanning the PFTD 2.1 dataset from 1995 to 2018. This line graph charts the year-on-year progression, allowing users to identify overall growth, decline, or periods of stability in trade activity. Such trends can reflect the impact of various factors, including economic shifts, significant policy changes affecting trade, major climatic events impacting agricultural output, or evolving consumer demands, offering valuable context for understanding the broader dynamics of food availability and movement over time.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")    

    # --- PENAMBAHAN VISUALISASI: IMPORTIR TERBESAR (FIG6) ---
    st.markdown("### 🚢 Largest Importer")
    if not filtered_data.empty and 'importer' in filtered_data.columns:
        top_importers = filtered_data.groupby("importer")["value"].sum().reset_index().sort_values(by="value", ascending=False).head(10)
        if not top_importers.empty:
            fig6 = px.bar(top_importers, x="importer", y="value", color="importer", # Menggunakan 'importer' untuk warna
                        title="Top 10 Importers by Volume",
                        labels={"importer": "Importing Country", "value": "Total Import Volume"})
            st.plotly_chart(fig6, use_container_width=True)
            # Narasi untuk Importir Terbesar
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            This bar chart illustrates the top importing countries and territories within the Pacific region, ranked by their total import volume according to the applied data filters. It effectively highlights which Pacific nations are most reliant on external sources for their food and beverage supplies. Analyzing these key importers is critical for understanding food import dependency across the region, identifying potential vulnerabilities in national and regional food security should trade flows be disrupted, and pinpointing areas where efforts to boost local production or diversify import sources might be most beneficial for strengthening resilience.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("There is no importer data to display based on the current filter.")
        st.markdown("---")
    # --- AKHIR PENAMBAHAN VISUALISASI ---

    # Visualisasi Eksportir Terbesar (FIG3)
    st.markdown("### 🌍 Largest Exporter")
    if not filtered_data.empty and 'exporter' in filtered_data.columns:
        top_exporters = filtered_data.groupby("exporter")["value"].sum().reset_index().sort_values(by="value", ascending=False).head(10)
        if not top_exporters.empty:
            fig3 = px.bar(top_exporters, x="exporter", y="value", color="exporter", title="Top 10 Exporters by Volume",
                        labels={"exporter": "Exporting Country", "value": "Total Export Volume"})
            st.plotly_chart(fig3, use_container_width=True)
            # Narasi untuk Eksportir Terbesar
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            This bar chart presents a clear overview of the top exporting countries or territories contributing to the food and beverage supply within the Pacific region, ranked by their total export volume based on the selected data filters. By showcasing the most significant exporters, the visualization enables users to quickly identify the primary sources of food and beverages for the region. This understanding is fundamental for analyzing regional food supply dynamics, assessing potential dependencies on specific nations, and identifying strategic opportunities for diversifying sourcing or strengthening trade partnerships to enhance overall food security across the Pacific.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("There is no exporter data to display based on the current filter.")
            
        st.markdown("---")
    st.markdown("### 📈 Volume Distribution per Commodity Code")
    if not filtered_data.empty and 'commodity_code' in filtered_data.columns:
        fig4 = px.box(filtered_data, 
                    x="commodity_code", y="value", color="commodity_code",
                    title="Volume Distribution per Commodity Code (HS92)",
                    labels={"commodity_code": "Commodity Code (HS92)", "value": "Volume of Trade"})
        
        if 'fig1_data' in locals() and not fig1_data.empty: 
             fig4.update_xaxes(categoryorder='array', categoryarray=fig1_data['commodity_code'].tolist())
        
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 14px;'>
        This visualization offers a detailed look into the trading volume distribution for various commodity codes, classified using the HS92 system. By examining the spread and central tendency of trade volumes (often represented through elements like box plots showing quartiles, medians, and potential outliers) for each specific food and beverage category, users can identify patterns such as consistency or volatility in the trade of particular items. This insight is crucial for understanding the reliability of supply chains and the relative importance or fluctuation in the availability of different food products within the Pacific region. The arrangement of commodity codes, typically following their overall trading significance as indicated in other related charts, allows for a structured analysis from the most to least traded items, highlighting potential areas of focus for food security assessments.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("### 📉 Volume Trend per Importer")
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
                        title="Annual Volume Trend per Importer (filtered in sidebar)",
                        labels={"year": "Tahun", "value": "Total Volume Impor", "importer": "Importer Country"})
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify; font-size: 14px;'> 
            The import trend per country (selected in the global importer filter in the sidebar) shows a unique pattern of food dependency.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("There is no trend data for the importer selected in the global filter on the sidebar.")
    else:
        st.info("ℹ️ Select at least one *Importer* country in the global filter on the sidebar to see annual trends per importer.")
    st.markdown("---")

    with st.expander("📋 Display Filtered Raw Data"):
        st.dataframe(filtered_data, use_container_width=True)