# %%
# # This notebook reads the input banking data and returns the personal finance stats by year

# %%
# Read the input data
from data import read_banking, dkb_banking_reading_kwargs

banking_data_file = "data/DKB_data_imanol.csv"
df = read_banking(banking_data_file, **dkb_banking_reading_kwargs)

# banking_data_file = "data/DKB_data_imanol.xlsx"
# df = pd.read_excel(banking_data_file)
df.dtypes
# %%
df.info()
# %%
df
# %%
# Clean data should look like this:
# -- Index: Year, Month, Day
# -- Columns: Status (0,1), Sender, Receiver, Note, Type (in, out), IBAN, Amount (€)
# -- Delete columns: Creditor ID, Mandate Reference, Customer Reference
# %%
# Final personal finance report by year should look like this
# -- Index: Year
# -- Columns directly from data: (Cash start,) Cash end, Earned, Saved, Spent, Invested in X, Invested in Y, ...
# -- Derived Columns: Investment Ratio, Investment in X, Investment in Y...
# %%
