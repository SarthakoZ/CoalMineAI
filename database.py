import psycopg2
import streamlit as st


def get_connection():
    connection = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )

    return connection


if __name__ == "__main__":
    connection = get_connection()
    print("Database connected successfully!")
    connection.close()