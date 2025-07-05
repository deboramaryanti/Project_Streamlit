import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def tampilkan_predshop():
    df = pd.read_csv("shopping_trends.csv")

    st.title("Purchase Amount (USD) Prediction")

    # Pilihan input pengguna
    gender = st.selectbox("Select Gender:", df['Gender'].unique())
    age = st.slider("Age:", min_value=15, max_value=70, value=30)
    category = st.selectbox("Product Categories:", df['Category'].unique())
    payment = st.selectbox("Payment Method:", df['Payment Method'].unique())

    # Siapkan data & model
    X = df[['Gender', 'Age', 'Category', 'Payment Method']]
    y = df['Purchase Amount (USD)']

    # Pipeline preprocessing + model
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), ['Gender', 'Category', 'Payment Method'])
        ],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    model.fit(X, y)

    # Prediksi berdasarkan input pengguna
    input_df = pd.DataFrame({
        'Gender': [gender],
        'Age': [age],
        'Category': [category],
        'Payment Method': [payment]
    })

    prediction = model.predict(input_df)[0]

    # Tampilkan hasil
    st.markdown("Prediction Result")
    st.success(f"Purchase Amount Prediction is **${prediction:,.2f}**")