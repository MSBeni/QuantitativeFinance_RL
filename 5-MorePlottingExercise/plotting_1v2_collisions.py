import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv("data/statistics-MAMMKTD_1v2_1000.csv")
df2 = pd.read_csv("data/statistics-ddpg_1v2.csv")
df3 = pd.read_csv("data/statistics-maddpg_1v2.csv")
df4 = pd.read_csv("data/statistics-dqn_1v2.csv")

df_collisions_new = pd.DataFrame()
df_collisions_new['collisions_DDPG'] = (df2['collisions_0'][:1001] + df2['collisions_1'][:1001] + df2['collisions_2'][:1001])/3

df_collisions_new['collisions_MADDPG'] = (df3['collisions_0'][:1001] + df3['collisions_1'][:1001] + df3['collisions_2'][:1001])/3

df_collisions_new['collisions_DQN'] = (df4['collisions_0'][:1001] + df4['collisions_1'][:1001] + df4['collisions_2'][:1001])/3

df_collisions_new['collisions_MAMMKTD'] = (df['collisions_0'] + df['collisions_1'] + df['collisions_2'])/3
# df_collisions_new['collisions_MAMMKTD'] = (np.sqrt(np.power(df['collisions_0'], 2)) + np.sqrt(np.power(df['collisions_1'], 2)) +
#                                np.sqrt(np.power(df['collisions_2'], 2)))/3



fig = plt.figure()

ax = fig.add_axes([0, 0, 1, 1])
df_collisions_new_standardized = (df_collisions_new - df_collisions_new.mean())/df_collisions_new.std()

lower_range = 1
upper_range = 1000

x = df['episode'][lower_range:upper_range]
y = df_collisions_new_standardized['collisions_DDPG'][lower_range:upper_range]
error = (df_collisions_new['collisions_DDPG'].std())/100
plt.plot(x, y, 'k', color='#CC4F1B', label='collisions DDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


y = df_collisions_new_standardized['collisions_MADDPG'][lower_range:upper_range]
error = (df_collisions_new['collisions_MADDPG'].std())/100
plt.plot(x, y, 'k', color='#1B2ACC', label='collisions MADDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
    linewidth=4, linestyle='dashdot', antialiased=True)



y = df_collisions_new_standardized['collisions_DQN'][lower_range:upper_range]
error = (df_collisions_new['collisions_DQN'].std())/100
plt.plot(x, y, 'k', color='#3F7F4C', label='collisions DQN')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#3F7F4C', facecolor='#7EFF99',
    linewidth=0)


y = df_collisions_new_standardized['collisions_MAMMKTD'][lower_range:upper_range]
error = (df_collisions_new['collisions_MAMMKTD'].std())/100
plt.plot(x, y, 'k', color='#6e3f7f', label='collisions MAMMKTD')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#bf5ee6', facecolor='#d79fed',
    linewidth=0)

# major_ticks = np.arange(0, 2, 1)
# minor_ticks = np.arange(0, 2, 1)
# ax.set_xticks(major_ticks)
# ax.set_yticks(major_ticks)
plt.legend()
plt.grid()
ax.set_xlabel('x(m)')
ax.set_ylabel('y(m)')

plt.show()
