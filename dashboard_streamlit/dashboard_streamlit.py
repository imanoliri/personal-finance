import streamlit as st
import pandas as pd
from typing import List
import pickle
import matplotlib.pyplot as plt


# Run with:
# streamlit run .\dashboard_streamlit\dashboard_streamlit.py

## DATA
df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 11, 12, 13]})


report_yearly_file = "data/report_yearly_imanol.pkl"
report_monthly_file = "data/report_monthly_imanol.pkl"
report_by_month_of_the_year_file = "data/report_by_month_of_the_year_imanol.pkl"
report_files = [
    report_yearly_file,
    report_monthly_file,
    report_by_month_of_the_year_file,
]


def load_reports(filepaths: List[str]) -> pd.DataFrame:
    for filepath in filepaths:
        yield load_pickle(filepath)


def load_pickle(filepath: str) -> pd.DataFrame:
    with open(filepath, "rb") as fp:
        return pickle.load(fp)


report_yearly, report_monthly, report_by_month_of_the_year = load_reports(report_files)


## APPLICATION
st.title("Financial report dashboard (Streamlit)")


def plot_without_total(df: pd.DataFrame, y=None, kind: str = "bar", **kwargs):
    if y is None:
        y = df.columns
    y = [c for c in y if c.lower() != "total"]
    df.plot(y=y, kind="bar", **kwargs)
    st.pyplot(plt.gcf())


# Total report
report_total = report_yearly.General.sum()
report_total.index = report_total.index.droplevel(-1)
report_total.plot(kind="bar")
st.pyplot(plt.gcf())

# Yearly report
st.table(report_yearly)
report_yearly.General.plot(kind="bar")
st.pyplot(plt.gcf())

# Monthly report
st.table(report_monthly)
plot_without_total(report_monthly.Income.Employers)
plot_without_total(-report_monthly.Income.Investments)

# By month of the year report
st.table(report_by_month_of_the_year)
plot_without_total(report_by_month_of_the_year.Income.Employers)
plot_without_total(-report_by_month_of_the_year.Income.Investments)
