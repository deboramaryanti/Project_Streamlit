import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

def tampilkan_employee():
    st.title("Summary")

    # Load dataset
    df = pd.read_csv("employee_attrition.csv")

    # Kolom KPI
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Employee", df['employee_number'].nunique())

    with col2:
        avg = df['job_satisfaction'].mean()
        st.metric("Average Job Satisfaction", f"{avg:,.2f}")

    with col3:
        avg = df['age'].mean()
        st.metric("Average Age", f"{avg:,.2f}")

    # Departemen dengan karyawan terbanyak
    st.subheader("Department with the Most Employees")
    top_dept = df['department'].value_counts().idxmax()
    st.info(f"{top_dept}")

    # Distribusi numerik
    st.markdown("Numerical Distribution")

    st.write("Age")
    fig, ax = plt.subplots()
    sns.histplot(df['age'], kde=True, bins=20, ax=ax, color='skyblue')
    st.pyplot(fig)

    st.write("Total Working Hours")
    fig2, ax2 = plt.subplots()
    sns.histplot(df['total_working_years'], kde=True, bins=20, ax=ax2, color='orange')
    st.pyplot(fig2)

    st.write("Monthly Income")
    fig3, ax3 = plt.subplots()
    sns.histplot(df['monthly_income'], kde=True, bins=20, ax=ax3, color='green')
    st.pyplot(fig3)

    st.write("Length of Service at the Company")
    fig4, ax4 = plt.subplots()
    sns.histplot(df['years_at_company'], kde=True, bins=20, ax=ax4, color='purple')
    st.pyplot(fig4)

    # Distribusi Kategorikal
    st.markdown("Categorical Distribution")
    kategori = ["gender", "marital_status", "department"]

    for col in kategori:
        st.write(f"Distribution {col.capitalize()}")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x=col, palette="Set2", ax=ax)
        plt.xticks(rotation=15)
        st.pyplot(fig)

    # Perbandingan Attrition
    st.markdown("Attrition Status Comparison")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="attrition", palette="pastel")
    ax.set_xticklabels(["Survive", "Leave"])
    st.pyplot(fig)

    # Encode kolom kategorikal
    df_encoded = df.copy()
    le = LabelEncoder()
    for col in df_encoded.select_dtypes(include='object').columns:
        df_encoded[col] = le.fit_transform(df_encoded[col])

    # Pisahkan fitur dan target
    X = df_encoded.drop("attrition", axis=1)
    y = df_encoded["attrition"]

    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # Feature importance
    importances = rf.feature_importances_
    features = X.columns
    indices = np.argsort(importances)[::-1]

    st.markdown("🔽 10 Most Influential Features")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=importances[indices][:10], y=features[indices][:10], palette="coolwarm", ax=ax)
    ax.set_title("Top 10 Feature Importance")
    st.pyplot(fig)

    # Sidebar filter
    st.sidebar.header("Demographic Filtration")

    # 1. Filter Gender
    gender_options = df['gender'].unique().tolist()
    selected_gender = st.sidebar.multiselect("Select Gender:", gender_options, default=gender_options)

    # 2. Filter Department
    dept_options = df['department'].unique().tolist()
    selected_dept = st.sidebar.multiselect("Select Department:", dept_options, default=dept_options)

    # Filter Status Pernikahan
    marital_options = df['marital_status'].unique().tolist()
    selected_marital = st.sidebar.multiselect("Select Marital Status:", marital_options, default=marital_options)

    # Terapkan filter
    filtered_df = df[
        (df["gender"].isin(selected_gender)) &
        (df["department"].isin(selected_dept)) &
        (df["marital_status"].isin(selected_marital))
    ]

    st.success(f"Display {len(filtered_df)} employee data with selected filters.")

    # Jika mau download hasil
    st.subheader("Download Filter Result Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='filtered_demographics_employee.csv',
        mime='text/csv')