import plotly.express as px
import plotly.graph_objects as go


# --------------------------------
# Funding by Industry
# --------------------------------

def funding_bar_chart(df):

    industry = df.groupby(
        "Industry"
    )["Funding Amount (M USD)"].sum().reset_index()

    fig = px.bar(
        industry,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    return fig


# --------------------------------
# Revenue vs Valuation
# --------------------------------

def revenue_valuation_scatter(df):

    fig = px.scatter(
        df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Employees",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    return fig


# --------------------------------
# Regional Distribution
# --------------------------------

def regional_pie(df):

    fig = px.pie(
        df,
        names="Region",
        title="Regional Distribution"
    )

    return fig


# --------------------------------
# Revenue Trend
# --------------------------------

def revenue_trend(df):

    trend = df.groupby(
        "Year Founded"
    )["Revenue (M USD)"].mean().reset_index()

    fig = px.line(
        trend,
        x="Year Founded",
        y="Revenue (M USD)",
        markers=True,
        title="Revenue Trend"
    )

    return fig


# --------------------------------
# Valuation Trend
# --------------------------------

def valuation_trend(df):

    trend = df.groupby(
        "Year Founded"
    )["Valuation (M USD)"].mean().reset_index()

    fig = px.line(
        trend,
        x="Year Founded",
        y="Valuation (M USD)",
        markers=True,
        title="Valuation Trend"
    )

    return fig


# --------------------------------
# Funding Distribution
# --------------------------------

def funding_histogram(df):

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=25,
        title="Funding Distribution"
    )

    return fig


# --------------------------------
# Profitability Distribution
# --------------------------------

def profitability_chart(df):

    fig = px.histogram(
        df,
        x="Profit Margin %",
        nbins=30,
        title="Profitability Distribution"
    )

    return fig


# --------------------------------
# Startup Growth Trend
# --------------------------------

def startup_growth(df):

    growth = df.groupby(
        "Year Founded"
    ).size().reset_index(
        name="Count"
    )

    fig = px.line(
        growth,
        x="Year Founded",
        y="Count",
        markers=True,
        title="Startup Growth Trend"
    )

    return fig


# --------------------------------
# Industry Revenue Comparison
# --------------------------------

def industry_revenue(df):

    rev = df.groupby(
        "Industry"
    )["Revenue (M USD)"].mean().reset_index()

    fig = px.bar(
        rev,
        x="Industry",
        y="Revenue (M USD)",
        title="Industry Revenue Comparison"
    )

    return fig


# --------------------------------
# Employee Distribution
# --------------------------------

def employee_boxplot(df):

    fig = px.box(
        df,
        x="Industry",
        y="Employees",
        title="Employee Distribution"
    )

    return fig


# --------------------------------
# Heatmap
# --------------------------------

def revenue_heatmap(df):

    heat = df.pivot_table(
        values="Revenue (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="mean"
    )

    fig = px.imshow(
        heat,
        aspect="auto",
        title="Revenue Heatmap"
    )

    return fig


# --------------------------------
# Cluster Scatter
# --------------------------------

def cluster_chart(df):

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        color=df["Cluster"].astype(str),
        hover_name="Startup Name",
        title="Cluster Analysis"
    )

    return fig
