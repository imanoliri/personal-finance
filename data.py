import pandas as pd
from datetime import datetime

StandardBakingData = pd.DataFrame


dkb_reading_kwargs = dict(sep=";", decimal=",", thousands=".")
dkb_columns = [
    "Buchungsdatum",
    "Wertstellung",
    "Status",
    "Zahlungspflichtige*r",
    "Zahlungsempfänger*in",
    "Verwendungszweck",
    "Umsatztyp",
    "IBAN",
    "Betrag (€)",
    "Gläubiger-ID",
    "Mandatsreferenz",
    "Kundenreferenz",
]
dkb_banking_dtypes = {
    "Buchungsdatum": datetime,
    "Wertstellung": datetime,
    "Status": str,
    "Zahlungspflichtige*r": str,
    "Zahlungsempfänger*in": str,
    "Verwendungszweck": str,
    "Umsatztyp": str,
    "IBAN": str,
    "Betrag (€)": float,
    "Gläubiger-ID": str,
    "Mandatsreferenz": str,
    "Kundenreferenz": str,
}
dkb_date_format = "%d.%m.%y"
dkb_2_standard_columns = {
    "Buchungsdatum": "Booking date",
    "Wertstellung": "Paying date",
    "Status": "Status",
    "Zahlungspflichtige*r": "Sender",
    "Zahlungsempfänger*in": "Receiver",
    "Verwendungszweck": "Reason for payment",
    "Umsatztyp": "Type",
    "IBAN": "IBAN",
    "Betrag (€)": "Amount",
    "Gläubiger-ID": "Creditor ID",
    "Mandatsreferenz": "Mandate reference",
    "Kundenreferenz": "Customer reference",
}

dkb_banking_reading_kwargs = dict(
    dtypes=dkb_banking_dtypes,
    date_format=dkb_date_format,
    to_standard_columns=dkb_2_standard_columns,
    **dkb_reading_kwargs
)

standard_date_column = "Booking date"
standard_year_date_column = "Year"
standard_month_date_column = "Month"
standard_day_date_column = "Day"
standard_date_columns = [
    standard_year_date_column,
    standard_month_date_column,
    standard_day_date_column,
]
standard_time_columns_dtypes = dict(
    zip(standard_date_columns, [int] * len(standard_date_columns))
)

standard_columns = [
    "Booking date",
    "Paying date",
    "Status",
    "Sender",
    "Receiver",
    "Reason for payment",
    "Type",
    "IBAN",
    "Amount",
    "Creditor ID",
    "Mandate reference",
    "Customer reference",
]

standard_banking_dtypes = {
    **standard_time_columns_dtypes,
    standard_date_column: datetime,
    "Status": str,
    "Sender": str,
    "Receiver": str,
    "Reason for payment": str,
    "Type": str,
    "IBAN": str,
    "Amount": float,
    "Creditor ID": str,
    "Mandate reference": str,
    "Customer reference": str,
}


def read_banking(
    fpath: str, dtypes: dict, date_format: str, to_standard_columns: dict, **kwargs
) -> StandardBakingData:
    time_cols = [key for key, value in dtypes.items() if value == datetime]
    time_kwargs = {}
    dtypes_no_dates = dtypes
    if time_cols:
        time_kwargs = dict(parse_dates=time_cols, date_format=date_format)
        dtypes_no_dates = {
            key: value for key, value in dtypes.items() if key not in time_cols
        }

    return to_standard_banking(
        pd.read_csv(fpath, dtype=dtypes_no_dates, **time_kwargs, **kwargs),
        to_standard_columns=to_standard_columns,
    )


def to_standard_banking(
    df: pd.DataFrame, to_standard_columns: dict
) -> StandardBakingData:
    # Columns
    cols_to_keep = list(to_standard_columns.keys())
    df_keep = df.loc[:, cols_to_keep]
    df_keep = df_keep.rename(columns=to_standard_columns)

    # Generate time columns from Booking date , axis=1
    df_keep.loc[:, standard_date_columns] = (
        df_keep.loc[:, standard_date_column].apply(lambda x: x.timetuple()[:3]).tolist()
    )

    # Reorder columns
    df_keep = df_keep.loc[:, standard_banking_dtypes.keys()]

    return df_keep
