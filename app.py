import streamlit as st
import pandas as pd
import altair as alt
# import matplotlib.pyplot as plt

# Judul
st.title('Hubungan Kelapa Sawit dan Nilai Produk Domestik Regional Bruto')

# Tabs
# tab1, tab2, tab3, tab4, tab5 = st.tabs(['Informasi Project', 'Area', 'Produktivitas', 'Kesimpulan'])
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Informasi Project', 'Area', 'Area %', 'Produktivitas', 'Kesimpulan'])

with tab1:
    st.header('Informasi Project')
    st.write('''
        Minyak nabati yang paling banyak dikonsumsi oleh umat manusia di berbagai belahan dunia merupakan minyak kelapa sawit. Produsen terbesar dari Minyak kelapa sawit merupakan negara tercinta Indonesia. Kelapa sawit merupakan salah satu pendorong perekonomian di Indonesia. Dengan menggunakan nilai Produk Domestik Regional Bruto sebagai indikator perkembangan ekonomi, kita dapat melihat dampak dari perluasan dan pengembangan lahan kelapa sawit terhadap perkembangan ekonomi.
            ''')
    
    with st.expander('Target'):
        st.write('''
            Pemerintahan yang berhubungan dengan pertanian dan perkebunan, Kelompok/Organisasi petani sawit
             ''')

    with st.expander('Scope'):
        st.write('''
                Proses analisa menggunakan data dari BPS dari tahun 2014 hingga 2021.
                Data yang digunakan berupa luas lahan kelapa sawit, produktivitas sawit dan PDRB.
                ''')

    with st.expander('Problem Statement'):
        st.write('''
                Analisis akan digunakan untuk mengetahui hubungan perkembangan sawit dnegan kemajuan ekonomi.
                ''')

    with st.expander('Objectives'):
        st.write('''
                Dengan data, perkembangan ekonomi daerah yang didominasi oleh pertanian sawit akan diketahui. 
                Informasi mengenai daerah yang sukses dan yang kurang berhasil dapat dibandingkan dan dipelajari lebih lanjut.
                ''')

    with st.expander('Defining Question'):
        st.write('''
                Bagaimana korelasi perkembangan sawit dan ekonomi?
                ''')
        
    with st.expander('Hipotesis'):
        st.write('''
                Sawit yang berkembang dapat mendorong ekonomi daerah tersebut dan memiliki korelasi positif.
                ''')

with tab2:
    # Konten Luas
    st.header('10 Provinsi dengan luas lahan sawit terluas')
    st.write('''
             Provinsi dengan lahan sawit terluas akan memiliki keadaan ekonomi yang sangat bergantung pada hasil kelapa sawit.         
             ''')

    df = pd.read_csv('https://drive.google.com/uc?id=1-KD0URusqdUYO4aBi_gTeg_UFWG7UNUo', delimiter =';')
    df2 = pd.read_csv('https://drive.google.com/uc?id=1dTrK2F7DHQngdzlfLO9XG1qp9sKO-KpU', delimiter=';')

    kolom_dihapus = ['2010',
                    '2011',
                    '2012',
                    '2013',
                    '2022',
                    '2023']

    for kolom in kolom_dihapus:
        df.drop(columns=[kolom], inplace=True)

    df = df.drop(df[df['Provinsi'] == 'Indonesia'].index)
    df2 = df2.drop(df2[df2['Provinsi'] == 'Indonesia'].index)

    kolom = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

    df2.replace(' -   ', '', inplace=True)
    for isi_kolom in kolom:
        df2[isi_kolom] = pd.to_numeric(df2[isi_kolom])

    df2['rata2'] = df2[kolom].mean(axis=1)
    top_10_luas= df2.nlargest(10, 'rata2')

    rata2_terbesar = top_10_luas['rata2'].max()
    prov_terbesar = top_10_luas[top_10_luas['rata2']==rata2_terbesar]
    prov_terbesar = prov_terbesar.iloc[0, prov_terbesar.columns.get_loc('Provinsi')]

    # Bar Chart top 10 terluas
    top_10_luas_bar = alt.Chart(top_10_luas).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_terbesar,
            alt.value('orange'),
            alt.value('green')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_luas_bar)

    non_zero_df = df2[df2['rata2'] != 0]
    top_10_sempit = non_zero_df.nsmallest(10, 'rata2')
    top_10_sempit.head(10)

    st.header('10 Provinsi dengan luas lahan sawit terkecil dan bukan nol')
    st.write('''
    Provinsi yang memulai proses penanaman kelapa sawit. Belum tentu bergantung pada produktivitas kelapa sawit.
            ''')

    rata2_terkecil = top_10_sempit['rata2'].min()
    prov_terkecil = top_10_sempit[top_10_sempit['rata2']==rata2_terkecil]
    prov_terkecil = prov_terkecil.iloc[0, prov_terkecil.columns.get_loc('Provinsi')]

    # Bar chart top 10 tersempit
    top_10_sempit_bar = alt.Chart(top_10_sempit).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_terkecil,
            alt.value('cyan'),
            alt.value('gray')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_sempit_bar)

    df2.drop(columns=['rata2'], inplace=True)

    st.title('Hubungan nilai PDRB dan luas lahan kelapa sawit ')

    pilih_provinsi = st.selectbox(
        'Pilih provinsi yang akan ditampilkan',
        df['Provinsi']
    )

    df_pilih = df[df['Provinsi'] == pilih_provinsi]
    df2_pilih = df2[df2['Provinsi'] == pilih_provinsi]

    normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
    normalisasi_df2 = (df2_pilih.iloc[0, 1:] - df2_pilih.iloc[0, 1:].min()) / (df2_pilih.iloc[0, 1:].max() - df2_pilih.iloc[0, 1:].min())
    
    merged_df = pd.DataFrame({
    'tahun': kolom,
    'pdrb' : normalisasi_df,
    'area' : normalisasi_df2
    })

    correlation_coefficient = merged_df['pdrb'].corr(merged_df['area'])
    st.write('Korelasi Pearson: ', correlation_coefficient)

    df_melted = merged_df.melt(id_vars='tahun', var_name='Line', value_name='Normalisasi')
    hasil_grafik = alt.Chart(df_melted).mark_line().encode(
        x='tahun:O',
        y='Normalisasi:Q',
        color='Line:N',
    ).properties(
        width=500,
        height=300,
        title='Perbandingan PDRB terhadap luas lahan sawit Provinsi ' + pilih_provinsi
    ).configure_axis(
        grid=False
    )

    st.altair_chart(hasil_grafik,use_container_width=True)

    st.header('Hasil Korelasi')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top 10 Terluas')
        for pilih_provinsi in top_10_luas['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            df2_pilih = df2[df2['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_df2 = (df2_pilih.iloc[0, 1:] - df2_pilih.iloc[0, 1:].min()) / (df2_pilih.iloc[0, 1:].max() - df2_pilih.iloc[0, 1:].min())
            
            merged_df = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'area' : normalisasi_df2
            })

            correlation_coefficient = merged_df['pdrb'].corr(merged_df['area'])
            if correlation_coefficient <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
                
    with col2:
        st.subheader('Top 10 Terkecil')
        for pilih_provinsi in top_10_sempit['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            df2_pilih = df2[df2['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_df2 = (df2_pilih.iloc[0, 1:] - df2_pilih.iloc[0, 1:].min()) / (df2_pilih.iloc[0, 1:].max() - df2_pilih.iloc[0, 1:].min())
            
            merged_df = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'area' : normalisasi_df2
            })

            correlation_coefficient = merged_df['pdrb'].corr(merged_df['area'])
            if correlation_coefficient <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
    
with tab3:
    st.header('10 Provinsi dengan Persentase Luas Lahan Terbesar')
    st.write('Semakin tinggi persentase lahan kelapa sawit, maka perekonomian masyarakat akan semakin tergantung pada sawit.')

    df4 = pd.read_csv('https://drive.google.com/uc?id=1JTgdN7ZOT-jlQdOYYqJPKMJKY13yb9nz', delimiter=';')

    merged_df_persen = pd.merge(df4, df2, on='Provinsi', how='left')

    for isi_kolom in kolom:
        merged_df_persen[isi_kolom] = merged_df_persen[isi_kolom]/merged_df_persen['Luas Wilayah']
        merged_df_persen[isi_kolom] = merged_df_persen[isi_kolom].apply(lambda x: "{:.2f}".format(x))
        merged_df_persen[isi_kolom] = merged_df_persen[isi_kolom].astype(float)
        

    merged_df_persen['rata2'] = merged_df_persen[kolom].mean(axis=1)
    top_10_persen_besar= merged_df_persen.nlargest(10, 'rata2')

    rata2_persen_besar = top_10_persen_besar['rata2'].max()
    prov_persen_besar = top_10_persen_besar[top_10_persen_besar['rata2']==rata2_persen_besar]
    prov_persen_besar = prov_persen_besar.iloc[0, prov_persen_besar.columns.get_loc('Provinsi')]

    # Bar Chart top 10 persentase terbesar
    top_10_persen_besar_bar = alt.Chart(top_10_persen_besar).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_persen_besar,
            alt.value('orange'),
            alt.value('green')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_persen_besar_bar)

    non_zero_df_persen = merged_df_persen[merged_df_persen['rata2'] > 0]
    top_10_persen_kecil = non_zero_df_persen.nsmallest(10, 'rata2')
    top_10_persen_kecil.head(10)

    st.header('10 Provinsi dengan Persentase lahan sawit terkecil dan bukan nol')
    st.write('''
    Provinsi yang perekonomiannya tidak terlalu bergantung pada sawit.
            ''')

    rata2_persen_kecil = top_10_persen_kecil['rata2'].min()
    prov_persen_kecil = top_10_persen_kecil[top_10_persen_kecil['rata2']==rata2_persen_kecil]
    prov_persen_kecil = prov_persen_kecil.iloc[0, prov_persen_kecil.columns.get_loc('Provinsi')]

    # Bar chart top 10 persentase terkecil
    top_10_persen_kecil_bar = alt.Chart(top_10_persen_kecil).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_persen_kecil,
            alt.value('cyan'),
            alt.value('gray')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_persen_kecil_bar)

    merged_df_persen.drop(columns=['rata2'], inplace=True)
    merged_df_persen.drop(columns=['Luas Wilayah'], inplace=True)

    st.title('Hasil Korelasi PDRB terhadap Persentase Lahan Kelapa Sawit')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top 10 Persentase Terbesar')
        for pilih_provinsi in top_10_persen_besar['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            merged_df_persen_pilih = merged_df_persen[merged_df_persen['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_merged_df_persen = (merged_df_persen_pilih.iloc[0, 1:] - merged_df_persen_pilih.iloc[0, 1:].min()) / (merged_df_persen_pilih.iloc[0, 1:].max() - merged_df_persen_pilih.iloc[0, 1:].min())
            
            merged_df_persen_kor = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'area %' : normalisasi_merged_df_persen
            })

            correlation_coefficient_persen = merged_df_persen_kor['pdrb'].corr(merged_df_persen_kor['area %'])
            if correlation_coefficient_persen <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient_persen), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient_persen), '</span>', unsafe_allow_html=True)
                
    with col2:
        st.subheader('Top 10 Persentase Terkecil')
        for pilih_provinsi in top_10_persen_kecil['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            merged_df_persen_pilih = merged_df_persen[merged_df_persen['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_merged_df_persen = (merged_df_persen_pilih.iloc[0, 1:] - merged_df_persen_pilih.iloc[0, 1:].min()) / (merged_df_persen_pilih.iloc[0, 1:].max() - merged_df_persen_pilih.iloc[0, 1:].min())
            
            merged_df_persen_kor = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'area %' : normalisasi_merged_df_persen
            })

            correlation_coefficient_persen = merged_df_persen_kor['pdrb'].corr(merged_df_persen_kor['area %'])
            if correlation_coefficient_persen <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient_persen), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient_persen), '</span>', unsafe_allow_html=True)

with tab4:
    st.header('10 Provinsi dengan Produktivitas Sawit Tertinggi')
    st.write('''
             Produktivitas sawit yang tinggi akan mempengaruhi perekonomian daerah tersebut.         
             ''')

    df3 = pd.read_csv('https://drive.google.com/uc?id=1l9CH_ognM6YrOWr1HDuRsOlq9IWmgiJd', delimiter=';')

    kolom = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
    for isi_kolom in kolom:
        df3[isi_kolom] = df3[isi_kolom].str.replace(',', '').replace('-', '0')
        df3[isi_kolom] = pd.to_numeric(df3[isi_kolom], errors='coerce').fillna(0).astype(float)
    
    df3['rata2'] = df3[kolom].mean(axis=1)
    top_10_tinggi= df3.nlargest(10, 'rata2')

    rata2_tertinggi = top_10_tinggi['rata2'].max()
    prov_tertinggi = top_10_tinggi[top_10_tinggi['rata2']==rata2_tertinggi]
    prov_tertinggi = prov_tertinggi.iloc[0, prov_tertinggi.columns.get_loc('Provinsi')]

    # Bar Chart top 10 terluas
    top_10_tinggi_bar = alt.Chart(top_10_tinggi).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_tertinggi,
            alt.value('orange'),
            alt.value('green')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_tinggi_bar)

    non_zero_df_prod = df3[df3['rata2'] > 0 ]
    top_10_rendah = non_zero_df_prod.nsmallest(10, 'rata2')
    top_10_rendah.head(10)

    st.header('10 Provinsi dengan produktivitas sawit terendah dan bukan nol')
    st.write('''
            Daerah yang mungkin kurang efisien dalam merawat kelapa sawit.
             ''')

    rata2_terendah = top_10_rendah['rata2'].min()
    prov_terendah = top_10_rendah[top_10_rendah['rata2']==rata2_terendah]
    prov_terendah = prov_terendah.iloc[0, prov_terendah.columns.get_loc('Provinsi')]

    # Bar chart top 10 terrendah
    top_10_rendah_bar = alt.Chart(top_10_rendah).mark_bar().encode(
        alt.X('Provinsi:N', sort=alt.EncodingSortField(order='ascending')),
        alt.Y('rata2:Q'),
        color=alt.condition(
            alt.datum['Provinsi'] == prov_terendah,
            alt.value('cyan'),
            alt.value('gray')
        ),
    ).properties(
        width=720,
        height=480
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_10_rendah_bar)

    df3.drop(columns=['rata2'], inplace=True)

    st.title('Hubungan nilai PDRB dan Produktivitas kelapa sawit ')

    pilih_provinsi_prod = st.selectbox(
        'Pilih provinsi yang akan ditampilkan',
        df['Provinsi'],
        key = 'select_box_prod'
    )

    df_pilih = df[df['Provinsi'] == pilih_provinsi_prod]
    df3_pilih = df3[df3['Provinsi'] == pilih_provinsi_prod]

    normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
    normalisasi_df3 = (df3_pilih.iloc[0, 1:] - df3_pilih.iloc[0, 1:].min()) / (df3_pilih.iloc[0, 1:].max() - df3_pilih.iloc[0, 1:].min())
    
    merged_df_prod = pd.DataFrame({
    'tahun': kolom,
    'pdrb' : normalisasi_df,
    'produktivitas' : normalisasi_df3
    })

    correlation_coefficient = merged_df_prod['pdrb'].corr(merged_df_prod['produktivitas'])
    st.write('Korelasi Pearson: ', correlation_coefficient)

    df_melted = merged_df_prod.melt(id_vars='tahun', var_name='Line', value_name='Normalisasi')
    hasil_grafik = alt.Chart(df_melted).mark_line().encode(
        x='tahun:O',
        y='Normalisasi:Q',
        color='Line:N',
    ).properties(
        width=500,
        height=300,
        title='Perbandingan PDRB terhadap Produktivitas sawit Provinsi ' + pilih_provinsi_prod
    ).configure_axis(
        grid=False
    )

    st.altair_chart(hasil_grafik,use_container_width=True)

    st.header('Hasil Korelasi')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top 10 Produktivitas Tertinggi')
        for pilih_provinsi in top_10_tinggi['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            df3_pilih = df3[df3['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_df3 = (df3_pilih.iloc[0, 1:] - df3_pilih.iloc[0, 1:].min()) / (df3_pilih.iloc[0, 1:].max() - df3_pilih.iloc[0, 1:].min())
            
            merged_df_prod = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'produktivitas' : normalisasi_df3
            })

            correlation_coefficient = merged_df_prod['pdrb'].corr(merged_df_prod['produktivitas'])
            if correlation_coefficient <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
                
    with col2:
        st.subheader('Top 10 Produktivitas Terendah')
        for pilih_provinsi in top_10_rendah['Provinsi']:
            df_pilih = df[df['Provinsi'] == pilih_provinsi]
            df3_pilih = df3[df3['Provinsi'] == pilih_provinsi]

            normalisasi_df = (df_pilih.iloc[0, 1:] - df_pilih.iloc[0, 1:].min()) / (df_pilih.iloc[0, 1:].max() - df_pilih.iloc[0, 1:].min())
            normalisasi_df3 = (df3_pilih.iloc[0, 1:] - df3_pilih.iloc[0, 1:].min()) / (df3_pilih.iloc[0, 1:].max() - df3_pilih.iloc[0, 1:].min())
            
            merged_df_prod = pd.DataFrame({
            'tahun': kolom,
            'pdrb' : normalisasi_df,
            'produktivitas' : normalisasi_df3
            })

            correlation_coefficient = merged_df_prod['pdrb'].corr(merged_df_prod['produktivitas'])
            if correlation_coefficient <= 0:
                st.write('<span style="color: orange;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)
            else:
                st.write('<span style="color: #66cc99;">', pilih_provinsi, ' ', "{:.2f}".format(correlation_coefficient), '</span>', unsafe_allow_html=True)

with tab5:
    st.header('Kesimpulan')
    st.markdown('''
    - Riau yang memiliki Lahan terluas secara nominal dan persentase disertai dengan produktivitas tinggi. Tetapi justru menunjukkan korelasi negatif terhadap PDRB. Hal ini mungkin dapat menjadi indikasi bahwa Riau sudah menanam terlalu banyak. Namun masih banyak faktor lain yang perlu dipertimbangkan.
    ''')
    image_path = 'riau.png'
    st.image(image_path, caption='riau', use_column_width=True)

    st.markdown('''
    - Korelasi kuat dan positif pada luas area dan produktivitas ditunjukkan pada provinsi Kalimantan Tengah. Provinsi ini dapat dijadikan pedoman ukuran luas lahan yang optimal dan dapat menjadi studi kasus dalam meningkatkan standar produktivitas.
    ''')
    image_path = 'kalteng.png'
    st.image(image_path, caption='kalteng', use_column_width=True)

    st.markdown('''
    - Pada hasil korelasi area%, terdapat trend bahwa Provinsi dengan persentase luas lahan yang tinggi justru memiliki keadaan ekonomi yang menurun. Sedangkan yang persentasenya cukup tinggi memiliki peningkatan keadaan ekonomi.
    ''')
    image_path = 'area%.png'
    st.image(image_path, caption='area%', use_column_width=False)

    st.markdown('''
    - 10 lahan terkecil juga menempati top 10 persentase terkecil dengan urutan yang berubah.
                ''')
    image_path = 'gambar.png'
    st.image(image_path, caption='gambar', use_column_width=True)








