"""
===============================================================
  Customer Segmentation using RFM Analysis
  SyntecxHub Internship - Project 1
===============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────
# STEP 1: Generate / Load Transactional Data
# ──────────────────────────────────────────────
np.random.seed(42)

# Simulate 500 customers, 2000 transactions over 2 years
n_customers = 500
n_transactions = 2000
analysis_date = datetime(2024, 12, 31)

customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, n_customers + 1)]

# Assign customer "types" to make segmentation realistic
customer_types = np.random.choice(['loyal', 'churn_risk', 'new', 'regular'],
                                   size=n_customers,
                                   p=[0.20, 0.25, 0.25, 0.30])

records = []
for cid, ctype in zip(customer_ids, customer_types):
    if ctype == 'loyal':
        num_orders = np.random.randint(8, 20)
        days_since_last = np.random.randint(1, 30)
        spend_range = (150, 500)
    elif ctype == 'churn_risk':
        num_orders = np.random.randint(2, 6)
        days_since_last = np.random.randint(120, 365)
        spend_range = (50, 200)
    elif ctype == 'new':
        num_orders = np.random.randint(1, 3)
        days_since_last = np.random.randint(1, 60)
        spend_range = (30, 150)
    else:  # regular
        num_orders = np.random.randint(3, 8)
        days_since_last = np.random.randint(30, 120)
        spend_range = (80, 300)

    for _ in range(num_orders):
        days_ago = np.random.randint(days_since_last, days_since_last + 200)
        order_date = analysis_date - timedelta(days=int(days_ago))
        amount = round(np.random.uniform(*spend_range), 2)
        records.append({
            'CustomerID': cid,
            'OrderDate': order_date,
            'Amount': amount
        })

df = pd.DataFrame(records)
print(f"✅ Dataset created: {len(df)} transactions, {df['CustomerID'].nunique()} customers")
print(df.head())

# ──────────────────────────────────────────────
# STEP 2: Clean & Prepare Data
# ──────────────────────────────────────────────
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.dropna()
df = df[df['Amount'] > 0]  # remove zero/negative amounts
df = df[df['OrderDate'] <= analysis_date]  # remove future dates

print(f"\n✅ After cleaning: {len(df)} valid transactions")

# ──────────────────────────────────────────────
# STEP 3: Calculate RFM Metrics
# ──────────────────────────────────────────────
rfm = df.groupby('CustomerID').agg(
    Recency   = ('OrderDate', lambda x: (analysis_date - x.max()).days),
    Frequency = ('OrderDate', 'count'),
    Monetary  = ('Amount', 'sum')
).reset_index()

rfm['Monetary'] = rfm['Monetary'].round(2)
print("\n📊 RFM Summary Statistics:")
print(rfm[['Recency', 'Frequency', 'Monetary']].describe().round(2))

# ──────────────────────────────────────────────
# STEP 4: Score Each RFM Dimension (1–5)
# ──────────────────────────────────────────────
# Recency: lower days = better = higher score
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
# Frequency: higher = better
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
# Monetary: higher = better
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)

rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

# ──────────────────────────────────────────────
# STEP 5: Segment Customers
# ──────────────────────────────────────────────
def segment_customer(row):
    r, f, m, total = row['R_Score'], row['F_Score'], row['M_Score'], row['RFM_Score']
    if total >= 12 and r >= 4:
        return 'Loyal'
    elif r <= 2 and total <= 7:
        return 'Churn Risk'
    elif r >= 4 and f <= 2:
        return 'New Customer'
    elif total >= 9:
        return 'Promising'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    else:
        return 'Regular'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print("\n👥 Customer Segment Distribution:")
seg_counts = rfm['Segment'].value_counts()
print(seg_counts.to_string())

# ──────────────────────────────────────────────
# STEP 6: Analyze Behavior Per Segment
# ──────────────────────────────────────────────
seg_profile = rfm.groupby('Segment').agg(
    Customers  = ('CustomerID', 'count'),
    Avg_Recency= ('Recency', 'mean'),
    Avg_Frequency=('Frequency','mean'),
    Avg_Monetary =('Monetary','mean'),
    Total_Revenue=('Monetary','sum')
).round(2).sort_values('Total_Revenue', ascending=False)

print("\n📋 Segment Profiles:")
print(seg_profile.to_string())

# ──────────────────────────────────────────────
# STEP 7: Marketing Recommendations
# ──────────────────────────────────────────────
recommendations = {
    'Loyal':        '🏆 VIP rewards, early access to new products, personalized thank-you offers',
    'Promising':    '🌟 Loyalty program invites, upsell campaigns, targeted discounts',
    'New Customer': '👋 Onboarding series, welcome discount, product education content',
    'Regular':      '📧 Regular newsletters, cross-sell recommendations, seasonal deals',
    'At Risk':      '⚠️  Win-back email sequence, special discount, feedback survey',
    'Churn Risk':   '🆘 Urgent retention offer (30–50% off), personal outreach, exit survey'
}

print("\n🎯 Targeted Marketing Recommendations:")
for seg, rec in recommendations.items():
    count = seg_counts.get(seg, 0)
    print(f"  {seg} ({count} customers): {rec}")

# ──────────────────────────────────────────────
# STEP 8: Visualizations  (4-panel dashboard)
# ──────────────────────────────────────────────
COLORS = {
    'Loyal':        '#6B48FF',
    'Promising':    '#9B72FF',
    'New Customer': '#4CAF50',
    'Regular':      '#2196F3',
    'At Risk':      '#FF9800',
    'Churn Risk':   '#F44336'
}
palette = [COLORS.get(s, '#999') for s in seg_counts.index]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Customer Segmentation Dashboard\nRFM Analysis — SyntecxHub Project 1',
             fontsize=18, fontweight='bold', y=0.98, color='#2D2D6B')
fig.patch.set_facecolor('#F5F3FF')
for ax in axes.flat:
    ax.set_facecolor('#FAFAFE')

# ── Chart 1: Segment Distribution (Pie) ──
ax1 = axes[0, 0]
wedges, texts, autotexts = ax1.pie(
    seg_counts.values,
    labels=seg_counts.index,
    colors=[COLORS.get(s, '#999') for s in seg_counts.index],
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.8,
    wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2)
)
for at in autotexts:
    at.set_fontsize(9); at.set_color('white'); at.set_fontweight('bold')
ax1.set_title('Customer Segment Distribution', fontweight='bold', pad=15)

# ── Chart 2: Revenue by Segment (Bar) ──
ax2 = axes[0, 1]
bar_colors = [COLORS.get(s, '#999') for s in seg_profile.index]
bars = ax2.barh(seg_profile.index, seg_profile['Total_Revenue'],
                color=bar_colors, edgecolor='white', linewidth=1.5)
ax2.set_xlabel('Total Revenue ($)', fontsize=10)
ax2.set_title('Total Revenue by Segment', fontweight='bold', pad=15)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars, seg_profile['Total_Revenue']):
    ax2.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
             f'${val:,.0f}', va='center', fontsize=8)
ax2.set_xlim(0, seg_profile['Total_Revenue'].max() * 1.2)
ax2.invert_yaxis()

# ── Chart 3: RFM Score Distribution (Box) ──
ax3 = axes[1, 0]
seg_order = ['Loyal', 'Promising', 'Regular', 'New Customer', 'At Risk', 'Churn Risk']
seg_order = [s for s in seg_order if s in rfm['Segment'].unique()]
rfm_plot = rfm[rfm['Segment'].isin(seg_order)]
box_colors = [COLORS[s] for s in seg_order]

bp = ax3.boxplot(
    [rfm_plot[rfm_plot['Segment']==s]['RFM_Score'].values for s in seg_order],
    labels=seg_order, patch_artist=True, notch=False
)
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color); patch.set_alpha(0.7)
for median in bp['medians']:
    median.set_color('white'); median.set_linewidth(2)
ax3.set_xlabel('Customer Segment', fontsize=10)
ax3.set_ylabel('RFM Score (3–15)', fontsize=10)
ax3.set_title('RFM Score Distribution by Segment', fontweight='bold', pad=15)
ax3.tick_params(axis='x', rotation=20)

# ── Chart 4: Recency vs Monetary scatter ──
ax4 = axes[1, 1]
for seg in rfm['Segment'].unique():
    sub = rfm[rfm['Segment'] == seg]
    ax4.scatter(sub['Recency'], sub['Monetary'],
                c=COLORS.get(seg, '#999'), label=seg,
                alpha=0.6, s=40, edgecolors='white', linewidths=0.5)
ax4.set_xlabel('Recency (days since last purchase)', fontsize=10)
ax4.set_ylabel('Total Spend ($)', fontsize=10)
ax4.set_title('Recency vs. Monetary Value', fontweight='bold', pad=15)
ax4.legend(title='Segment', fontsize=8, title_fontsize=9,
           loc='upper right', framealpha=0.8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/mnt/user-data/outputs/rfm_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#F5F3FF')
plt.close()
print("\n✅ Dashboard saved!")

# ──────────────────────────────────────────────
# STEP 9: Export Results to CSV
# ──────────────────────────────────────────────
rfm.to_csv('/mnt/user-data/outputs/rfm_results.csv', index=False)
df.to_csv('/mnt/user-data/outputs/transactions.csv', index=False)
print("✅ CSV files saved!")

print("\n🎉 RFM Analysis Complete!")
print(f"   Segments created : {rfm['Segment'].nunique()}")
print(f"   Total customers  : {len(rfm)}")
print(f"   Total revenue    : ${rfm['Monetary'].sum():,.2f}")
