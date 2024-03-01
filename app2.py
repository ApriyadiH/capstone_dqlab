import streamlit as st
import pandas as pd
import altair as alt

st.title("Hubungan Luas Lahan Kelapa Sawit dan Nilai Produk Domestik Regional Bruto")
st.write("""
Minyak nabati yang paling banyak dikonsumsi oleh umat manusia di berbagai belahan dunia merupakan minyak kelapa sawit. Produsen terbesar dari Minyak kelapa sawit merupakan negara tercinta Indonesia. Kelapa sawit merupakan salah satu pendorong perekonomian di Indonesia. Dengan menggunakan nilai Produk Domestik Regional Bruto sebagai indikator perkembangan ekonomi, kita dapat melihat dampak dari perluasan dan pengembangan lahan kelapa sawit terhadap perkembangan ekonomi.
         """)

st.header("10 Provinsi dengan luas lahan sawit terluas")
st.write("""
Provinsi dengan lahan sawit terluas akan memiliki keadaan ekonomi yang sangat bergantung pada hasil kelapa sawit.         """)

# Kode dulu
# link = 'https://drive.google.com/uc?id=1mWjqzp9uo02_0J-_E7rHI1mnqjX3wicv'
df = pd.read_csv('https://drive.google.com/uc?id=1-KD0URusqdUYO4aBi_gTeg_UFWG7UNUo', delimiter =';')
df2 = pd.read_csv('https://drive.google.com/uc?id=1dTrK2F7DHQngdzlfLO9XG1qp9sKO-KpU', delimiter=";")

kolom_dihapus = ["2010",
                 "2011",
                 "2012",
                 "2013",
                 "2022",
                 "2023"]

for kolom in kolom_dihapus:
    df.drop(columns=[kolom], inplace=True)

df = df.drop(df[df['Provinsi'] == 'Indonesia'].index)
df2 = df2.drop(df2[df2['Provinsi'] == 'Indonesia'].index)

kolom = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]

df2.replace(' -   ', '', inplace=True)
for isi_kolom in kolom:
  df2[isi_kolom] = pd.to_numeric(df2[isi_kolom])

df2['rata2'] = df2[kolom].mean(axis=1)
top_10_luas= df2.nlargest(10, 'rata2')

df['rata2'] = df[kolom].mean(axis=1)
top_10_pdrb = df.nlargest(10, 'rata2')

# Bar Chart disini top 10 terluas
st.bar_chart(
    x = top_10_luas['Provinsi'][1],
    y = top_10_luas['rata2'])





non_zero_df = df2[df2['rata2'] != 0]
top_10_sempit = non_zero_df.nsmallest(10, 'rata2')
top_10_sempit.head(10)

# Bar chart disini top 10 tersempit

df.drop(columns=['rata2'], inplace=True)
df2.drop(columns=['rata2'], inplace=True)

for isi_provinsi in top_10_luas['Provinsi']:
    df_top_10_luas = df[df['Provinsi'] == isi_provinsi]
    df2_top_10_luas = df2[df2['Provinsi'] == isi_provinsi]

    normalisasi_df = (df_top_10_luas.iloc[0, 1:] - df_top_10_luas.iloc[0, 1:].min()) / (df_top_10_luas.iloc[0, 1:].max() - df_top_10_luas.iloc[0, 1:].min())
    normalisasi_df2 = (df2_top_10_luas.iloc[0, 1:] - df2_top_10_luas.iloc[0, 1:].min()) / (df2_top_10_luas.iloc[0, 1:].max() - df2_top_10_luas.iloc[0, 1:].min())

    # Buat line chart disini

