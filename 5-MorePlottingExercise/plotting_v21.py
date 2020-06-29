import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv("data/statistics-MAMMKTD_1v2_1000.csv")
df2 = pd.read_csv("data/statistics-ddpg_1v2.csv")
df3 = pd.read_csv("data/statistics-maddpg_1v2.csv")
df4 = pd.read_csv("data/statistics-dqn_1v2.csv")

df_loss_new = pd.DataFrame()
df_loss_new['loss_DDPG'] = (df2['loss_0'][:1001] + df2['loss_1'][:1001] + df2['loss_2'][:1001])/3

df_loss_new['loss_MADDPG'] = (df3['loss_0'][:1001] + df3['loss_1'][:1001] + df3['loss_2'][:1001])/3

df_loss_new['loss_DQN'] = (df4['loss_0'][:1001] + df4['loss_1'][:1001] + df4['loss_2'][:1001])/3

# df_loss_new['loss_MAMMKTD'] = (df['loss_0'] + df['loss_1'] + df['loss_2'])/3
df_loss_new['loss_MAMMKTD'] = (np.sqrt(np.power(df['loss_0'], 2)) + np.sqrt(np.power(df['loss_1'], 2)) +
                               np.sqrt(np.power(df['loss_2'], 2)))/3

fig = plt.figure()

ax = fig.add_axes([0, 0, 1, 1])
df_loss_new_standardized = (df_loss_new - df_loss_new.mean())/df_loss_new.std()

ax.plot(df['episode'], df_loss_new_standardized['loss_DDPG'], color='blue', lw=1, linestyle='-', label='Loss DDPG')
ax.plot(df['episode'], df_loss_new_standardized['loss_MADDPG'], color='red', lw=1, linestyle='-.', label='Loss MADDPG')
ax.plot(df['episode'], df_loss_new_standardized['loss_DQN'], color='green', lw=1, linestyle='-.', label='Loss DQN')
# ax.plot(df['episode'],AoA_y, color = 'purple', lw=1, linestyle = '-.', label='Angle of Arrival')
ax.plot(df['episode'], df_loss_new_standardized['loss_MAMMKTD'], color='black', lw=3, linestyle='-.',
        label='Loss MAMMKTD')
major_ticks = np.arange(0, 2, 1)
minor_ticks = np.arange(0, 2, 1)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)
plt.legend()
plt.grid()
ax.set_xlabel('x(m)')
ax.set_ylabel('y(m)')

plt.show()