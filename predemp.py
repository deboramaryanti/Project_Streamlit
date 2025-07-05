import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def tampilkan_predem():
    st.markdown("---")
    st.header("Employee Attrition Prediction")

    # Load dataset
    df = pd.read_csv("employee_attrition.csv")

    # Bersihkan target 'attrition' dari NaN dan map jika perlu
    df = df.dropna(subset=["attrition"]).copy()
    
    # Form input user
    st.markdown("Enter employee data to predict whether employees will quit (attrition) or not:")

    age = st.slider("Age", 18, 60, 30)
    st.caption("Current employee age.")

    gender = st.selectbox("Gender", ["Male", "Female"])
    st.caption("Select employee gender.")

    department = st.selectbox("Departemen", df["department"].dropna().unique())
    st.caption("The department where the employee works, such as Sales, R&D, HR, etc.")

    education_level = st.selectbox("Education Level", sorted(df["education"].dropna().unique()))
    st.caption("1 (High School), 2 (Associate Degree), 3 (Bachelor Degree), 4 (Magister Degree), 5 (Professor Degree).")

    job_role = st.selectbox("Job Role", df["job_role"].dropna().unique())
    st.caption("Employee title or position, such as Sales Executive, Research Scientist, etc.")

    monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=20000, value=5000)
    st.caption("In thousands. Example: 5000 means IDR 5,000,000.")

    marital_status = st.selectbox("Marital Status", df["marital_status"].dropna().unique())
    st.caption("Employee marital status: Single, Married, atau Divorced.")

    years_at_company = st.slider("Working Hour in year", 0, 40, 5)
    st.caption("How many years the employee has worked at the company.")

    if st.button("Attrition Prediction", key="prediksi_attrition"):
        # Fitur dan target
        features = ["age", "gender", "department", "education", "job_role",
                    "monthly_income", "marital_status", "years_at_company"]
        target = "attrition"

        # Proses target: map jika masih string, atau langsung jika sudah 0/1
        if df[target].dtype in ("int64", "float64"):
            y_raw = df[target].astype(int)
        else:
            y_raw = (
                df[target].astype(str)
                .str.strip()
                .str.lower()
                .map({"yes": 1, "no": 0, "1": 1, "0": 0})
            )

        mask_valid = y_raw.notna()
        X = pd.get_dummies(df.loc[mask_valid, features])
        y = y_raw[mask_valid].astype(int)

        # Training model
        model = RandomForestClassifier()
        model.fit(X, y)

        # Data user
        user_input = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "department": department,
            "education": education_level,
            "job_role": job_role,
            "monthly_income": monthly_income,
            "marital_status": marital_status,
            "years_at_company": years_at_company
        }])
        user_input_encoded = pd.get_dummies(user_input)
        user_input_encoded = user_input_encoded.reindex(columns=X.columns, fill_value=0)

        # Prediksi
        pred = model.predict(user_input_encoded)[0]
        prob = model.predict_proba(user_input_encoded)[0][1]

        # Hasil
        if pred == 1:
            st.error(f"❌ Employees are likely to leave. Probability: {prob:.2f}")
        else:
            st.success(f"✅ Employees are likely to remain. Probability: {1 - prob:.2f}")
        
        st.markdown("""
---
<p style='text-align:center;'>
    Made with ❤️ by Debora Maryanti | Powered by Streamlit
</p>
""", unsafe_allow_html=True)
