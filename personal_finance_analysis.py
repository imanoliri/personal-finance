# %%
# # This notebook reads the input banking data and returns the personal finance stats by year

# %%
# Read the input data
from banking_data import read_standard_banking_data
from dkb import dkb_banking_reading_kwargs

banking_data_file = "data/DKB_data_imanol.csv"
df = read_standard_banking_data(banking_data_file, **dkb_banking_reading_kwargs)

# banking_data_file = "data/DKB_data_imanol.xlsx"
# df = pd.read_excel(banking_data_file)
df.dtypes
# %%
df.info()
# %%
from finance import yearly_financial_report_from_banking_data
from imanol import (
    employers,
    investments,
    sender_aliases,
    receiver_aliases,
    reason_aliases,
)
from cleaning import clean_senders, clean_receivers, clean_reasons

df = clean_senders(df, sender_aliases)
df = clean_receivers(df, receiver_aliases)
df = clean_reasons(df, reason_aliases)
report_yearly = yearly_financial_report_from_banking_data(
    df, employers=employers, investments=investments
)
report_yearly
# %%
from finance import monthly_financial_report_from_banking_data

report_monthly = monthly_financial_report_from_banking_data(
    df, employers=employers, investments=investments
)
report_monthly
# %%
from finance import per_month_of_the_year_financial_report_from_banking_data

report_per_month_of_the_year = per_month_of_the_year_financial_report_from_banking_data(
    df, employers=employers, investments=investments
)
report_per_month_of_the_year
# %%
