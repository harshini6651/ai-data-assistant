import streamlit as st
import pandas as pd
import mysql.connector

# ----------------------------
# Streamlit UI + Styling
# ----------------------------
st.markdown("""
<style>

/* Whole page background */
.stApp {
    background-color: #F5F5F5 !important;
}

/* Top Streamlit header bar (remove pink/dark tint) */
[data-testid="stHeader"] {
    background: #F5F5F5 !important;
}

/* Main content background */
section.main {
    background-color: #F5F5F5 !important;
}

/* Title + all headings */
h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
    text-align: center;
}

/* Normal text (st.write, captions, labels) */
.stMarkdown, .stMarkdown p, label, .stCaption, div, span {
    color: #111111 !important;
}

/* Text input box */
.stTextInput input {
    background-color: #E8E8E8 !important;
    color: #000000 !important;
    border-radius: 8px !important;
    padding: 10px !important;
    border: 1px solid #CFCFCF !important;
}

/* Button */
.stButton button {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
    height: 40px !important;
    width: 100% !important;
    font-weight: bold !important;
    border: none !important;
}

/* SQL code block background */
pre, code, .stCodeBlock {
    background-color: #E8E8E8 !important;
    color: #000000 !important;
}

/* Dataframe container */
[data-testid="stDataFrame"] {
    background-color: white !important;
}

/* Keep alerts rounded (success stays green by default) */
[data-testid="stAlert"] {
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Data Assistant")
st.write("Ask questions about your sales database")

# ----------------------------
# Database Connection (Stable)
# ----------------------------

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="ai_project"
    )

try:
    conn = get_connection()
    st.success("✅ Database Connected")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# ----------------------------
# Rule-Based SQL Generator
# ----------------------------
def generate_sql(question):
    q = question.lower()

    # Total sales
    if "total" in q and "sales" in q:
        return "SELECT SUM(sales) AS total_sales FROM sales"

    # Sales by region
    if "region" in q and "sales" in q:
        return "SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region"

    # Sales by product
    if "product" in q and "sales" in q:
        return "SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product"

    # Highest sales product
    if "highest" in q or "top" in q or "max" in q:
        return "SELECT product, sales FROM sales ORDER BY sales DESC LIMIT 1"

    # Show all data
    if "show" in q or "all" in q or "data" in q:
        return "SELECT * FROM sales"

    # Region filters
    if "east" in q:
        return "SELECT * FROM sales WHERE region = 'East'"

    if "west" in q:
        return "SELECT * FROM sales WHERE region = 'West'"

    if "north" in q:
        return "SELECT * FROM sales WHERE region = 'North'"

    return None

# ----------------------------
# User Input
# ----------------------------
question = st.text_input("Enter your question:")
st.caption("Try: total sales | sales by region | show all data | highest sales product | sales in east")

# ----------------------------
# Run Query
# ----------------------------
if st.button("Run Query") and question:

    sql_query = generate_sql(question)

    if sql_query:
        st.subheader("Generated SQL Query")
        st.code(sql_query)

        try:
            df = pd.read_sql(sql_query, conn)

            st.subheader("Query Result")
            st.dataframe(df)

            st.success("✅ Query executed successfully")

            # Optional chart if grouped data
            if "group by" in sql_query.lower():
                st.bar_chart(df.set_index(df.columns[0]))

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

    else:
        st.warning("No SQL generated. Try another question.")