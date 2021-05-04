#import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import altair as alt

# loading data and doing the preprocessing
st.title("Louisas Gapminder")


@st.cache
def load():
    income = pd.read_csv(
        "/Users/LouisaEbert/Desktop/HWR - BIPM/Enterprise Architectures of Big Data /Data/income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    f_income = pd.melt(income,
                       ["country"],
                       var_name="year",
                       value_name="income")
    f_income = f_income.sort_values(by=["country", "year"])
    f_income.ffill()

    lifeexp = pd.read_csv(
        "/Users/LouisaEbert/Desktop/HWR - BIPM/Enterprise Architectures of Big Data /Data/life_expectancy_years.csv")
    f_le = pd.melt(lifeexp,
                   ["country"],
                   var_name="year",
                   value_name="lifeexp")
    f_le = f_le.sort_values(by=["country", "year"])
    f_le = f_le.astype({"year": int})
    f_le.ffill()

    population = pd.read_csv(
        "/Users/LouisaEbert/Desktop/HWR - BIPM/Enterprise Architectures of Big Data /Data/population_total.csv")
    f_pop = pd.melt(population,
                    ["country"],
                    var_name="year",
                    value_name="population")
    f_pop = f_pop.sort_values(by=["country", "year"])
    f_pop.ffill()

    df2 = f_income.merge(f_pop, how='inner', left_on=["country", "year"], right_on=["country", "year"])
    df2 = df2.astype({"year": int})

    df = df2.merge(f_le, how='inner', left_on=["country", "year"], right_on=["country", "year"])
    df['gni'] = np.log(df['income'])

    return df


df = load()

# creating the sliders
years = st.sidebar.slider('Year', int(df.year.min()), int(df.year.max()))

# creating multiselect for countries
countries = st.sidebar.multiselect("Select countries", df.country.unique())
subset_df = df.loc[lambda d: d['country'].isin(countries)]
subset_df = subset_df[(subset_df.year == years)]
subset_df.head()

bubble = sns.scatterplot(subset_df['gni'], subset_df['lifeexp'], hue=subset_df['country'], size=subset_df['population'],
                         sizes=(20, 400), legend="full")

plt.grid(True)
plt.legend(bbox_to_anchor=(1.05,1.0),loc='upper left')
# plt.xscale('log')
plt.xlabel('log GNI [in USD]', fontsize=14)
plt.ylabel('Life Expectancy [in years]', fontsize=14)
#plt.title('Louisas Gapminder', fontsize=20)
plt.axvline(max(df['gni']), 0, 1)
plt.xticks([0, 4, 8, 12])

st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
