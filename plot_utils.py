import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# create fake data
date_range = pd.date_range('2019-01-01 00:00:00', '2019-12-31 23:59:00', freq='1Min')  # freq='15 Min'
number_of_minutes_per_year = 24*60*365
data = pd.DataFrame(np.random.rand(number_of_minutes_per_year), columns=['measurements'], index=date_range)


##
DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']


plt.close('all')
fig, ax = plt.subplots(1, 1)
start = data.index.min()
end = data.index.max()
num_days = (end - start).days
xticks = pd.date_range('00:00', '23:45', freq='15 Min').strftime('%H:%M')
yticks = {}
heatmap = np.full([num_days, 96], np.nan)
for day in range(num_days):
    for time in range(96):
        date = start + np.timedelta64(time, '15m') + np.timedelta64(day, 'D')
        #print(date)
        if date.day == 1:
            yticks[day] = MONTHS[date.month - 1]

        if date.dayofyear == 1:
            yticks[day] += f'\n{date.year}'

        # if start <= date < end:
        if type(data['measurements'].loc[date]) == np.float64:
            heatmap[day, time] = data['measurements'].loc[date]
        else:
            heatmap[day, time] = data['measurements'].loc[date][0]

# Plotting
mesh = ax.pcolormesh(heatmap, vmin=0, vmax=data.max(), cmap='Oranges')#, cmap = cmap, edgecolors = 'grey')

# Invert y-axis
ax.invert_yaxis()

# Hatch for out of bound values in a year
ax.patch.set(hatch='xx', edgecolor='black')

# Set ticks
ax.set_yticks(list(yticks.keys()))
ax.set_yticklabels(list(yticks.values()))
ax.set_xticks([0, 24, 48, 72, 95])
ax.set_xticklabels(xticks[[0, 24, 48, 72, 95]])

# Add color bar
fig.colorbar(mesh, orientation="vertical")#, pad=0.2)
colorbar = ax.collections[0].colorbar
plt.savefig('test_data.png')