from datetime import datetime

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
dkb_2_standard_values = {
    "Status": {"Gebucht": "Booked", "Vorgemerkt": "Prebooked"},
    "Umsatztyp": {"Eingang": "In", "Ausgang": "Out"},
}
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
    to_standard_values=dkb_2_standard_values,
    to_standard_columns=dkb_2_standard_columns,
    **dkb_reading_kwargs
)
