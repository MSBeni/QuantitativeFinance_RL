import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# df = pd.read_csv("data/statistics-MAMMKTD_1v2_1000.csv")
df = pd.read_csv("data/statistics-MAMMKTD_1v2-Train_1000.csv")
df2 = pd.read_csv("data/statistics-ddpg_1v2.csv")
df3 = pd.read_csv("data/statistics-maddpg_1v2.csv")
df4 = pd.read_csv("data/statistics-dqn_1v2.csv")

df_steps_new = pd.DataFrame()
df_steps_new['steps_DDPG'] = df2['steps'][:1001]

df_steps_new['steps_MADDPG'] = df3['steps'][:1001]

df_steps_new['steps_DQN'] = df4['steps'][:1001]

df_steps_new['steps_MAMMKTD'] = df['steps'] 
# df_steps_new['steps_MAMMKTD'] = (np.sqrt(np.power(df['steps_0'], 2)) + np.sqrt(np.power(df['steps_1'], 2)) +
#                                np.sqrt(np.power(df['steps_2'], 2)))/3


for i in range(len(df_steps_new['steps_DDPG'])):
    if i != 0:
        df_steps_new['steps_DDPG'][i] = df_steps_new['steps_DDPG'][i] + \
                                                  df_steps_new['steps_DDPG'][i - 1]

        df_steps_new['steps_MADDPG'][i] = df_steps_new['steps_MADDPG'][i] + \
                                                    df_steps_new['steps_MADDPG'][i - 1]

        df_steps_new['steps_DQN'][i] = df_steps_new['steps_DQN'][i] + \
                                                 df_steps_new['steps_DQN'][i - 1]

        df_steps_new['steps_MAMMKTD'][i] = df_steps_new['steps_MAMMKTD'][i] + \
                                                     df_steps_new['steps_MAMMKTD'][i - 1]





fig = plt.figure()

ax = fig.add_axes([0, 0, 1, 1])
df_steps_new_standardized = (df_steps_new - df_steps_new.mean())/df_steps_new.std()

lower_range = 1
upper_range = 1000

x = df['episode'][lower_range:upper_range]
y = df_steps_new_standardized['steps_DDPG'][lower_range:upper_range]
error = (df_steps_new['steps_DDPG'].std())/100000
plt.plot(x, y, 'k', color='#CC4F1B', label='steps DDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


y = df_steps_new_standardized['steps_MADDPG'][lower_range:upper_range]
error = (df_steps_new['steps_MADDPG'].std())/100000
plt.plot(x, y, 'k', color='#1B2ACC', label='steps MADDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
    linewidth=4, linestyle='dashdot', antialiased=True)



y = df_steps_new_standardized['steps_DQN'][lower_range:upper_range]
error = (df_steps_new['steps_DQN'].std())/100000
plt.plot(x, y, 'k', color='#3F7F4C', label='steps DQN')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#3F7F4C', facecolor='#7EFF99',
    linewidth=0)


y = df_steps_new_standardized['steps_MAMMKTD'][lower_range:upper_range]
error = (df_steps_new['steps_MAMMKTD'].std())/100000
plt.plot(x, y, 'k', color='#6e3f7f', label='steps MAMMKTD')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#bf5ee6', facecolor='#d79fed',
    linewidth=0)
# plt.xlim(0, 500, 1000)
# plt.xticks([0, 500, 1000])
# major_ticks = np.arange(0, 2, 1)
# minor_ticks = np.arange(0, 2, 1)
# ax.set_xticks(major_ticks)
# ax.set_yticks(major_ticks)
plt.legend()
plt.grid()
ax.set_xlabel('episode')
ax.set_ylabel('Cumulative Steps')

plt.show()
