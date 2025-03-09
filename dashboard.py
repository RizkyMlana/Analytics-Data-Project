#import module yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import zipfile

#ekstrak dataset
zip = zipfile.ZipFile('air.zip','r')
zip.extractall('air')
zip.close()

#membaca dataset Guanyuan dan Nongzhanguan
guanyuan_dir = 'air/AirDataset/Guanyuan.csv'
nongzhanguan_dir = 'air/AirDataset/Nongzhanguan.csv'

guan_df = pd.read_csv(guanyuan_dir)
nong_df = pd.read_csv(nongzhanguan_dir)

#Menambahkan variabel date
guan_df['date'] = pd.to_datetime(guan_df[['year', 'month', 'day', 'hour']])
nong_df['date'] = pd.to_datetime(nong_df[['year', 'month', 'day', 'hour']])

#Melakukan cleaning terhadap dataset
guan_df[['PM2.5','PM10','SO2','NO2','CO','O3','RAIN','WSPM']] = guan_df[['PM2.5','PM10','SO2','NO2','CO','O3','RAIN','WSPM']].interpolate()
guan_df['TEMP'] = guan_df['TEMP'].fillna(guan_df['TEMP'].mean())
guan_df['PRES'] = guan_df['PRES'].fillna(guan_df['PRES'].mean())
guan_df['DEWP'] = guan_df['DEWP'].fillna(guan_df['DEWP'].mean())
guan_df['wd'] = guan_df['wd'].bfill()

nong_df[['PM2.5','PM10','SO2','NO2','CO','O3','RAIN','WSPM']] = nong_df[['PM2.5','PM10','SO2','NO2','CO','O3','RAIN','WSPM']].interpolate()
nong_df['TEMP'] = nong_df['TEMP'].fillna(nong_df['TEMP'].mean())
nong_df['PRES'] = nong_df['PRES'].fillna(nong_df['PRES'].mean())
nong_df['DEWP'] = nong_df['DEWP'].fillna(nong_df['DEWP'].mean())
nong_df['wd'] = nong_df['wd'].bfill()

#merge kedua dataset
fusion = pd.merge(guan_df, nong_df, on=['year', 'month', 'day', 'hour'], suffixes=('_guanyuan', '_nongzhanguan'))
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

#Menambahkan variabel baru
def get_season(x):
  if x in [12,1,2]:
    return 'Winter'
  elif x in [3,4,5]:
    return 'Spring'
  elif x in [6,7,8]:
    return 'Summer'
  else:
    return 'Autumn'

fusion['season'] = fusion['month'].apply(get_season)
if 'season' not in fusion.columns:
    fusion['season'] = fusion['season_guanyuan']

#membuat dashboard
st.title("Visualisasi Polusi Udara di Distrik Guanyuan dan Nongzhanguan")

with st.sidebar:
  st.image('bear.jpeg')
  st.markdown("<h2>RizMlana<h2>" ,unsafe_allow_html=True)

#membuat filtering terkait loc, polutan, season
st.sidebar.header("Filter")
loc = st.sidebar.selectbox("Choose Location:", ["Guanyuan", "Nongzhanguan"])
polutan = st.sidebar.selectbox("Choose Polutant:", pollutants)
season = st.sidebar.selectbox("Choose Season:", ["All", "Winter", "Spring", "Summer", "Autumn"])

if season != "All":
    fusion = fusion[fusion["season"] == season]

pollutant_col = f"{polutan}_{loc.lower()}"

st.subheader(f"Statistik {polutan} di {loc}")
st.write(fusion[pollutant_col].describe())

st.subheader(f"Distribusi {polutan} di {loc}")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(fusion[pollutant_col], bins=50, kde=True, color="b", alpha=0.6)
plt.xlabel(f"Konsentrasi {polutan}")
plt.ylabel("Frekuensi")
plt.grid(axis="y", linestyle="--", alpha=0.5)
st.pyplot(fig)

st.subheader(f"Hubungan Kecepatan Angin dengan {polutan}")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=fusion[f"WSPM_{loc.lower()}"], y=fusion[pollutant_col], alpha=0.5)
plt.xlabel("Kecepatan Angin (m/s)")
plt.ylabel(f"Konsentrasi {polutan}")
plt.grid()
st.pyplot(fig)

st.subheader(f"Tren Rata-rata {polutan} Berdasarkan season")

season_avg = fusion.groupby("season")[pollutant_col].mean().reset_index()

season_order = ["Winter", "Spring", "Summer", "Autumn"]
season_avg["season"] = pd.Categorical(season_avg["season"], categories=season_order, ordered=True)

season_palette = {
    "Winter": "#74c2e1",  
    "Spring": "#76c893",  
    "Summer": "#ffdd57",  
    "Autumn": "#ff9f1c",  
}

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y=pollutant_col, data=season_avg, palette=season_palette, ax=ax)
plt.xlabel("season")
plt.ylabel(f"Rata-rata {polutan}")
st.pyplot(fig)

