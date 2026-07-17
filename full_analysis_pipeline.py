import pandas as pd
import numpy as np

pd.set_option('display.width', 140)

trades = pd.read_csv('/mnt/user-data/uploads/historical_data.csv')
fg = pd.read_csv('/mnt/user-data/uploads/fear_greed_index.csv')

# Parse dates
trades['Timestamp IST'] = pd.to_datetime(trades['Timestamp IST'], format='%d-%m-%Y %H:%M')
trades['date'] = trades['Timestamp IST'].dt.date
fg['date'] = pd.to_datetime(fg['date']).dt.date

# Merge
merged = trades.merge(fg[['date','value','classification']], on='date', how='left')
print("Unmatched rows:", merged['classification'].isna().sum(), "of", len(merged))
merged.to_pickle('/home/claude/merged.pkl')
print(merged['classification'].value_counts(dropna=False))
print(merged[['date']].drop_duplicates().shape)
print(fg['date'].min(), fg['date'].max())
print(trades['date'].min(), trades['date'].max())
import pandas as pd
import numpy as np

merged = pd.read_pickle('/home/claude/merged.pkl')
merged = merged.dropna(subset=['classification'])

# Order for plotting
order = ['Extreme Fear','Fear','Neutral','Greed','Extreme Greed']
merged['classification'] = pd.Categorical(merged['classification'], categories=order, ordered=True)

# Only consider actual closing/realizing trades for PnL-based win rate (nonzero PnL)
closed = merged[merged['Closed PnL'] != 0]

summary = merged.groupby('classification', observed=True).agg(
    trades=('Closed PnL','count'),
    unique_traders=('Account','nunique'),
    total_volume_usd=('Size USD','sum'),
    avg_trade_size_usd=('Size USD','mean'),
    total_pnl=('Closed PnL','sum'),
).reset_index()

winrate = closed.groupby('classification', observed=True).apply(
    lambda g: (g['Closed PnL']>0).mean(), include_groups=False
).reset_index(name='win_rate')

avg_pnl_per_closed = closed.groupby('classification', observed=True)['Closed PnL'].mean().reset_index(name='avg_pnl_per_closed_trade')

summary = summary.merge(winrate, on='classification').merge(avg_pnl_per_closed, on='classification')
summary['pnl_per_1000usd_volume'] = summary['total_pnl'] / (summary['total_volume_usd']/1000)

print(summary.to_string(index=False))
summary.to_csv('/home/claude/summary_by_sentiment.csv', index=False)

# Daily aggregation for time series / correlation
daily = merged.groupby('date').agg(
    daily_pnl=('Closed PnL','sum'),
    daily_volume=('Size USD','sum'),
    daily_trades=('Closed PnL','count'),
    sentiment_value=('value','mean')
).reset_index()
daily.to_csv('/home/claude/daily.csv', index=False)
print("\nCorrelation (sentiment value vs daily PnL):", daily['sentiment_value'].corr(daily['daily_pnl']))
print("Correlation (sentiment value vs daily volume):", daily['sentiment_value'].corr(daily['daily_volume']))
print("Correlation (sentiment value vs daily trade count):", daily['sentiment_value'].corr(daily['daily_trades']))

# Per-trader behavior: does an individual trader's win rate change with sentiment?
trader_sent = closed.groupby(['Account','classification'], observed=True)['Closed PnL'].agg(['mean','count']).reset_index()
print("\nSample size check - trader x sentiment rows:", len(trader_sent))
import pandas as pd
import numpy as np

merged = pd.read_pickle('/home/claude/merged.pkl')
merged = merged.dropna(subset=['classification'])
order = ['Extreme Fear','Fear','Neutral','Greed','Extreme Greed']
merged['classification'] = pd.Categorical(merged['classification'], categories=order, ordered=True)

# Long vs short behavior by sentiment (using Side as proxy: BUY vs SELL)
side_mix = merged.groupby(['classification','Side'], observed=True).size().unstack(fill_value=0)
side_mix_pct = side_mix.div(side_mix.sum(axis=1), axis=0) * 100
print("BUY/SELL mix by sentiment (%):")
print(side_mix_pct.round(1))

# Top coins by volume overall
top_coins = merged.groupby('Coin', observed=True)['Size USD'].sum().sort_values(ascending=False).head(8)
print("\nTop 8 coins by volume:")
print(top_coins)

# Leverage proxy: average size per trade relative to account activity isn't available directly;
# check "Start Position" magnitude as proxy for position sizing conviction
pos_size = merged.groupby('classification', observed=True)['Start Position'].apply(lambda x: x.abs().mean())
print("\nAvg abs Start Position by sentiment:")
print(pos_size)
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.labelcolor'] = '#222222'
plt.rcParams['text.color'] = '#222222'
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'

order = ['Extreme Fear','Fear','Neutral','Greed','Extreme Greed']
colors = ['#b91c1c','#f97316','#9ca3af','#65a30d','#15803d']  # deep red -> orange -> gray -> green -> deep green

summary = pd.read_csv('/home/claude/summary_by_sentiment.csv')
summary['classification'] = pd.Categorical(summary['classification'], categories=order, ordered=True)
summary = summary.sort_values('classification')

daily = pd.read_csv('/home/claude/daily.csv')
daily['date'] = pd.to_datetime(daily['date'])
daily = daily.sort_values('date')

# --- Chart 1: Win rate by sentiment ---
fig, ax = plt.subplots(figsize=(7,4.2), dpi=200)
bars = ax.bar(summary['classification'], summary['win_rate']*100, color=colors, width=0.62)
for b, v in zip(bars, summary['win_rate']*100):
    ax.text(b.get_x()+b.get_width()/2, v+1.2, f"{v:.1f}%", ha='center', fontsize=10, fontweight='bold', color='#222')
ax.set_ylim(0, 100)
ax.set_ylabel('Win rate (% of closed trades with profit)')
ax.set_title('Trader Win Rate by Market Sentiment', fontsize=13, fontweight='bold', pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
plt.tight_layout()
plt.savefig('/home/claude/charts/chart1_winrate.png', facecolor='white')
plt.close()

# --- Chart 2: Profitability efficiency (PnL per $1000 traded) ---
fig, ax = plt.subplots(figsize=(7,4.2), dpi=200)
bars = ax.bar(summary['classification'], summary['pnl_per_1000usd_volume'], color=colors, width=0.62)
for b, v in zip(bars, summary['pnl_per_1000usd_volume']):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f"${v:.2f}", ha='center', fontsize=10, fontweight='bold', color='#222')
ax.set_ylabel('Net PnL per $1,000 traded (USD)')
ax.set_title('Profitability Efficiency by Market Sentiment', fontsize=13, fontweight='bold', pad=14)
plt.tight_layout()
plt.savefig('/home/claude/charts/chart2_efficiency.png', facecolor='white')
plt.close()

# --- Chart 3: Trading activity (volume) by sentiment ---
fig, ax = plt.subplots(figsize=(7,4.2), dpi=200)
vol_m = summary['total_volume_usd']/1e6
bars = ax.bar(summary['classification'], vol_m, color=colors, width=0.62)
for b, v in zip(bars, vol_m):
    ax.text(b.get_x()+b.get_width()/2, v+5, f"${v:.0f}M", ha='center', fontsize=10, fontweight='bold', color='#222')
ax.set_ylabel('Total trading volume (USD, millions)')
ax.set_title('Trading Activity by Market Sentiment', fontsize=13, fontweight='bold', pad=14)
plt.tight_layout()
plt.savefig('/home/claude/charts/chart3_volume.png', facecolor='white')
plt.close()

# --- Chart 4: Daily sentiment value vs daily PnL (dual axis time series) ---
fig, ax1 = plt.subplots(figsize=(9,4.5), dpi=200)
ax1.plot(daily['date'], daily['sentiment_value'], color='#6b7280', linewidth=1.1, label='Sentiment index (0-100)')
ax1.set_ylabel('Fear & Greed index value', color='#6b7280')
ax1.tick_params(axis='y', labelcolor='#6b7280')
ax1.set_ylim(0,100)

ax2 = ax1.twinx()
roll = daily['daily_pnl'].rolling(14, min_periods=1).mean()
ax2.plot(daily['date'], roll, color='#1d4ed8', linewidth=1.6, label='14-day avg daily PnL (USD)')
ax2.axhline(0, color='#1d4ed8', linewidth=0.6, alpha=0.3)
ax2.set_ylabel('14-day rolling avg daily PnL (USD)', color='#1d4ed8')
ax2.tick_params(axis='y', labelcolor='#1d4ed8')
ax2.spines['right'].set_visible(True)

ax1.set_title('Market Sentiment vs. Trader PnL Over Time', fontsize=13, fontweight='bold', pad=14)
fig.tight_layout()
plt.savefig('/home/claude/charts/chart4_timeseries.png', facecolor='white')
plt.close()

# --- Chart 5: Buy vs Sell mix by sentiment (100% stacked) ---
merged = pd.read_pickle('/home/claude/merged.pkl').dropna(subset=['classification'])
merged['classification'] = pd.Categorical(merged['classification'], categories=order, ordered=True)
side_mix = merged.groupby(['classification','Side'], observed=True).size().unstack(fill_value=0)
side_mix_pct = side_mix.div(side_mix.sum(axis=1), axis=0) * 100
side_mix_pct = side_mix_pct.reindex(order)

fig, ax = plt.subplots(figsize=(7,4.2), dpi=200)
ax.bar(order, side_mix_pct['BUY'], color='#2563eb', label='Buy orders', width=0.55)
ax.bar(order, side_mix_pct['SELL'], bottom=side_mix_pct['BUY'], color='#dc2626', label='Sell orders', width=0.55)
ax.set_ylabel('% of order flow')
ax.set_title('Buy vs. Sell Order Mix by Market Sentiment', fontsize=13, fontweight='bold', pad=14)
ax.axhline(50, color='white', linewidth=1, linestyle='--', alpha=0.6)
ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)
plt.tight_layout()
plt.savefig('/home/claude/charts/chart5_buysell.png', facecolor='white')
plt.close()

print("charts done")
