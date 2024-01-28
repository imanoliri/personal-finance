import pandas as pd
from datetime import datetime

StandardBakingData = pd.DataFrame

standard_date_column = "Booking date"
YEAR_DATE_COLUMN = "Year"
MONTH_DATE_COLUMN = "Month"
DAY_DATE_COLUMN = "Day"
date_columns = [
    YEAR_DATE_COLUMN,
    MONTH_DATE_COLUMN,
    DAY_DATE_COLUMN,
]
standard_time_columns_dtypes = dict(zip(date_columns, [int] * len(date_columns)))

SENDER_COLUMN = "Sender"
AMOUNT_COLUMN = "Amount"
standard_banking_dtypes = {
    **standard_time_columns_dtypes,
    standard_date_column: datetime,
    "Status": str,  # Booked / Prebooked
    SENDER_COLUMN: str,
    "Receiver": str,
    "Reason for payment": str,
    "Type": str,  # In / Out
    "IBAN": str,
    AMOUNT_COLUMN: float,
    "Creditor ID": str,
    "Mandate reference": str,
    "Customer reference": str,
}


def read_standard_banking_data(
    fpath: str,
    dtypes: dict,
    date_format: str,
    to_standard_values: dict,
    to_standard_columns: dict,
    **kwargs
) -> StandardBakingData:
    time_cols = [key for key, value in dtypes.items() if value == datetime]
    time_kwargs = {}
    dtypes_no_dates = dtypes
    if time_cols:
        time_kwargs = dict(parse_dates=time_cols, date_format=date_format)
        dtypes_no_dates = {
            key: value for key, value in dtypes.items() if key not in time_cols
        }

    return to_standard_banking_data(
        pd.read_csv(fpath, dtype=dtypes_no_dates, **time_kwargs, **kwargs),
        to_standard_values=to_standard_values,
        to_standard_columns=to_standard_columns,
    )


def to_standard_banking_data(
    df: pd.DataFrame, to_standard_values: dict, to_standard_columns: dict
) -> StandardBakingData:
    # To standard values (before renaming columns)
    for col, to_standard_value in to_standard_values.items():
        if col in df.columns:
            df.loc[:, col] = df.loc[:, col].replace(to_standard_value)

    # Columns
    cols_to_keep = list(to_standard_columns.keys())
    df_keep = df.loc[:, cols_to_keep]
    df_keep = df_keep.rename(columns=to_standard_columns)

    # To standard values (also after renaming columns, just in case)
    for col, to_standard_value in to_standard_values.items():
        if col in df.columns:
            df.loc[:, col] = df.loc[:, col].replace(to_standard_value)

    # Generate time columns from Booking date , axis=1
    df_keep.loc[:, date_columns] = (
        df_keep.loc[:, standard_date_column].apply(lambda x: x.timetuple()[:3]).tolist()
    )

    # Reorder columns
    df_keep = df_keep.loc[:, standard_banking_dtypes.keys()]

    return df_keep
