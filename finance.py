import pandas as pd
import numpy as np
from banking_data import (
    YEAR_DATE_COLUMN,
    MONTH_DATE_COLUMN,
    SENDER_COLUMN,
    RECEIVER_COLUMN,
    REASON_COLUMN,
    AMOUNT_COLUMN,
)


from typing import List


def yearly_financial_report_from_banking_data(
    df_banking: pd.DataFrame,
    employers: List[str],
    investments: List[str],
    round_decimals: str = 2,
) -> pd.DataFrame:
    return groupby_finance_data_from_banking_data(
        df_banking=df_banking,
        groupby_cols=[YEAR_DATE_COLUMN],
        employers=employers,
        investments=investments,
        round_decimals=round_decimals,
    )


def monthly_financial_report_from_banking_data(
    df_banking: pd.DataFrame,
    employers: List[str],
    investments: List[str],
    round_decimals: str = 2,
) -> pd.DataFrame:
    return groupby_finance_data_from_banking_data(
        df_banking=df_banking,
        groupby_cols=[YEAR_DATE_COLUMN, MONTH_DATE_COLUMN],
        employers=employers,
        investments=investments,
        round_decimals=round_decimals,
    )


def per_month_of_the_year_financial_report_from_banking_data(
    df_banking: pd.DataFrame,
    employers: List[str],
    investments: List[str],
    round_decimals: str = 2,
) -> pd.DataFrame:
    return groupby_finance_data_from_banking_data(
        df_banking=df_banking,
        groupby_cols=[MONTH_DATE_COLUMN],
        employers=employers,
        investments=investments,
        round_decimals=round_decimals,
    )


def groupby_finance_data_from_banking_data(
    df_banking: pd.DataFrame,
    groupby_cols: List[str],
    employers: List[str],
    investments: List[str],
    round_decimals: str = 2,
) -> pd.DataFrame:
    df_result = (
        df_banking.groupby(groupby_cols)
        .apply(
            extract_finance_data,
            employers=employers,
            investments=investments,
        )
        .round(round_decimals)
    )
    if isinstance(df_result, pd.Series):
        return df_result.unstack(groupby_cols).T
    return df_result


def extract_finance_data(
    df: pd.DataFrame, employers: List[str], investments: List[str]
) -> pd.DataFrame:
    # Basic stats
    df_positives = df.loc[df.loc[:, AMOUNT_COLUMN] > 0]
    df_negatives = df.loc[df.loc[:, AMOUNT_COLUMN] < 0]

    pos_stats = basic_stats(df_positives, name="Positives")
    neg_stats = basic_stats(df_negatives, name="Negatives")

    # Employment data
    employer_stats = pd.Series(
        [np.NaN], index=pd.MultiIndex.from_tuples([("Income", "Employers", "Total")])
    )
    if employers:
        employer_stats = get_stats_from_column_group(
            df_positives, SENDER_COLUMN, employers, [["Income"], ["Employers"]]
        )

    # Investment data
    investment_stats = pd.Series(
        [np.NaN],
        index=pd.MultiIndex.from_tuples([("Income", "Investments", "Total")]),
    )
    if investments:
        investment_stats = get_stats_from_column_group(
            df_negatives, REASON_COLUMN, investments, [["Income"], ["Investments"]]
        )

    invested_amount = -df_negatives.loc[
        (r in investments for r in df_negatives.Reason), AMOUNT_COLUMN
    ].sum()
    spent_amount = -df_negatives.loc[:, AMOUNT_COLUMN].sum() - invested_amount
    summary = pd.Series(
        [
            df_positives.loc[:, AMOUNT_COLUMN].sum(),
            df.loc[:, AMOUNT_COLUMN].sum(),
            spent_amount,
            invested_amount,
        ],
        index=pd.MultiIndex.from_tuples(
            [
                ("General", "Income", "Total"),
                ("General", "Saved", "Total"),
                ("General", "Spent", "Total"),
                ("General", "Invested", "Total"),
            ]
        ),
    ).T

    return pd.concat([summary, employer_stats, investment_stats, pos_stats, neg_stats])


def basic_stats(df: pd.DataFrame, name: str) -> pd.Series:
    return pd.Series(
        [
            len(df),
            df.loc[:, AMOUNT_COLUMN].median(),
            df.loc[:, AMOUNT_COLUMN].mean(),
        ],
        index=pd.MultiIndex.from_product([[name], ["count", "median", "mean"], [""]]),
    ).T


def get_stats_from_column_group(
    df: pd.DataFrame,
    grouping_column: str,
    column_values: List[str],
    over_levels: List[List[str]],
) -> pd.Series:
    df_selected = select_from_column(df, grouping_column, column_values)
    amount_by_sender = (
        df_selected.loc[:, [grouping_column, AMOUNT_COLUMN]]
        .groupby(grouping_column)
        .sum()
    )
    amount_by_sender = amount_by_sender.loc[:, AMOUNT_COLUMN]
    amount_by_sender.index = pd.MultiIndex.from_product(
        [*over_levels, amount_by_sender.index.values],
    )
    return pd.concat(
        [
            pd.Series(
                [df_selected.loc[:, AMOUNT_COLUMN].sum()],
                index=pd.MultiIndex.from_product(
                    [*over_levels, ["Total"]],
                ),
            ),
            amount_by_sender,
        ]
    )


def select_from_column(
    df: pd.DataFrame, col: str, selected_senders: List[str] = None
) -> pd.DataFrame:
    return df.loc[(sender in selected_senders for sender in df.loc[:, col])]


def prefix_dict_keys(di: dict, prefix: str) -> dict:
    return {f"{prefix}_{key}": value for key, value in di.items()}
