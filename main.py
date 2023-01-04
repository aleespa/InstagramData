import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import json
from datetime import datetime

initial_date = datetime(2018, 1, 1)
final_date = datetime(2022, 6, 30)
total_time_series = pd.DataFrame(index=pd.date_range(initial_date, final_date))
n_window = 45

f = open('data/likes/liked_posts.json')
likes = json.load(f)
likes_list = likes['likes_media_likes']
time_series = pd.DataFrame()
for j in range(len(likes_list)):
    dt_object = datetime.fromtimestamp(likes_list[j]['string_list_data'][0]['timestamp'])
    time_series.loc[j, 'Date'] = dt_object.date()
    time_series.loc[j, 'Likes'] = 1

for date_reference in total_time_series.index:
    window_left = date_reference.date() - pd.Timedelta(n_window, 'days')
    window_right = date_reference.date()
    window = (time_series['Date'] > window_left) & (time_series['Date'] <= window_right)
    total_time_series.loc[date_reference, 'Likes'] = float(time_series[window]['Likes'].sum() / n_window)

f = open('data/content/posts_1.json')
posts = json.load(f)

time_series = pd.DataFrame()
for j in range(len(posts)):
    dt_object = datetime.fromtimestamp(posts[j]['media'][0]['creation_timestamp'])
    time_series.loc[j, 'Date'] = dt_object.date()
    time_series.loc[j, 'Posts'] = 1

for date_reference in total_time_series.index:
    window_left = date_reference.date() - pd.Timedelta(n_window, 'days')
    window_right = date_reference.date()
    window = (time_series['Date'] > window_left) & (time_series['Date'] <= window_right)
    total_time_series.loc[date_reference, 'Posts'] = float(time_series[window]['Posts'].sum() / n_window)

f = open('data/content/stories.json')
stories = json.load(f)
stories_list = stories['ig_stories']

time_series = pd.DataFrame()
for j in range(len(stories_list)):
    dt_object = datetime.fromtimestamp(stories_list[j]['creation_timestamp'])
    time_series.loc[j, 'Date'] = dt_object.date()
    time_series.loc[j, 'Stories'] = 1
#
# for date_reference in total_time_series.index:
#     window_left = date_reference.date() - pd.Timedelta(n_window, 'days')
#     window_right = date_reference.date()
#     window = (time_series['Date'] > window_left) & (time_series['Date'] <= window_right)
#     total_time_series.loc[date_reference, 'Stories'] = float(time_series[window]['Stories'].sum() / n_window)
#
# plt.figure(figsize=(12, 6), dpi=200)
# plt.plot(total_time_series.index, total_time_series['Likes'], color='#405DE6', label='Likes')
# plt.fill_between(total_time_series.index, total_time_series['Likes'], alpha=0.1, color='#405DE6')
#
# plt.plot(total_time_series.index, total_time_series['Stories'], color='#C13584', label='Stories')
# plt.fill_between(total_time_series.index, total_time_series['Stories'], alpha=0.1, color='#C13584')
#
# plt.plot(total_time_series.index, total_time_series['Posts'], color='#FD1D1D', label='Posts')
# plt.fill_between(total_time_series.index, total_time_series['Posts'], alpha=0.1, color='#FD1D1D')
#
# plt.legend(ncol=3, frameon=False, title='Daily average, last 45 days', loc=(0.3, -0.2))
# plt.xlim(datetime(2018, 1, 1), datetime(2022, 6, 30))
# plt.ylim(0, 7.1)
# plt.grid(axis='y', alpha=0.2)
# plt.box(False)
# plt.tight_layout()
# plt.savefig('outputs/figure1.png')

idx = pd.IndexSlice
monthly_data = time_series.groupby([pd.to_datetime(time_series.Date).dt.year,
                                    pd.to_datetime(time_series.Date).dt.month])[['Stories']].sum()
monthly_data.loc[(2022, 7), 'Stories'] = 28
monthly_data.loc[(2022, 8), 'Stories'] = 33
monthly_data.loc[(2022, 9), 'Stories'] = 15
monthly_data.loc[(2022, 10), 'Stories'] = 0
monthly_data.loc[(2022, 11), 'Stories'] = 0
monthly_data.loc[(2022, 12), 'Stories'] = 0
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 15
year_color = {
    2018: '#181692',
    2019: '#006f4e',
    2020: '#d9c405',
    2021: '#1c8887',
    2022: '#c44100'
}
for year in [2018, 2019, 2020, 2021, 2022]:
    months = range(1, 13)
    fig = plt.figure(figsize=(9, 16), dpi=200)
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6])
    ax.text(6, 69+4, 'Number of instagram', fontsize=20, alpha=0.75, color=year_color[year])
    ax.text(6, 66+4, 'stories per month', fontsize=20, alpha=0.75, color=year_color[year])
    ax.text(1.5, 66+4, f"{year}", fontsize=60, color=year_color[year], alpha=0.8)
    ax.text(4.5, 66, f"@aleespa", fontsize=26, color='k', alpha=0.7)

    ax.bar(months, monthly_data.loc[(year, slice(None)), 'Stories'].to_numpy(), zorder=2, alpha=0.85,
           color=[plt.cm.winter(i / 4) for i in range(2, 4)] +
                 [plt.cm.spring(i / 4) for i in range(4)] +
                 [plt.cm.summer_r(i / 4) for i in range(4)] +
                 [plt.cm.winter(i / 4) for i in range(2)])
    ax.set_xticks(months, months)
    ax.set_yticks([10, 20, 30, 40, 50, 60], [10, 20, 30, 40, 50, 60])
    ax.set_ylim(0, 65)
    ax.set_xlabel('Month')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)
    ax.grid(alpha=0.3, zorder=1)
    fig.savefig(f'outputs/Monthly_plot_{year}.png')
