import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv("data/statistics-MAMMKTD_1v2-Train_1000.csv")
df2 = pd.read_csv("data/statistics-ddpg_1v2.csv")
df3 = pd.read_csv("data/statistics-maddpg_1v2.csv")
df4 = pd.read_csv("data/statistics-dqn_1v2.csv")

collision_list0 = []
collision_list1 = []
collision_list2 = []
collision_list0.append(df['collisions_0'][0])
collision_list1.append(df['collisions_1'][0])
collision_list2.append(df['collisions_2'][0])

for i in range(len(df['collisions_0'])):
    if i != 0:
        collision_list0.append(df['collisions_0'][i] - df['collisions_0'][i - 1])
        collision_list1.append(df['collisions_1'][i] - df['collisions_1'][i - 1])
        collision_list2.append(df['collisions_2'][i] - df['collisions_2'][i - 1])

df['collisions_0'] = collision_list0
df['collisions_1'] = collision_list1
df['collisions_2'] = collision_list2

df_collisions_new = pd.DataFrame()
df_collisions_new['collisions_DDPG'] = (df2['collisions_0'][:1001] + df2['collisions_1'][:1001] + df2['collisions_2'][:1001])/3

df_collisions_new['collisions_MADDPG'] = (df3['collisions_0'][:1001] + df3['collisions_1'][:1001] + df3['collisions_2'][:1001])/3

df_collisions_new['collisions_DQN'] = (df4['collisions_0'][:1001] + df4['collisions_1'][:1001] + df4['collisions_2'][:1001])/3

df_collisions_new['collisions_MAMMKTD'] = (df['collisions_0'] + df['collisions_1'] + df['collisions_2'])/3
# df_collisions_new['collisions_MAMMKTD'] = (np.sqrt(np.power(df['collisions_0'], 2)) + np.sqrt(np.power(df['collisions_1'], 2)) +
#                                np.sqrt(np.power(df['collisions_2'], 2)))/3


for i in range(len(df_collisions_new['collisions_DDPG'])):
    if i != 0:
        df_collisions_new['collisions_DDPG'][i] = df_collisions_new['collisions_DDPG'][i] + \
                                                  df_collisions_new['collisions_DDPG'][i-1]

        df_collisions_new['collisions_MADDPG'][i] = df_collisions_new['collisions_MADDPG'][i] + \
                                                    df_collisions_new['collisions_MADDPG'][i - 1]

        df_collisions_new['collisions_DQN'][i] = df_collisions_new['collisions_DQN'][i] + \
                                                 df_collisions_new['collisions_DQN'][i - 1]

        df_collisions_new['collisions_MAMMKTD'][i] = df_collisions_new['collisions_MAMMKTD'][i] + \
                                                     df_collisions_new['collisions_MAMMKTD'][i - 1]

fig = plt.figure()

ax = fig.add_axes([0, 0, 1, 1])
df_collisions_new_standardized = (df_collisions_new - df_collisions_new.mean())/df_collisions_new.std()

lower_range = 100
upper_range = 1000

x = df['episode'][lower_range:upper_range]
y = df_collisions_new_standardized['collisions_DDPG'][lower_range:upper_range]
error = (df_collisions_new['collisions_DDPG'].std())/1000
plt.plot(x, y, 'k', color='#CC4F1B', label='collisions DDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


y = df_collisions_new_standardized['collisions_MADDPG'][lower_range:upper_range]
error = (df_collisions_new['collisions_MADDPG'].std())/1000
plt.plot(x, y, 'k', color='#1B2ACC', label='collisions MADDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
    linewidth=4, linestyle='dashdot', antialiased=True)



y = df_collisions_new_standardized['collisions_DQN'][lower_range:upper_range]
error = (df_collisions_new['collisions_DQN'].std())/1000
plt.plot(x, y, 'k', color='#3F7F4C', label='collisions DQN')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#3F7F4C', facecolor='#7EFF99',
    linewidth=0)


y = df_collisions_new_standardized['collisions_MAMMKTD'][lower_range:upper_range]
error = (df_collisions_new['collisions_MAMMKTD'].std())/1000
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
