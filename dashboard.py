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