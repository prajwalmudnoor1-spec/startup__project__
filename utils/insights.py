import pandas as pd


# -----------------------------------
# Basic KPI Insights
# -----------------------------------

def get_basic_kpis(df):

    insights = {}

    insights["total_startups"] = len(df)

    insights["total_funding"] = round(
        df["Funding Amount (M USD)"].sum(),
        2
    )

    insights["avg_revenue"] = round(
        df["Revenue (M USD)"].mean(),
        2
    )

    insights["avg_valuation"] = round(
        df["Valuation (M USD)"].mean(),
        2
    )

    return insights


# -----------------------------------
# Top Industry
# -----------------------------------

def highest_funding_industry(df):

    industry = df.groupby(
        "Industry"
    )["Funding Amount (M USD)"].mean()

    return industry.idxmax()


# -----------------------------------
# Highest Revenue Industry
# -----------------------------------

def highest_revenue_industry(df):

    revenue = df.groupby(
        "Industry"
    )["Revenue (M USD)"].mean()

    return revenue.idxmax()


# -----------------------------------
# Highest Valuation Industry
# -----------------------------------

def highest_valuation_industry(df):

    value = df.groupby(
        "Industry"
    )["Valuation (M USD)"].mean()

    return value.idxmax()


# -----------------------------------
# Most Active Region
# -----------------------------------

def top_region(df):

    return df["Region"].mode()[0]


# -----------------------------------
# Best Startup by Revenue
# -----------------------------------

def top_revenue_startup(df):

    return df.loc[
        df[
            "Revenue (M USD)"
        ].idxmax(),
        "Startup Name"
    ]


# -----------------------------------
# Best Startup by Valuation
# -----------------------------------

def top_valuation_startup(df):

    return df.loc[
        df[
            "Valuation (M USD)"
        ].idxmax(),
        "Startup Name"
    ]


# -----------------------------------
# Funding Efficiency
# Revenue / Funding
# -----------------------------------

def funding_efficiency(df):

    temp = df.copy()

    temp["Efficiency"] = (
        temp["Revenue (M USD)"]
        /
        temp["Funding Amount (M USD)"]
    )

    return temp.sort_values(
        "Efficiency",
        ascending=False
    )


# -----------------------------------
# Profitability Calculation
# -----------------------------------

def profitability(df):

    temp = df.copy()

    temp["Profit Margin %"] = (
        (
            temp["Revenue (M USD)"]
            -
            temp["Funding Amount (M USD)"]
        )
        /
        temp["Revenue (M USD)"]
    ) * 100

    return temp


# -----------------------------------
# Growth Trend
# -----------------------------------

def startup_growth(df):

    growth = df.groupby(
        "Year Founded"
    ).size()

    return growth


# -----------------------------------
# Market Concentration
# -----------------------------------

def market_share(df):

    market = df.groupby(
        "Industry"
    ).size()

    percentage = round(
        (market / market.sum()) * 100,
        2
    )

    return percentage


# -----------------------------------
# AI Recommendation Engine
# -----------------------------------

def recommendations(df):

    rec = []

    top_industry = highest_revenue_industry(
        df
    )

    best_region = top_region(
        df
    )

    rec.append(
        f"Focus expansion on {top_industry}"
    )

    rec.append(
        f"Increase market presence in {best_region}"
    )

    if df[
        "Funding Amount (M USD)"
    ].mean() > 100:

        rec.append(
            "Funding levels are high. Improve profitability."
        )

    else:

        rec.append(
            "Funding levels are moderate."
        )

    return rec


# -----------------------------------
# Executive Summary Generator
# -----------------------------------

def executive_summary(df):

    summary = {}

    summary["top_industry"] = highest_revenue_industry(
        df
    )

    summary["top_region"] = top_region(
        df
    )

    summary["best_company"] = top_valuation_startup(
        df
    )

    summary["startup_count"] = len(
        df
    )

    return summary


# -----------------------------------
# Risk Detection
# -----------------------------------

def risk_analysis(df):

    risky = df[
        df["Revenue (M USD)"]
        <
        df["Funding Amount (M USD)"]
    ]

    return risky


# -----------------------------------
# Unicorn Detection
# -----------------------------------

def unicorns(df):

    return df[
        df["Valuation (M USD)"] >= 1000
    ]


# -----------------------------------
# Industry Ranking
# -----------------------------------

def industry_rankings(df):

    ranking = df.groupby(
        "Industry"
    )[[
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Valuation (M USD)"
    ]].mean()

    ranking["Score"] = (
        ranking["Funding Amount (M USD)"]
        +
        ranking["Revenue (M USD)"]
        +
        ranking["Valuation (M USD)"]
    )

    ranking = ranking.sort_values(
        "Score",
        ascending=False
    )

    return ranking
