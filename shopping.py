import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def tampilkan_shopping():
    # Load dataset
    df = pd.read_csv("shopping_trends.csv")

    # Menu Beranda
    st.title("Summary")

    # Kolom KPI
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Customer", df['Customer ID'].nunique())

    with col2:
        st.metric("Total Purchase Amount", f"${df['Purchase Amount (USD)'].sum():,.2f}")

    with col3:
        avg = df['Purchase Amount (USD)'].mean()
        st.metric("Average Purchase Amount", f"${avg:,.2f}")

    # Info kategori populer
    st.subheader("📦 Populer Product Categories")
    top_category = df['Category'].value_counts().idxmax()
    jumlah_top = df['Category'].value_counts().max()
    st.success(f"{top_category} - {jumlah_top} Transaction")

    # Metode pembayaran populer
    st.subheader("💳 Most Used Payment Method")
    top_payment = df['Payment Method'].value_counts().idxmax()
    st.info(f"{top_payment}")

    # Sidebar filter
    st.sidebar.header("Demographc Filtration")

    # 1. Filter Gender
    gender_options = df['Gender'].unique().tolist()
    selected_gender = st.sidebar.multiselect("Select Gender:", gender_options, default=gender_options)

    # 2. Filter Usia
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())
    selected_age = st.sidebar.slider("Select Age Range:", min_age, max_age, (min_age, max_age))

    # Filter data
    filtered_df = df[
        (df['Gender'].isin(selected_gender)) &
        (df['Age'] >= selected_age[0]) &
        (df['Age'] <= selected_age[1])
    ]

    st.success(f"Display {len(filtered_df)} customer data with selected filters.")

    # Top 5 Kategori Produk
    st.subheader("Top 5 Product Categories")
    top5 = df['Category'].value_counts().nlargest(5)
    fig, ax = plt.subplots()
    top5.plot(kind='bar', color="#4A90E2", ax=ax)
    ax.set_ylabel("Total Purchase Amount")
    ax.set_xlabel("Category")
    st.pyplot(fig)

    # Visualisasi 1: Pie Chart Gender
    st.subheader("Gender Distribution")
    gender_count = filtered_df['Gender'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', colors=["#4A90E2", "#FF69B4"])
    ax1.axis('equal')
    st.pyplot(fig1)

    # Visualisasi 2: Histogram Usia
    st.subheader("Age Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(filtered_df['Age'], bins=15, kde=True, color="#4A90E2", ax=ax2)
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Total Customer")
    st.pyplot(fig2)

    # Visualisasi 3: Lokasi
    st.subheader("Total Customer by Location (Top 10)")
    top_locations = filtered_df['Location'].value_counts().head(10)
    fig3, ax3 = plt.subplots()
    top_locations.plot(kind='barh', color="#50E3C2", ax=ax3)
    ax3.set_xlabel("Total Customer")
    ax3.set_ylabel("Location")
    st.pyplot(fig3)

    # Jika mau download hasil
    st.subheader("Download Filter Result Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='filtered_demographics.csv',
        mime='text/csv')