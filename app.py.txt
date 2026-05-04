import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

st.title("Data Visualization Dashboard")

# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv("sales_data.csv")
    data.drop_duplicates(inplace=True)
    data.fillna(0, inplace=True)
    return data

data = load_data()

# Show Data
st.subheader("Dataset")
st.write(data)

# Stats
st.subheader("Key Insights")
st.write("Total Sales:", data['Sales'].sum())
st.write("Average Sales:", data['Sales'].mean())
st.write("Max Sales:", data['Sales'].max())
st.write("Min Sales:", data['Sales'].min())

# Chart Selector
chart = st.selectbox("Select Chart Type", 
                     ["Bar", "Line", "Pie", "Histogram", "Scatter"])

# BAR
if chart == "Bar":
    fig, ax = plt.subplots()
    data.groupby('Category')['Sales'].sum().plot(kind='bar', ax=ax)
    plt.title("Sales by Category")
    st.pyplot(fig)

# LINE
elif chart == "Line":
    fig, ax = plt.subplots()
    data['Date'] = pd.to_datetime(data['Date'])
    ax.plot(data['Date'], data['Sales'])
    plt.title("Sales Over Time")
    st.pyplot(fig)

# PIE
elif chart == "Pie":
    fig, ax = plt.subplots()
    data.groupby('Category')['Sales'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

# HISTOGRAM
elif chart == "Histogram":
    fig, ax = plt.subplots()
    ax.hist(data['Sales'])
    plt.title("Sales Distribution")
    st.pyplot(fig)

# SCATTER
elif chart == "Scatter":
    fig, ax = plt.subplots()
    ax.scatter(data['Sales'], data['Profit'])
    plt.xlabel("Sales")
    plt.ylabel("Profit")
    st.pyplot(fig)

# Machine Learning
st.subheader("ML Prediction (Sales → Profit)")
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