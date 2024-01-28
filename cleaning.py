from typing import Dict, List
import pandas as pd
from banking_data import SENDER_COLUMN


Aliases = Dict[str, List[str]]


def clean_senders(df: pd.DataFrame, sender_aliases: Aliases) -> pd.DataFrame:
    return clean_strings(df, SENDER_COLUMN, sender_aliases)


def clean_strings(df: pd.DataFrame, col: str, aliases: Aliases) -> pd.DataFrame:
    df.loc[:, col] = df.loc[:, col].apply(replace_string, aliases=aliases)
    return df


def replace_string(
    s: str, aliases: Aliases, return_clean_string_default: bool = False
) -> str:
    s_clean = standard_string(s)
    for k, vs in aliases.items():
        if isinstance(vs, str):
            if s_clean == standard_string(vs):
                return k
        for v in vs:
            if s_clean == standard_string(v):
                return k

    if return_clean_string_default:
        return s_clean
    return s


def standard_string(s: str) -> str:
    return s.lower().replace(",", " ").strip()
