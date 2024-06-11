import pandas as pd
import matplotlib.pyplot as plt

data = [
    {'country': 'HK', 'export_value': 314586755.0, 'export_weight': '24048', 'export_growth_rate': 1201.828077798469},
    {'country': 'CN', 'export_value': 320551379.0, 'export_weight': '15927', 'export_growth_rate': 0.99567},
    {'country': 'VN', 'export_value': 255284582.0, 'export_weight': '4758', 'export_growth_rate': 527543.714604605},
    {'country': 'TW', 'export_value': 63889030.0, 'export_weight': '2808', 'export_growth_rate': 140.15756289411962},
    {'country': 'MY', 'export_value': 13571769.0, 'export_weight': '1014', 'export_growth_rate': 1407.4517500599793}
]

df = pd.DataFrame(data)

# Bar graph for export value
plt.figure(figsize=(10, 6))
df.plot(kind='bar', x='country', y='export_value', rot=0)
plt.title('Export Value by Country')
plt.xlabel('Country')
plt.ylabel('Export Value (USD)')
plt.show()

# Bar graph for export weight
plt.figure(figsize=(10, 6))
df.plot(kind='bar', x='country', y='export_weight', rot=0)
plt.title('Export Weight by Country')
plt.xlabel('Country')
plt.ylabel('Export Weight (kg)')
plt.show()

# Scatter plot for export value vs export weight
plt.figure(figsize=(10, 6))
plt.scatter(df['export_weight'], df['export_value'])
plt.title('Export Value vs Export Weight')
plt.xlabel('Export Weight (kg)')
plt.ylabel('Export Value (USD)')
plt.show()

# Scatter plot for export growth rate vs export weight
plt.figure(figsize=(10, 6))
plt.scatter(df['export_weight'], df['export_growth_rate'])
plt.title('Export Growth Rate vs Export Weight')
plt.xlabel('Export Weight (kg)')
plt.ylabel('Export Growth Rate (%)')
plt.show()
