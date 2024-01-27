#%%
# # This notebook reads the input banking data and returns the personal finance stats by year

#%% 
# Read the input data
import pandas as pd
banking_data_file = 'data/DKB_data_imanol.xlsx'
df = pd.read_excel(banking_data_file)
df
#%%
# Clean data should look like this:
# -- Index: Year, Month, Day
# -- Columns: Status (0,1), Sender, Receiver, Note, Type (in, out), IBAN, Ammount (€)
# -- Delete columns: Believer-ID?, Reference, Customer Reference
#%%
# Final personal finance report by year should look like this
# -- Index: Year
# -- Columns directly from data: (Cash start,) Cash end, Earned, Saved, Spent, Invested in X, Invested in Y, ...
# -- Derived Columns: Investment Ratio, Investment in X, Investment in Y...
#%%