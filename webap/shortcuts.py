import pandas as pd
from .models import InformationHousehold
from . import utilities
from datetime import datetime
from . import engine
import numpy as np
from . import constants as C
from datetime import timedelta
from dateutil import parser
from . import simulation as sim


def index(request):
    return True


def populate_house_information(file_path):
    data = pd.read_csv(r'D:\jaipur\zugmentors\media\informations_households.csv')

    for index, row in data.iterrows():
        ih = InformationHousehold()
        ih.LCLid = row['LCLid']
        ih.stdorToU = row['stdorToU']
        ih.Acorn = row['Acorn']
        ih.Acorn_grouped = row['Acorn_grouped']
        ih.file = row['file']
        ih.save()

'''
is_sun', 'is_mon', 'is_tue', 'is_wed', 'is_thur', 'is_fri', 'is_sat', 'last', 'public_holiday_yes', 
                            'public_holiday_no', 'is_winter', 'is_summer', 'is_autumn', 'is_spring', 'energy'
'''

def get_user_statistics(identifier):
    identifier = identifier
    success, block = utilities.get_meter_id(identifier)
    if not success:
        return False, None
    ## load appropriate dataframe
    df = utilities.load_df_from_mysql_2(block, identifier)
    this_month = utilities.get_energy_this_month(df)
    last_months = utilities.get_energy_last_months(df).values
    this_day = utilities.get_energy_this_day(df)
    # neighbourhood_mean = utilities.neighbourhood_average_this_month(utilities.load_df_from_mysql(block))

    today = str(datetime.now())
    today_date = datetime.now()

    days = utilities.findDay(today)
    season = utilities.predict_season(today)
    last = this_month
    public_holiday = utilities.is_public_holiday(today_date)

    pred_params = days
    pred_params.append(last)
    pred_params.extend(public_holiday)
    pred_params.extend(season)
    prediction = engine.predict(pred_params)

    context = {
        'this_month': int(this_month),
        'last_months': last_months,
        'previous_month': int(last_months[0]),
        'this_day': int(this_day/10),
        'prediction': prediction + 1.1*this_day
    }
    return True, context


def euc(x, df):
    x = np.array(x)
    multi = np.array([5, 4, 3, 2])
    energy = x.dot(multi)
    similarity = []
    for i in range(len(df)):
        row = df.loc[i][:4].values
        diff = x - row
        diffsq = diff * diff
        simval = 1 / (1 + np.sqrt(np.sum(diffsq)))
        similarity.append(simval)
    df['similarity'] = similarity
    df.sort_values(by='similarity', ascending=False, inplace=True)
    return df.iloc[0]['plans']


def recommend(h, f, l, b):
    df = utilities.load_df_from_mysql_3('recommendation_dataset')
    x = list(map(int, [h, f, l, b]))
    p = euc(x, df)
    return p


def automatic_simulation():
    total_load = np.dot(np.array([sim.fans, sim.bulb, sim.light, sim.fridge, sim.tv, sim.ac, sim.geyser, sim.iron]), np.array(C.VALS))
    if total_load == 0:
        return
    next_time = parser.parse(sim.last_time) + timedelta(minutes=30)
    sim.last_time = str(next_time)

    blockn = pd.DataFrame(columns=['col1', 'col2', 'col3'])
    blockn.loc[0] = ["MAC23372337", str(next_time), total_load]
    utilities.save_df_to_mysql(blockn, "block_n")


def handle_simulation(request):
    fans = request.POST.get('fan', 0)
    if fans == 'on':
        fans = 1
    sim.fans = fans
    bulb = request.POST.get('bulb', 0)
    if bulb == 'on':
        bulb = 1
    sim.bulb = bulb
    light = request.POST.get('light', 0)
    if light == 'on':
        light = 1
    sim.light = light
    fridge = request.POST.get('fridge', 0)
    if fridge == 'on':
        fridge = 1
    sim.fridge = fridge
    tv = request.POST.get('tv', 0)
    if tv == 'on':
        tv = 1
    sim.tv = tv
    ac = request.POST.get('ac', 0)
    if ac == 'on':
        ac = 1
    sim.ac = ac
    geyser = request.POST.get('geyser', 0)
    if geyser == 'on':
        geyser = 1
    sim.geyser = geyser
    iron = request.POST.get('iron', 0)
    if iron == 'on':
        iron = 1
    sim.iron = iron
    print(sim.iron, sim.geyser, sim.fans)


def update_all_houses():
    next_time = parser.parse(sim.last_time) + timedelta(minutes=30)
    sim.last_time = str(next_time)
    blockn = pd.DataFrame(columns=['col1', 'col2', 'col3'])
    for i in range(4):
        total_load = sim.houses[i]

        blockn.loc[i] = ["MAC2337233" + str(i) , str(next_time) , total_load]

    utilities.save_df_to_mysql(blockn, "block_n")


def last_hope(request):
    for i in range(1, 5):
        house = 'h' + str(i)
        features = ['fan', 'bulb', 'light', 'fridge', 'tv', 'ac', 'geyser', 'iron']
        total_for_house = 0
        for feature in features:
            this_feature = house + feature
            temp = request.POST.get(this_feature, 0)
            if temp == 'on':
                temp = 1
            total_for_house += C.UNITS_PER_HOUR[feature]*temp
        sim.houses[i] = total_for_house

