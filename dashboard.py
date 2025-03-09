import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
import zipfile

zip = zipfile.ZipFile('air.zip','r')
zip.extractall('air')
zip.close()

guanyuan_dir = 'air/AirDataset/Guanyuan.csv'
nongzhanguan_dir = 'air/AirDataset/Nongzhanguan.csv'

guan_df = pd.read_csv(guanyuan_dir)
nong_df = pd.read_csv(nongzhanguan_dir)

guan_df['date'] = pd.to_datetime(guan_df[['year', 'month', 'day', 'hour']])
nong_df['date'] = pd.to_datetime(nong_df[['year', 'month', 'day', 'hour']])

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


fusion = pd.merge(guan_df, nong_df, on=['year', 'month', 'day', 'hour'], suffixes=('_guanyuan', '_nongzhanguan'))
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

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