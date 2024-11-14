import asyncio
from utils.sqlite_utils import Database
from utils.init_utils import initialize_app
import pandas as pd
import streamlit as st


async def main():
    initialize_app()
    db = Database("letterboxd.db")
    last_month_entries = db.filter_diary_entries({"watched_date": "2019-03-15"})
    df = pd.DataFrame(last_month_entries)
    st.table(df)


if __name__ == "__main__":
    asyncio.run(main())
