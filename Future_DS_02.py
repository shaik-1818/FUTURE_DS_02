# ============================================================
#   FUTURE INTERNS — DATA SCIENCE & ANALYTICS
#   Task 2 : Customer Retention & Churn Analysis
#   Repo   : FUTURE_DS_02
#   Dataset: Telco_Churn.xlsx
#   Tools  : Python, Pandas, Matplotlib, Seaborn, ReportLab
# ============================================================

# pip install pandas matplotlib seaborn reportlab openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image, Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')
plt.rcParams['figure.dpi'] = 130
plt.rcParams['font.family'] = 'DejaVu Sans'

# ════════════════════════════════════════════════════════════
# SECTION 1 — LOAD & CLEAN DATA
# ════════════════════════════════════════════════════════════

print("=" * 55)
print("  FUTURE_DS_02 — Customer Retention & Churn Analysis")
print("=" * 55)

df = pd.read_excel('Telco_customer_churn.xlsx')
print(f"\n✅ Dataset loaded   : {df.shape[0]} rows × {df.shape[1]} columns")

# Clean column names
df.columns = df.columns.str.strip()

# Convert Total Charges to numeric
df['Total Charges'] = pd.to_numeric(df['Total Charges'], errors='coerce')
df['Total Charges'].fillna(df['Total Charges'].median(), inplace=True)

# Binary churn column
df['Churned'] = df['Churn Label'].map({'Yes': 1, 'No': 0})

# Tenure buckets
bins   = [0, 12, 24, 36, 48, 60, 72]
labels = ['0–12', '13–24', '25–36', '37–48', '49–60', '61–72']
df['Tenure Group'] = pd.cut(df['Tenure Months'], bins=bins,
                             labels=labels, include_lowest=True)

total_customers = len(df)
churned         = df['Churned'].sum()
retained        = total_customers - churned
churn_rate      = churned / total_customers * 100
retention_rate  = 100 - churn_rate
avg_tenure      = df['Tenure Months'].mean()
avg_monthly     = df['Monthly Charges'].mean()
avg_cltv        = df['CLTV'].mean()
churned_tenure  = df[df['Churned']==1]['Tenure Months'].mean()
retained_tenure = df[df['Churned']==0]['Tenure Months'].mean()

print(f"\n{'─'*55}")
print(f"  OVERALL CHURN SUMMARY")
print(f"{'─'*55}")
print(f"  Total Customers   : {total_customers:,}")
print(f"  Churned           : {churned:,}  ({churn_rate:.1f}%)")
print(f"  Retained          : {retained:,}  ({retention_rate:.1f}%)")
print(f"  Avg Tenure        : {avg_tenure:.1f} months")
print(f"  Avg Monthly Charge: ${avg_monthly:.2f}")
print(f"  Avg CLTV          : ${avg_cltv:,.0f}")
print(f"  Churned Avg Tenure: {churned_tenure:.1f} months")
print(f"  Retained Avg Tenure:{retained_tenure:.1f} months")
print(f"{'─'*55}\n")


# ════════════════════════════════════════════════════════════
# SECTION 2 — KPI DASHBOARD
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 5, figsize=(22, 3))
fig.patch.set_facecolor('#1e1e2e')

kpis = [
    ('Total Customers', f'{total_customers:,}',      '#4361ee'),
    ('Churn Rate',      f'{churn_rate:.1f}%',         '#f72585'),
    ('Retention Rate',  f'{retention_rate:.1f}%',     '#2dc653'),
    ('Avg Tenure',      f'{avg_tenure:.1f} mo',       '#f8961e'),
    ('Avg CLTV',        f'${avg_cltv/1e3:.1f}K',     '#7b2d8b'),
]
for ax, (title, value, color) in zip(axes, kpis):
    ax.set_facecolor(color)
    ax.text(0.5, 0.58, value, ha='center', va='center',
            fontsize=22, fontweight='bold', color='white',
            transform=ax.transAxes)
    ax.text(0.5, 0.22, title, ha='center', va='center',
            fontsize=10, color='#ffffffcc', transform=ax.transAxes)
    ax.axis('off')

plt.suptitle('📊 Churn & Retention KPI Overview — Telco Dataset',
             fontsize=14, fontweight='bold', color='white', y=1.06)
plt.tight_layout(pad=0.5)
plt.savefig('t2_kpi.png', bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("📊 Chart 1 saved : t2_kpi.png")


# ════════════════════════════════════════════════════════════
# SECTION 3 — CHURN OVERVIEW
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Donut chart — Churn vs Retained
sizes  = [retained, churned]
clabels = [f'Retained\n{retention_rate:.1f}%',
           f'Churned\n{churn_rate:.1f}%']
wedge_colors = ['#2dc653', '#f72585']
wedges, texts, autotexts = axes[0].pie(
    sizes, labels=clabels, autopct='%1.1f%%',
    colors=wedge_colors, startangle=90,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
    textprops=dict(fontsize=11))
for at in autotexts:
    at.set_fontweight('bold')
axes[0].set_title('Overall Churn vs Retention',
                   fontweight='bold', fontsize=13)

# Churn by Contract Type
contract_churn = df.groupby('Contract')['Churned'].agg(['sum','count'])
contract_churn['rate'] = contract_churn['sum'] / contract_churn['count'] * 100
contract_churn = contract_churn.sort_values('rate', ascending=False)
bar_colors = ['#f72585','#f8961e','#2dc653']
bars = axes[1].bar(contract_churn.index, contract_churn['rate'],
                   color=bar_colors, edgecolor='white', linewidth=0.8)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].set_title('Churn Rate by Contract Type',
                   fontweight='bold', fontsize=13)
axes[1].set_xlabel('Contract Type')
axes[1].set_ylabel('Churn Rate (%)')
for bar, val in zip(bars, contract_churn['rate']):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center',
                 fontsize=10, fontweight='bold')

# Churn by Internet Service
net_churn = df.groupby('Internet Service')['Churned'].agg(['sum','count'])
net_churn['rate'] = net_churn['sum'] / net_churn['count'] * 100
net_churn = net_churn.sort_values('rate', ascending=False)
bars2 = axes[2].bar(net_churn.index, net_churn['rate'],
                    color=['#f72585','#f8961e','#2dc653'],
                    edgecolor='white', linewidth=0.8)
axes[2].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[2].set_title('Churn Rate by Internet Service',
                   fontweight='bold', fontsize=13)
axes[2].set_xlabel('Internet Service')
axes[2].set_ylabel('Churn Rate (%)')
for bar, val in zip(bars2, net_churn['rate']):
    axes[2].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center',
                 fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('t2_churn_overview.png', bbox_inches='tight')
plt.show()
print("📊 Chart 2 saved : t2_churn_overview.png")


# ════════════════════════════════════════════════════════════
# SECTION 4 — TENURE & CHARGES ANALYSIS
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Tenure distribution by churn
churned_df  = df[df['Churned'] == 1]['Tenure Months']
retained_df = df[df['Churned'] == 0]['Tenure Months']
axes[0].hist(retained_df, bins=30, alpha=0.65, color='#2dc653',
             label=f'Retained (n={retained:,})', edgecolor='white')
axes[0].hist(churned_df,  bins=30, alpha=0.65, color='#f72585',
             label=f'Churned  (n={churned:,})',  edgecolor='white')
axes[0].axvline(churned_df.mean(),  color='#f72585', linestyle='--',
                linewidth=1.5, label=f'Churned avg: {churned_df.mean():.1f}mo')
axes[0].axvline(retained_df.mean(), color='#2dc653', linestyle='--',
                linewidth=1.5, label=f'Retained avg: {retained_df.mean():.1f}mo')
axes[0].set_xlabel('Tenure (Months)', fontsize=11)
axes[0].set_ylabel('Number of Customers', fontsize=11)
axes[0].set_title('Tenure Distribution: Churned vs Retained',
                   fontweight='bold', fontsize=12)
axes[0].legend(fontsize=8)

# Churn rate by tenure group
tg = df.groupby('Tenure Group', observed=True)['Churned']\
       .agg(['sum','count'])
tg['rate'] = tg['sum'] / tg['count'] * 100
colors_tg = ['#f72585' if r > 30 else '#f8961e' if r > 15 else '#2dc653'
             for r in tg['rate']]
bars = axes[1].bar(tg.index, tg['rate'],
                   color=colors_tg, edgecolor='white', linewidth=0.8)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].set_title('Churn Rate by Tenure Group',
                   fontweight='bold', fontsize=12)
axes[1].set_xlabel('Tenure (Months)')
axes[1].set_ylabel('Churn Rate (%)')
for bar, val in zip(bars, tg['rate']):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center', fontsize=9)

# Monthly Charges: Churned vs Retained boxplot
plot_data = df[['Monthly Charges', 'Churn Label']].copy()
sns.boxplot(data=plot_data, x='Churn Label', y='Monthly Charges',
            palette={'Yes': '#f72585', 'No': '#2dc653'},
            ax=axes[2], linewidth=1.5)
axes[2].set_title('Monthly Charges: Churned vs Retained',
                   fontweight='bold', fontsize=12)
axes[2].set_xlabel('Churn Status')
axes[2].set_ylabel('Monthly Charges ($)')
churned_avg  = df[df['Churned']==1]['Monthly Charges'].mean()
retained_avg = df[df['Churned']==0]['Monthly Charges'].mean()
axes[2].text(0.05, 0.93,
             f'Churned avg : ${churned_avg:.1f}\n'
             f'Retained avg: ${retained_avg:.1f}',
             transform=axes[2].transAxes, fontsize=9,
             bbox=dict(facecolor='#fff9c4', edgecolor='gray', alpha=0.9))

plt.tight_layout()
plt.savefig('t2_tenure_charges.png', bbox_inches='tight')
plt.show()
print("📊 Chart 3 saved : t2_tenure_charges.png")


# ════════════════════════════════════════════════════════════
# SECTION 5 — CHURN DRIVERS (Demographics & Services)
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

cols = ['Gender', 'Senior Citizen', 'Partner',
        'Dependents', 'Paperless Billing', 'Payment Method']

for i, col in enumerate(cols):
    grp = df.groupby(col)['Churned'].agg(['sum','count'])
    grp['rate'] = grp['sum'] / grp['count'] * 100
    grp = grp.sort_values('rate', ascending=False)
    bar_c = ['#f72585' if r > 30 else '#f8961e' if r > 20
             else '#2dc653' for r in grp['rate']]
    bars = axes[i].bar(grp.index, grp['rate'],
                       color=bar_c, edgecolor='white', linewidth=0.8)
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter())
    axes[i].set_title(f'Churn Rate by {col}',
                      fontweight='bold', fontsize=11)
    axes[i].set_ylabel('Churn Rate (%)')
    axes[i].tick_params(axis='x', rotation=15)
    for bar, val in zip(bars, grp['rate']):
        axes[i].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.4,
                     f'{val:.1f}%', ha='center', fontsize=8)

plt.suptitle('Churn Rate by Customer Demographics & Billing',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('t2_churn_drivers.png', bbox_inches='tight')
plt.show()
print("📊 Chart 4 saved : t2_churn_drivers.png")


# ════════════════════════════════════════════════════════════
# SECTION 6 — SERVICES IMPACT ON CHURN
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

service_cols = ['Phone Service', 'Online Security', 'Online Backup',
                'Device Protection', 'Tech Support', 'Streaming TV']

for i, col in enumerate(service_cols):
    grp = df.groupby(col)['Churned'].agg(['sum','count'])
    grp['rate'] = grp['sum'] / grp['count'] * 100
    grp = grp.sort_values('rate', ascending=False)
    bar_c = ['#f72585' if r > 30 else '#f8961e' if r > 20
             else '#2dc653' for r in grp['rate']]
    bars = axes[i].bar(grp.index, grp['rate'],
                       color=bar_c, edgecolor='white', linewidth=0.8)
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter())
    axes[i].set_title(f'Churn Rate by {col}',
                      fontweight='bold', fontsize=11)
    axes[i].set_ylabel('Churn Rate (%)')
    axes[i].tick_params(axis='x', rotation=15)
    for bar, val in zip(bars, grp['rate']):
        axes[i].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.4,
                     f'{val:.1f}%', ha='center', fontsize=8)

plt.suptitle('Churn Rate by Service Subscription',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('t2_services_churn.png', bbox_inches='tight')
plt.show()
print("📊 Chart 5 saved : t2_services_churn.png")


# ════════════════════════════════════════════════════════════
# SECTION 7 — COHORT / RETENTION ANALYSIS
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Retention rate by tenure group
tg_ret = df.groupby('Tenure Group', observed=True)['Churned']\
           .agg(['sum','count'])
tg_ret['retention'] = (1 - tg_ret['sum'] / tg_ret['count']) * 100

axes[0].plot(tg_ret.index, tg_ret['retention'],
             marker='o', linewidth=2.5, markersize=8,
             color='#4361ee', markerfacecolor='#f72585',
             markeredgecolor='white', markeredgewidth=1.5)
axes[0].fill_between(range(len(tg_ret)), tg_ret['retention'],
                     alpha=0.15, color='#4361ee')
axes[0].set_ylim(0, 105)
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[0].set_title('Retention Rate by Tenure Cohort',
                   fontweight='bold', fontsize=13)
axes[0].set_xlabel('Tenure Group (Months)')
axes[0].set_ylabel('Retention Rate (%)')
for x, (idx, row) in enumerate(tg_ret.iterrows()):
    axes[0].annotate(f"{row['retention']:.1f}%",
                     (x, row['retention']),
                     textcoords='offset points', xytext=(0, 10),
                     ha='center', fontsize=9, fontweight='bold',
                     color='#4361ee')

# CLTV by Churn Status
cltv_data = df[['CLTV', 'Churn Label']].copy()
sns.violinplot(data=cltv_data, x='Churn Label', y='CLTV',
               palette={'Yes': '#f72585', 'No': '#2dc653'},
               ax=axes[1], linewidth=1.5, inner='quartile')
axes[1].yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
axes[1].set_title('Customer Lifetime Value (CLTV): Churned vs Retained',
                   fontweight='bold', fontsize=12)
axes[1].set_xlabel('Churn Status')
axes[1].set_ylabel('CLTV ($)')
cltv_c = df[df['Churned']==1]['CLTV'].mean()
cltv_r = df[df['Churned']==0]['CLTV'].mean()
axes[1].text(0.05, 0.93,
             f'Churned avg : ${cltv_c:,.0f}\n'
             f'Retained avg: ${cltv_r:,.0f}',
             transform=axes[1].transAxes, fontsize=9,
             bbox=dict(facecolor='#fff9c4', edgecolor='gray', alpha=0.9))

plt.tight_layout()
plt.savefig('t2_cohort_cltv.png', bbox_inches='tight')
plt.show()
print("📊 Chart 6 saved : t2_cohort_cltv.png")


# ════════════════════════════════════════════════════════════
# SECTION 8 — TOP CHURN REASONS
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Top churn reasons
churn_reasons = df[df['Churned']==1]['Churn Reason']\
                .dropna().value_counts().head(12)
bars = axes[0].barh(churn_reasons.index[::-1],
                    churn_reasons.values[::-1],
                    color='#f72585', edgecolor='white', linewidth=0.8)
axes[0].set_title('Top 12 Churn Reasons',
                   fontweight='bold', fontsize=13)
axes[0].set_xlabel('Number of Customers')
for bar, val in zip(bars, churn_reasons.values[::-1]):
    axes[0].text(val + 3, bar.get_y() + bar.get_height()/2,
                 str(val), va='center', fontsize=8)

# Churn risk heatmap: Contract × Internet Service
heatmap_data = df.groupby(['Contract', 'Internet Service'])['Churned']\
               .mean().unstack() * 100
sns.heatmap(heatmap_data, ax=axes[1], annot=True, fmt='.1f',
            cmap='RdYlGn_r', linewidths=0.5, linecolor='white',
            annot_kws={'size': 11, 'weight': 'bold'},
            cbar_kws={'label': 'Churn Rate (%)'})
axes[1].set_title('Churn Rate Heatmap: Contract × Internet Service',
                   fontweight='bold', fontsize=13)
axes[1].set_xlabel('Internet Service')
axes[1].set_ylabel('Contract Type')

plt.tight_layout()
plt.savefig('t2_reasons_heatmap.png', bbox_inches='tight')
plt.show()
print("📊 Chart 7 saved : t2_reasons_heatmap.png")


# ════════════════════════════════════════════════════════════
# SECTION 9 — KEY INSIGHTS (printed)
# ════════════════════════════════════════════════════════════

top_reason    = df[df['Churned']==1]['Churn Reason'].value_counts().idxmax()
high_risk_con = df.groupby('Contract')['Churned'].mean().idxmax()
high_risk_net = df.groupby('Internet Service')['Churned'].mean().idxmax()
high_risk_pay = df.groupby('Payment Method')['Churned'].mean().idxmax()

print(f"""
╔══════════════════════════════════════════════════════════╗
║        KEY INSIGHTS — CHURN & RETENTION ANALYSIS        ║
╠══════════════════════════════════════════════════════════╣
║  1. Overall Churn Rate    : {churn_rate:.1f}%                       ║
║  2. Avg Churned Tenure    : {churned_tenure:.1f} months                  ║
║  3. Avg Retained Tenure   : {retained_tenure:.1f} months                 ║
║  4. Top Churn Reason      : {top_reason[:28]:<28}║
║  5. Highest Risk Contract : {high_risk_con:<28}║
║  6. Highest Risk Internet : {high_risk_net:<28}║
║  7. Highest Risk Payment  : {high_risk_pay[:28]:<28}║
╠══════════════════════════════════════════════════════════╣
║                  RECOMMENDATIONS                        ║
╠══════════════════════════════════════════════════════════╣
║  ✅ Push Month-to-Month customers to annual contracts    ║
║  ✅ Target first 12 months with loyalty incentives       ║
║  ✅ Offer Online Security & Tech Support bundles         ║
║  ⚠️  Fiber Optic customers churn most — review pricing   ║
║  ⚠️  Electronic check users have highest churn risk      ║
╚══════════════════════════════════════════════════════════╝
""")


# ════════════════════════════════════════════════════════════
# SECTION 10 — GENERATE PDF REPORT
# ════════════════════════════════════════════════════════════

doc    = SimpleDocTemplate(
    'FUTURE_DS_02_Report.pdf', pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=1.5*cm,   bottomMargin=1.5*cm)
styles = getSampleStyleSheet()
story  = []

title_style = ParagraphStyle(
    'MyTitle', parent=styles['Title'],
    fontSize=19, textColor=colors.HexColor('#1a1a2e'),
    spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold')
sub_style = ParagraphStyle(
    'MySub', parent=styles['Normal'],
    fontSize=10, textColor=colors.HexColor('#555555'),
    alignment=TA_CENTER, spaceAfter=12)
h2_style = ParagraphStyle(
    'MyH2', parent=styles['Heading2'],
    fontSize=13, textColor=colors.HexColor('#f72585'),
    spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold')
insight_style = ParagraphStyle(
    'Insight', parent=styles['Normal'],
    fontSize=9.5, leading=15,
    textColor=colors.HexColor('#1a1a2e'), leftIndent=10)
cap_style = ParagraphStyle(
    'Cap', parent=styles['Normal'],
    fontSize=8.5, textColor=colors.HexColor('#888888'),
    alignment=TA_CENTER, spaceAfter=6)

# Cover
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('Customer Retention & Churn Analysis', title_style))
story.append(Paragraph(
    'Future Interns — Data Science &amp; Analytics | Task 2 (FUTURE_DS_02)',
    sub_style))
story.append(Paragraph(
    'Dataset: Telco Customer Churn &nbsp;|&nbsp; Tools: Python, Pandas, Matplotlib, Seaborn',
    sub_style))
story.append(HRFlowable(width='100%', thickness=2,
                        color=colors.HexColor('#f72585'), spaceAfter=10))

# KPI Table
story.append(Paragraph('Executive KPI Summary', h2_style))
kpi_data = [
    ['Metric', 'Value', 'Metric', 'Value'],
    ['Total Customers', f'{total_customers:,}',
     'Churned Customers', f'{churned:,}'],
    ['Churn Rate',      f'{churn_rate:.1f}%',
     'Retention Rate',  f'{retention_rate:.1f}%'],
    ['Avg Tenure',      f'{avg_tenure:.1f} months',
     'Churned Avg Tenure', f'{churned_tenure:.1f} months'],
    ['Avg Monthly Charge', f'${avg_monthly:.2f}',
     'Avg CLTV',        f'${avg_cltv:,.0f}'],
]
kpi_table = Table(kpi_data,
                  colWidths=[4.5*cm, 4.2*cm, 4.5*cm, 4.2*cm])
kpi_table.setStyle(TableStyle([
    ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#f72585')),
    ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
    ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0, 0), (-1, 0),  10),
    ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME',      (0, 1), (0, -1),  'Helvetica-Bold'),
    ('FONTNAME',      (2, 1), (2, -1),  'Helvetica-Bold'),
    ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.HexColor('#fff0f5'),
                                         colors.white]),
    ('GRID',          (0, 0), (-1, -1), 0.5,
                                         colors.HexColor('#cccccc')),
    ('ROWHEIGHT',     (0, 0), (-1, -1), 18),
    ('TOPPADDING',    (0, 0), (-1, -1), 4),
]))
story.append(kpi_table)
story.append(Spacer(1, 0.3*cm))

# Charts
charts = [
    ('t2_kpi.png',            'Fig 1 — Churn & Retention KPI Dashboard',
     17*cm, 3.0*cm),
    ('t2_churn_overview.png', 'Fig 2 — Churn Overview: Overall, Contract & Internet',
     17*cm, 6.0*cm),
    ('t2_tenure_charges.png', 'Fig 3 — Tenure Distribution & Monthly Charges Analysis',
     17*cm, 6.0*cm),
    ('t2_churn_drivers.png',  'Fig 4 — Churn Rate by Demographics & Billing',
     17*cm, 10*cm),
    ('t2_services_churn.png', 'Fig 5 — Churn Rate by Service Subscription',
     17*cm, 10*cm),
    ('t2_cohort_cltv.png',    'Fig 6 — Retention Cohort & Customer Lifetime Value',
     17*cm, 6.0*cm),
    ('t2_reasons_heatmap.png','Fig 7 — Top Churn Reasons & Risk Heatmap',
     17*cm, 6.5*cm),
]
for fname, caption, w, h in charts:
    story.append(Paragraph(caption, cap_style))
    story.append(Image(fname, width=w, height=h))
    story.append(Spacer(1, 0.2*cm))

# Key Insights
story.append(HRFlowable(width='100%', thickness=1.5,
                        color=colors.HexColor('#f72585'), spaceAfter=8))
story.append(Paragraph('Key Insights', h2_style))

insights = [
    ('📉 High Churn Rate',
     f'The overall churn rate is {churn_rate:.1f}%, meaning roughly 1 in 4 '
     f'customers leave. This represents significant revenue risk.'),
    ('⏱️ Early Tenure Risk',
     f'Customers in the 0–12 month cohort have the highest churn rate. '
     f'Churned customers leave after an average of {churned_tenure:.1f} months '
     f'vs {retained_tenure:.1f} months for retained customers.'),
    ('📋 Contract Type is Key',
     f'Month-to-month contract holders churn at dramatically higher rates '
     f'than annual or two-year contract customers. Long-term contracts act '
     f'as the strongest retention anchor.'),
    ('🌐 Fiber Optic Risk',
     f'Fiber Optic internet customers have the highest churn rate despite '
     f'being a premium service — likely due to pricing or competition.'),
    ('🔒 Services Protect Retention',
     f'Customers without Online Security and Tech Support churn at much '
     f'higher rates. Bundling these services significantly boosts retention.'),
    ('💳 Payment Method Matters',
     f'Electronic check users show the highest churn risk. Auto-pay '
     f'methods (credit card, bank transfer) correlate with higher retention.'),
    ('💰 CLTV Difference',
     f'Retained customers have significantly higher CLTV (${cltv_r:,.0f}) '
     f'vs churned customers (${cltv_c:,.0f}). Retention directly drives revenue.'),
]
for title, text in insights:
    story.append(Paragraph(f'<b>{title}:</b> {text}', insight_style))
    story.append(Spacer(1, 0.15*cm))

# Recommendations
story.append(Paragraph('Actionable Recommendations', h2_style))
recs = [
    ('Convert Month-to-Month Customers',
     'Offer discounts or incentives to upgrade to annual contracts. '
     'Even a 10% discount on a 1-year plan is cheaper than losing a customer.'),
    ('First 12 Months Onboarding Program',
     'Launch a loyalty program targeting new customers in their first year — '
     'the highest-risk period. Proactive check-ins and rewards reduce early churn.'),
    ('Bundle Security & Support Services',
     'Customers without Online Security and Tech Support churn far more. '
     'Offer these as free add-ons for the first 3 months to boost adoption.'),
    ('Review Fiber Optic Pricing',
     'Fiber Optic customers churn most despite paying premium prices. '
     'Conduct a competitive pricing review and improve service quality.'),
    ('Promote Auto-Pay Enrollment',
     'Incentivize customers to switch from electronic checks to auto-pay. '
     'Offer a small monthly discount for credit card or bank transfer payments.'),
]
for i, (title, text) in enumerate(recs, 1):
    story.append(Paragraph(f'<b>{i}. {title}:</b> {text}', insight_style))
    story.append(Spacer(1, 0.12*cm))

# Footer
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width='100%', thickness=1,
                        color=colors.HexColor('#cccccc')))
story.append(Paragraph(
    'Analysis by: [Your Name] &nbsp;|&nbsp; Future Interns — '
    'Data Science &amp; Analytics &nbsp;|&nbsp; FUTURE_DS_02',
    ParagraphStyle('foot', parent=styles['Normal'], fontSize=8,
                   textColor=colors.HexColor('#999999'),
                   alignment=TA_CENTER, spaceBefore=8)))

doc.build(story)
