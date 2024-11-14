from utils.sqlite_utils import Database
import pandas as pd
import streamlit as st

def main():
    db = Database("letterboxd.db")
    last_month_entries = db.filter_diary_entries({"watched_date": "2019-03-15"})
    df = pd.DataFrame(last_month_entries)
    st.table(df)
    print("Hello from chatboxd!")


if __name__ == "__main__":
    main()
