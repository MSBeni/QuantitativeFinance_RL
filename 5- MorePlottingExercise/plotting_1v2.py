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


x = df['episode'][800:1000]
y = df_loss_new_standardized['loss_DDPG'][800:1000]
error = (df_loss_new['loss_DDPG'].std())/10000
plt.plot(x, y, 'k', color='#CC4F1B', label='Loss DDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


y = df_loss_new_standardized['loss_MADDPG'][800:1000]
error = (df_loss_new['loss_MADDPG'].std())/10000
plt.plot(x, y, 'k', color='#1B2ACC', label='Loss MADDPG')
plt.fill_between(x, y-error, y+error,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
    linewidth=4, linestyle='dashdot', antialiased=True)



y = df_loss_new_standardized['loss_DQN'][800:1000]
error = (df_loss_new['loss_DQN'].std())/100
plt.plot(x, y, 'k', color='#3F7F4C', label='Loss DQN')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#3F7F4C', facecolor='#7EFF99',
    linewidth=0)


y = df_loss_new_standardized['loss_MAMMKTD'][800:1000]
error = (df_loss_new['loss_MAMMKTD'].std())/50
plt.plot(x, y, 'k', color='#6e3f7f', label='Loss MAMMKTD')
plt.fill_between(x, y-error, y+error,
    alpha=1, edgecolor='#bf5ee6', facecolor='#d79fed',
    linewidth=0)

plt.legend()
plt.grid()
ax.set_xlabel('x(m)')
ax.set_ylabel('y(m)')

plt.show()