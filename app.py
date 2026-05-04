import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Advanced Data Visualization Dashboard")

# 📂 FILE UPLOAD
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.warning("Using default dataset")
    data = pd.read_csv("sales_data.csv")

# 🧹 DATA CLEANING (SAFE)
data.drop_duplicates(inplace=True)

# Handle missing values safely
num_cols = data.select_dtypes(include=['number']).columns
data[num_cols] = data[num_cols].fillna(0)

text_cols = data.select_dtypes(include=['object']).columns
data[text_cols] = data[text_cols].fillna("Unknown")

# 📊 SHOW DATA
st.subheader("Dataset Preview")
st.dataframe(data)

# 🎛️ FILTER (only if Category exists)
if "Category" in data.columns:
    category = st.sidebar.selectbox("Select Category", data["Category"].unique())
    filtered_data = data[data["Category"] == category]
else:
    filtered_data = data

# 📈 STATS
st.subheader("Key Insights")
st.write("Total:", filtered_data.select_dtypes(include='number').sum())
st.write("Average:", filtered_data.select_dtypes(include='number').mean())

# 📊 CHART SELECTOR
chart = st.sidebar.selectbox("Select Chart", 
                            ["Bar", "Line", "Pie", "Histogram", "Scatter"])

# 📊 BAR CHART
if chart == "Bar":
    if "Category" in filtered_data.columns and "Sales" in filtered_data.columns:
        fig, ax = plt.subplots()
        filtered_data.groupby('Category')['Sales'].sum().plot(kind='bar', ax=ax)
        st.pyplot(fig)
    else:
        st.error("Bar chart requires 'Category' and 'Sales' columns")

# 📈 LINE CHART
elif chart == "Line":
    if "Date" in filtered_data.columns and "Sales" in filtered_data.columns:
        filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], errors='coerce')
        fig, ax = plt.subplots()
        ax.plot(filtered_data['Date'], filtered_data['Sales'])
        st.pyplot(fig)
    else:
        st.error("Line chart requires 'Date' and 'Sales' columns")

# 🥧 PIE CHART
elif chart == "Pie":
    if "Category" in filtered_data.columns and "Sales" in filtered_data.columns:
        fig, ax = plt.subplots()
        filtered_data.groupby('Category')['Sales'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)
    else:
        st.error("Pie chart requires 'Category' and 'Sales' columns")

# 📉 HISTOGRAM
elif chart == "Histogram":
    fig, ax = plt.subplots()
    filtered_data.select_dtypes(include='number').hist(ax=ax)
    st.pyplot(fig)

# 🔵 SCATTER PLOT
elif chart == "Scatter":
    if "Sales" in filtered_data.columns and "Profit" in filtered_data.columns:
        fig, ax = plt.subplots()
        ax.scatter(filtered_data['Sales'], filtered_data['Profit'])
        st.pyplot(fig)
    else:
        st.error("Scatter requires 'Sales' and 'Profit' columns")

# 🤖 MACHINE LEARNING
st.subheader("📈 ML Prediction")

if "Sales" in data.columns and "Profit" in data.columns:
    X = data[['Sales']]
    y = data['Profit']

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    fig, ax = plt.subplots()
    ax.scatter(X, y, label="Actual")
    ax.plot(X, predictions, label="Prediction")
    ax.legend()
    st.pyplot(fig)
else:
    st.error("ML requires 'Sales' and 'Profit' columns")on")
    ax.legend()
    st.pyplot(fig)
