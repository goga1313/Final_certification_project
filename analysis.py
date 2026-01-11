import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def operations_to_df(operations: list) -> pd.DataFrame:
    """Преобразование операций в DataFrame"""
    df = pd.DataFrame([op.to_dict() for op in operations])
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def histplot_income_expense_by_category(df: pd.DataFrame):
    """Гистограмма приёма и отпуска нефтепродуктов"""
    sns.set(context="notebook", style="darkgrid")
    plt.figure(figsize = (9,5))
    graf_class = sns.barplot(
        x="category", 
        y="volume", 
        hue="op_type", 
        data=df, 
        alpha=0.7, 
        palette=["#DF25B7", "#129FE0"], 
        estimator="sum", 
        errorbar=None
        )
    # Вывод значения столбцов
    for container in graf_class.containers:
        graf_class.bar_label(container)
    graf_class.set_title("Движение нефтепродуктов по маркам топлива")
    graf_class.set_xlabel("Марка топлива")
    graf_class.set_ylabel("Объём нефтепродуктов(литры)")
    plt.legend(title='Тип операции')
    plt.show()

def plot_income_expense_over_time(df: pd.DataFrame):
    """Линейный график объёма принятых и отпущенных нефтепродуктов по датам """
    df_grouped = df.groupby(["date", "op_type"])["volume"].sum().unstack(fill_value=0)
    color = ["#08AC1E", "#EE3654"]
    df_grouped.plot(
        figsize=(8,5), 
        marker="o", 
        markersize=6, 
        linewidth=2, 
        color=color, 
        alpha=0.7, 
        linestyle="--", 
        title="Объём принятых и отпущенных нефтепродуктов по датам"
        )
    plt.xlabel("Дата")
    plt.ylabel("Объём(литры)")
    plt.legend(title='Тип операции')
    plt.grid(True)
    plt.show()

