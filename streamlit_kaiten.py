import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
import datetime
from itertools import product
import plotly.express as px

import warnings
warnings.simplefilter('ignore')
import streamlit as st

st.title('都心23区における業種別の　　　　　　開店閉店年次別比較グラフ')

df_jp_ind = pd.read_csv('df_tokyo_new2.csv')

# 都心23区の開店閉店の推移を表示

df_jp_ind_open = df_jp_ind[(df_jp_ind['status']=='開店')]
df_jp_ind_close = df_jp_ind[(df_jp_ind['status']=='閉店')]

lst_industry_type = df_jp_ind['industry_type'].unique()

# 日付データに変換
df_jp_ind['open_close_day_fixed'] = pd.to_datetime(df_jp_ind['open_close_day_fixed'])
df_jp_ind['year'] = df_jp_ind['open_close_day_fixed'].dt.year
lst_year = range(df_jp_ind['year'].min(), df_jp_ind['year'].max())

df_template = pd.DataFrame(list(product(lst_year, lst_industry_type)), columns=['year', 'industry_type'])

# テンプレートとマージ
result = df_template.merge(df_jp_ind.groupby([df_jp_ind['year'], 'industry_type']).size().reset_index(name='count'),
                           on=['year', 'industry_type'], how='left').fillna(0)

# 開店数をカテゴリー/年別でリスト化
lst_industry_type_open = df_jp_ind_open['industry_type'].unique()

# 日付データに変換
df_jp_ind_open['open_close_day_fixed'] = pd.to_datetime(df_jp_ind_open['open_close_day_fixed'])
df_jp_ind_open['year'] = df_jp_ind_open['open_close_day_fixed'].dt.year
lst_year_open = range(df_jp_ind_open['year'].min(), df_jp_ind_open['year'].max())

df_template = pd.DataFrame(list(product(lst_year_open, lst_industry_type_open)), columns=['year', 'industry_type'])

# テンプレートとマージ
result_open = df_template.merge(df_jp_ind_open.groupby([df_jp_ind_open['year'], 'industry_type']).size().reset_index(name='count'),
                           on=['year', 'industry_type'], how='left').fillna(0)

# 閉店数をカテゴリー/年別でリスト化
lst_industry_type_close = df_jp_ind_close['industry_type'].unique()

# 日付データに変換
df_jp_ind_close['open_close_day_fixed'] = pd.to_datetime(df_jp_ind_close['open_close_day_fixed'])
df_jp_ind_close['year'] = df_jp_ind_close['open_close_day_fixed'].dt.year
lst_year_close = range(df_jp_ind_close['year'].min(), df_jp_ind_close['year'].max())

df_template = pd.DataFrame(list(product(lst_year_close, lst_industry_type_close)), columns=['year', 'industry_type'])

# テンプレートとマージ
result_close = df_template.merge(df_jp_ind_close.groupby([df_jp_ind_close['year'], 'industry_type']).size().reset_index(name='count'),
                           on=['year', 'industry_type'], how='left').fillna(0)


# カテゴリーごとのセレクトボックスを作成
pref_list = result_open['industry_type'].unique()

option_pref = st.selectbox(
    '業種カテゴリー',
    (pref_list))
result_open = result_open[result_open['industry_type']==option_pref]
result_close = result_close[result_close['industry_type']==option_pref]

df_line = pd.merge(result_open,result_close,on='year')

df_line = df_line[['year','count_x','count_y']]

df_line = df_line.set_index('year')

# df_lineのカラム名を変更。ｃｏｕｎｔ_xを「開店数」、ｃｏｕｎｔ_yを「閉店数」に変更
df_line.columns = ['開店数','閉店数']

st.line_chart(df_line)


st.title('2019年渋谷と墨田区の業種別の　開店比較グラフ')
# リスト化
lst_ku = df_jp_ind['address_ku'].unique()
lst_year = range(df_jp_ind['year'].min(), df_jp_ind['year'].max())
lst_ind = df_jp_ind['industry_type'].unique()
df_jp_ind['status'] = df_jp_ind['status'].replace('休業', '閉店')
lst_status = df_jp_ind['status'].unique()
df_template = pd.DataFrame(list(product(lst_year, lst_ku, lst_status,lst_ind)), columns=['year', 'address_ku', 'status','industry_type'])

df_template = df_template.merge(df_jp_ind.groupby([df_jp_ind['year'], 'address_ku', 'status','industry_type']).size().reset_index(name='count'),
                          on=['year', 'address_ku', 'status','industry_type'], how='left').fillna(0)

# df_templateの「year=2019」かつ「address_ku=渋谷区」かつ「status=開店」のデータを抽出し、df_template_shibuyaに代入
df_template_shibuya = df_template[(df_template['year']==2019) & (df_template['address_ku']=='渋谷区') & (df_template['status']=='開店')]
df_template_shibuya = df_template_shibuya[['industry_type','count']]

# 墨田区のデータを抽出
df_template_sumida = df_template[(df_template['year']==2018) & (df_template['address_ku']=='墨田区') & (df_template['status']=='開店')]
df_template_sumida = df_template_sumida[['industry_type','count']]

# df_template_shibuya　と　df_template_sumida　をマージ
df_template_shibuya_sumida = pd.merge(df_template_shibuya,df_template_sumida,on='industry_type')

# df_template_shibuya_sumidaのカラム名を変更。ｃｏｕｎｔ_xを「渋谷区」、ｃｏｕｎｔ_yを「墨田区」に変更
df_template_shibuya_sumida.columns = ['industry_type','渋谷区','墨田区']

# df_template_shibuya_sumidaの「渋谷区」と「墨田区」を比率に変換
df_template_shibuya_sumida['渋谷区'] = df_template_shibuya_sumida['渋谷区'] / df_template_shibuya_sumida['渋谷区'].sum()

# df_template_shibuya_sumidaの「渋谷区」と「墨田区」をそれぞれを円グラフに変換
fig = px.pie(df_template_shibuya_sumida, values='渋谷区', names='industry_type', title='　　　　　 　　　　2019年渋谷区の業種別開店数')
fig2 = px.pie(df_template_shibuya_sumida, values='墨田区', names='industry_type', title='　　　　　 　　　　2019年墨田区の業種別開店数')

# figとfig2を並べて表示
st.plotly_chart(fig)
st.plotly_chart(fig2)

# 産業別推移グラフ
st.title('産業別推移グラフ')
# status=開店、x=year、y=count、color=industry_typeでindustryごとの推移グラフを作成し、df_template_oresenに代入
df_template_oresen = px.bar(df_template[(df_template['status']=='開店')],
                x='year',
                y='count',
                color='industry_type',
                title='　　　　　 　　　　2010～2022年業種別合計の業種別開店数')

                            
# df_template_oresenを表示 
st.plotly_chart(df_template_oresen)

# status=閉店、x=year、y=count、color=industry_typeでindustryごとの推移グラフを作成し、df_template_oresenに代入
df_template_oresen2 = px.bar(df_template[(df_template['status']=='閉店')],
                x='year',
                y='count',
                color='industry_type',
                title='　　　　　 　　　　2010～2022年業種別合計の業種別閉店数')

st.plotly_chart(df_template_oresen2)

st.title('2020年渋谷と墨田区の業種別の閉店比較グラフ') 
# df_templateの「year=2020」かつ「address_ku=渋谷区」かつ「status=閉店」のデータを抽出し、df_template_shibuyaに代入
df_template_shibuya2 = df_template[(df_template['year']==2020) & (df_template['address_ku']=='渋谷区') & (df_template['status']=='閉店')]
df_template_shibuya2 = df_template_shibuya2[['industry_type','count']]

# 墨田区のデータを抽出
df_template_sumida2 = df_template[(df_template['year']==2020) & (df_template['address_ku']=='墨田区') & (df_template['status']=='閉店')]
df_template_sumida2 = df_template_sumida2[['industry_type','count']]

# df_template_shibuya　と　df_template_sumida　をマージ
df_template_shibuya_sumida2 = pd.merge(df_template_shibuya2,df_template_sumida2,on='industry_type')

# df_template_shibuya_sumidaのカラム名を変更。ｃｏｕｎｔ_xを「渋谷区」、ｃｏｕｎｔ_yを「墨田区」に変更
df_template_shibuya_sumida2.columns = ['industry_type','渋谷区','墨田区']

# df_template_shibuya_sumidaの「渋谷区」と「墨田区」を比率に変換
df_template_shibuya_sumida2['渋谷区'] = df_template_shibuya_sumida2['渋谷区'] / df_template_shibuya_sumida2['渋谷区'].sum()

# df_template_shibuya_sumidaの「渋谷区」と「墨田区」をそれぞれを円グラフに変換
fig3 = px.pie(df_template_shibuya_sumida2, values='渋谷区', names='industry_type', title='　　　　　 　　　　2020年渋谷区の業種別閉店数')
fig4 = px.pie(df_template_shibuya_sumida2, values='墨田区', names='industry_type', title='　　　　　 　　　　2020年墨田区の業種別閉店数')

# fig3とfig4を並べて表示
st.plotly_chart(fig3)
st.plotly_chart(fig4)


st.title('豊島区と23区全体の業種比較グラフ') 

# 開店グラフ
# df_templateから「address=豊島区」かつ「status=開店」をdf_template_toshimaに代入
df_template_toshima = df_template[(df_template['address_ku']=='豊島区') & (df_template['status']=='開店')]

#  df_template_toshimaをcsvファイルに出力
df_template_toshima.to_csv('df_template_toshima.csv')

# df_template_toshimaの「industry_type」ごとに「count」を合計し、リスト化して、df_template_toshima_countに代入
df_template_toshima_count = df_template_toshima.groupby('industry_type').sum().reset_index()

# df_template_toshima_countの「year」を削除
df_template_toshima_count = df_template_toshima_count.drop('year',axis=1)

# df_templateの「industry_type」ごとに「count」を合計し、リスト化して、df_template_countに代入
df_template_count = df_template.groupby('industry_type').sum().reset_index()

# df_template_countの「year」を削除
df_template__count = df_template_count.drop('year',axis=1)

# df_template_toshima　と　df_template_count　をマージ
df_template_toshima_count_all = pd.merge(df_template_toshima_count,df_template__count,on='industry_type')

# df_template_toshima_count_allのカラム名を変更。ｃｏｕｎｔ_xを「豊島区」、ｃｏｕｎｔ_yを「23区全体」に変更
df_template_toshima_count_all.columns = ['industry_type','豊島区','23区全体']

# df_template_toshima_count_allの「豊島区」と「23区全体」を比率に変換
df_template_toshima_count_all['豊島区'] = df_template_toshima_count_all['豊島区'] / df_template_toshima_count_all['豊島区'].sum()

# df_template_toshima_count_allの23区全体合計を｢1」として、比率に変換
df_template_toshima_count_all['23区全体'] = df_template_toshima_count_all['23区全体'] / df_template_toshima_count_all['23区全体'].sum()

# df_template_toshima_count_allの「industry_type」ごとに「豊島区」と「23区全体」を比較したグラフを作成
fig5 = px.bar(df_template_toshima_count_all, x='industry_type', y=['豊島区','23区全体'], barmode='group', title='　　　　　 　　　　2010～2022年業種別合計の豊島区と23区全体の業種別開店数')

# fig5を表示
st.plotly_chart(fig5)

# 閉店グラフ
# df_templateから「address=豊島区」かつ「status=閉店」をdf_template_toshimaに代入
df_template_toshima2 = df_template[(df_template['address_ku']=='豊島区') & (df_template['status']=='閉店')]

# df_template_toshimaの「industry_type」ごとに「count」を合計し、リスト化して、df_template_toshima_countに代入
df_template_toshima_count2 = df_template_toshima2.groupby('industry_type').sum().reset_index()

# df_template_toshima_countの「year」を削除
df_template_toshima_count2 = df_template_toshima_count2.drop('year',axis=1)

# df_template_toshima2　と　df_template_count　をマージ
df_template_toshima_count_all2 = pd.merge(df_template_toshima_count2,df_template__count,on='industry_type')

# df_template_toshima_count_all2のカラム名を変更。ｃｏｕｎｔ_xを「豊島区」、ｃｏｕｎｔ_yを「23区全体」に変更
df_template_toshima_count_all2.columns = ['industry_type','豊島区','23区全体']

# df_template_toshima_count_all2の「豊島区」と「23区全体」を比率に変換
df_template_toshima_count_all2['豊島区'] = df_template_toshima_count_all2['豊島区'] / df_template_toshima_count_all2['豊島区'].sum()

# df_template_toshima_count_all2の23区全体合計を｢1」として、比率に変換
df_template_toshima_count_all2['23区全体'] = df_template_toshima_count_all2['23区全体'] / df_template_toshima_count_all2['23区全体'].sum()

# df_template_toshima_count_all2の「industry_type」ごとに「豊島区」と「23区全体」を比較したグラフを作成
fig6 = px.bar(df_template_toshima_count_all2, x='industry_type', y=['豊島区','23区全体'], barmode='group', title='　　　　　 　　　　2010～2022年業種別合計の豊島区と23区全体の業種別閉店数')

# fig5を表示
st.plotly_chart(fig6)

st.title('世田谷区の業種推移グラフ')
# df_templateから「address=世田谷区」をdf_template_setagayaに代入
df_template_setagaya = df_template[(df_template['address_ku']=='世田谷区')]

# df_templateのstatusをselectboxで選択
status_list = df_template_setagaya ['status'].unique()
option_status = st.selectbox(
    'status',
    (status_list))

df_template_graph = df_template_setagaya[(df_template_setagaya['status']==option_status)]

max_x = df_template_graph["count"].max()+50

# df_temple_graphの「industry_type」ごとに「count」をplotly_chartで表示し、「year」ごとにアニメーション。
fig7 = px.bar(df_template_graph,
                x='count',
                y='industry_type',
                color='industry_type',
                animation_frame='year',
                range_x=[0, max_x],
                title='　　　　　 　　　　2010～2022年業種別合計の業種別開店数')

# figを表示
st.plotly_chart(fig7)
