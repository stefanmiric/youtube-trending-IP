import pandas as pd
import collections

countries = ['CA', 'DE', 'FR', 'GB', 'US']

for country in countries:
    print('Preparing ' + country)
    categories = pd.read_json('./dataset/' + country + '_category_id.json')['items']
    categories = dict([(int(category['id']), category['snippet']['title']) for category in categories])

    dataset = pd.read_csv('./dataset/' + country + 'videos.csv')

    dataset = dataset.drop(['thumbnail_link', 'description'], axis=1)

    dataset['trending_date'] = pd.to_datetime(dataset['trending_date'], format='%y.%d.%m')
    dataset['publish_date'] = pd.to_datetime(dataset['publish_time'])
    weekdays = ['Ponedeljak', 'Utorak', 'Sreda', 'Cetvrtak', 'Petak', 'Subota', 'Nedelja']
    dataset['publish_weekday'] = [str(publish_time.weekday()) + ' - ' + weekdays[publish_time.weekday()] for publish_time in pd.to_datetime(dataset['publish_time'])]
    dataset['category'] = [categories[cat_id] if cat_id in categories else 'Unknown' for cat_id in dataset['category_id']]
    daysTrending = collections.Counter(dataset['video_id'])
    dataset['days_trending'] = [daysTrending[video_id] for video_id in dataset['video_id']]

    daysToTrendMap = {}


    def addDaysToTrend (i):
        video = dataset.iloc[[i]]
        video_id = video['video_id'].values[0]
        if video_id in daysToTrendMap:
            return daysToTrendMap[video_id]
        daysToTrendMap[video_id] = [delta.days + 1 for delta in (video['trending_date'] - video['publish_date'])][0]
        return daysToTrendMap[video_id]

    dataset['days_to_trend'] = list(map(addDaysToTrend, range(dataset.shape[0])))

    # print(dataset.head())
    print('Done')

    dataset.to_csv('./prepared-dataset/' + country + 'videos.prep.csv', index=False)