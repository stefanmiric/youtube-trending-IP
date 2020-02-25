import pandas as pd
import matplotlib.pyplot as plt


def compare(A, B):
    a_total = 0
    b_same = 0
    for id in A:
        a_total += 1
        # print(B == id)
        if (B == id).any():
            b_same += 1
    return b_same / a_total

countries = ['CA', 'DE', 'FR', 'GB', 'US']
data = {}

for country in countries:
    data[country] = pd.read_csv('./prepared-dataset/' + country + 'videos.csv')
    data[country] = data[country]['video_id']
    print(str(country) + " | Ukupno redova:  " + str(data[country].shape[0]) + ", jedinstvenih klipova: " + str(data[country].drop_duplicates().shape[0]))
    data[country] = data[country].drop_duplicates()

results = {
    'CA': {},
    'DE': {},
    'FR': {},
    'GB': {},
    'US': {},
}
for A in countries:
    for B in countries:
        results[A][B] = compare(data[A], data[B])

tabledata = []
for A in countries:
    tmp = []
    for B in countries:
        tmp.append(results[A][B])
    tabledata.append(tmp)
print(tabledata)


plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
fig, ax = plt.subplots()
ax.imshow(tabledata, cmap='Greys')
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_xticklabels(countries)
ax.set_yticklabels(countries)

for i in range(5):
    for j in range(5):
        text = ax.text(j, i, str(int(tabledata[i][j] * 100)) + '%', ha="center", va="center", color="black")
plt.show()