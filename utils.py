import calendar
import os
import shutil
import tempfile
from datetime import timedelta, datetime as dt
from supabase import create_client
import pandas as pd
import requests
import streamlit as st
from PIL import Image, ImageOps
from contextlib import contextmanager
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool


load_dotenv()


@contextmanager
# def vericudb() -> ConnectionPool:
#    pool = ConnectionPool(kwargs={
#        'host': os.getenv('DB_HOST'),
#        'port': os.getenv('DB_PORT'),
#        'dbname': os.getenv('DB_NAME'),
#        'user': os.getenv('DB_USER'),
#        'password': os.getenv('DB_PASSWORD')
#    })
#    try:
#        yield pool
#    finally:
#        pool.close()


# region Resurse
def notiff_telegram(message, rank=False):
    chat_id = '-740131861'
    token = '5714323530:AAG1UL6vtGvJeUZQUqeP2ag5fXVv9-GRADo'
    if rank:
        img = f'{BASE_PATH}\\media\\ranks\\{message}'
        try:
            requests.post(f'https://api.telegram.org/bot{token}/sendDocument?chat_id={chat_id}', files={'document': open(f'{img}.gif', 'rb')})
        except:
            requests.post(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}', files={'photo': open(f'{img}.jpg', 'rb')})
        mesaj = f'🔝 Bravo! Ai avansat la nivelul de {message}!' if message != 'Troglodit' else '😞 Troglodit. Rise back up!'
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mesaj}')
    else:
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}')


def initialize_session_state(var, val=''):
    if var not in st.session_state:
        st.session_state[var] = val


supabase = create_client(st.secrets['SUPABASE_URL'], st.secrets['SUPABASE_KEY'])
BASE_PATH = 'E:\🛡️\coding\Vericu'
NOW = dt.now()
TODAY = dt.today().date()
WEEKDAYS = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică']
AZI = WEEKDAYS[TODAY.weekday()]
states_file = f"states_{str(TODAY)[4:].replace('-', '')}.csv"
FRECVENTE = ['Azi', 'Zilnic', 'Săptămânal', 'Lunar', 'Anual']
TIMPI = {'Zilnic': 'Ora', 'Săptămânal': 'Ziua', 'Lunar': 'Ziua', 'Anual': 'Data'}
USERS = ['elvin', 'ioana']
# endregion

# region DB
questlog = {
    'Luni': {
        'Lever (x5)': 17,
        'PIEPT + TRICEPS 🏋‍': 18
    },
    'Marți': {
        'Planche (x5)': 17,
        'ABS': 18
    },
    'Miercuri': {
        'Lever (x5)': 17,
        'LEGS 🦿': 18
    },
    'Joi': {
        'Planche (x5)': 17,
        'UMERI 🏋': 18
    },
    'Vineri': {
        'Lever (x5)': 17,
        'SPATE-BICEPS 🦾': 18
    },
    'Sâmbătă': {
        'Planche (x5)': 9,
        'PK 👟': 11
    },
    'Duminică': {
        'Lever (x5)': 17
    }
}
dailies = {
    'Meditate': 8,
    'Stretching/Posture 🧘🏽‍♂': 8,
    '1 watch laters 🎥': 12,
    'Sort 1 day of Photos 📷': 17.5,
    'Handstand 🤸‍♂': 21,
    'Dance 🕺': 22,
    'Read 📖': 22.5,
    'Floss 🦷🧵': 23,
    'Sleep la 11 🛌': 23
}
movement = {
    'Workout': {
        # Piept, Triceps
        'Flotări': {'zone': ['piept', 'triceps']},
        'Dips Inele': {'zone': ['piept', 'triceps']},
        'Dips Bară': {'zone': ['piept', 'triceps']},
        'Flotări Inele': {'zone': ['piept', 'triceps']},
        'Pullovers': {'zone': ['piept']},
        'Dips Bancă': {'zone': ['triceps']},
        'Flotări Coate': {'zone': ['triceps']},

        # Spate, Biceps
        'Tracțiuni': {'zone': ['spate']},
        'Horizontal Rows': {'zone': ['spate']},
        'Dumbbell Rows': {'zone': ['spate']},
        'Bicep Curls': {'zone': ['biceps']},
        'Bicep Push-ups': {'zone': ['biceps']},
        'Reverse Pelicans': {'zone': ['biceps']},

        # Legs:
        'Squats': {'zone': ['legs']},
        'Bulgarian Squats': {'zone': ['legs']},
        'Lunges': {'zone': ['legs']},
        'Deadlifts': {'zone': ['legs']},
        'Jumping Squats': {'zone': ['legs']},
        'Rvrs N Curls': {'zone': ['legs']},
        'Hamstring Curls': {'zone': ['legs']},
        'Calf Raises': {'zone': ['legs', 'calves']},

        # Umeri:
        'Overhead Press': {'zone': ['umeri']},
        'Dumbbell Lateral Raise': {'zone': ['umeri']},
        'Handstand Pushups': {'zone': ['umeri']},
        '(Seated) Dumbell Press': {'zone': ['umeri']}
    },
    'Stretching/Posture': {
        'Child Pose',
    },
    'Others': {
        'Handstand',
        'Podul',
        'Dance',
        '21s',
        'AbRipperX'
    }
}
dishes = {
    'Sandwich 🥪': {'ingrediente': ['yyy', 'zzz']},
    'Paste 🍝': {'ingrediente': ['yyy', 'zzz']},
    'Paste cu Feta 🍝': {'ingrediente': ['paste', 'feta', 'rosii cherry']},
    'Mămăligă 🌽': {'ingrediente': ['malai']},
    'Porridge 🌾': {'ingrediente': ['yyy', 'zzz']},
    'Salată 🥗': {'ingrediente': ['salata', 'fasole/naut', 'tofu', 'rosii', 'castraveti', 'ceapa verde', 'ardei', 'masline', 'porumb']},
    'Legume la cuptor 🥔🥦🥕🌶️': {'ingrediente': ['broccoli', 'cartofi (dulci)', 'conopida', 'morcovi'], 'condimente': []},
    'Piure de Cartofi 🥔': {'ingrediente': ['cartofi', 'lapte veg']},
    'Supă de fasole 🍲': {'ingrediente': ['fasole pestrita', 'zzz']},
    'Guacamole 🥑': {'ingrediente': ['avocado', 'rosii', 'usturoi/ceapa']}
}
ingrediende = {
    'fructe': {
        'primavara': {},
        'vara': {'cireșe 🍒', 'piersici 🍑', 'lebenits 🍉', 'căpșuni🍓', 'zmeură', 'caise'},
        'toamna': {'struguri 🍇', 'mere 🍎', 'pere 🍐', 'alune 🌰', 'prune', 'nuci'},
        'iarna': {'portocale 🍊', 'clementine', 'greph', 'mandarine'},
        'others': {'banane 🍌', 'avocado 🥑'}
    },
    'legume': {'cartofi 🥔', 'roșii 🍅', 'ardei 🌶️', 'broccoli 🥦', 'morcovi 🥕', 'ceapă verde 🥬', 'ceapă 🧅', 'avocado 🥑', 'conopidă', 'țelină'},
    'condimente': {'cimbru', 'piper', 'sare', 'pudră usturoi'},
    'alimente': {'pâine'}
}
birthdays = {
    'Ioana Carmen': {'data': (5, 1, 1994), 'cadou': True},
    'Adi Mare': {'data': (31, 1, 2001), 'cadou': True},
    'Alex Mare': {'data': (20, 2, 1990), 'cadou': False},
    'Kamy': {'data': (4, 3, 1986), 'cadou': False},
    'Roland': {'data': (7, 3, 1986), 'cadou': False},
    'Spider': {'data': (20, 3, 1991), 'cadou': True},
    'Eu': {'data': (26, 3, 1993), 'cadou': True},
    'Speramts': {'data': (28, 3, 1995), 'cadou': False},
    'Timi': {'data': (18, 4), 'cadou': True},
    'Vintila': {'data': (9, 5, 1992), 'cadou': False},
    'Cap': {'data': (21, 5, 1992), 'cadou': False},
    'Tatis': {'data': (26, 5, 1967), 'cadou': True},
    'Tavi': {'data': (29, 5, 1992), 'cadou': False},
    'Liviu': {'data': (3, 7, 1989), 'cadou': False},
    'Clau': {'data': (11, 7, 1996), 'cadou': False},
    'Bebi': {'data': (16, 7, 1995), 'cadou': True},
    'Sinzic': {'data': (16, 7, 1996), 'cadou': False},
    'Betty': {'data': (22, 7, 2005), 'cadou': True},
    'Țici': {'data': (4, 8, 1998), 'cadou': True},
    'Lilis': {'data': (1, 9, 1991), 'cadou': True},
    'Călin': {'data': (6, 9, 1972), 'cadou': True},
    'DeeAnn Tanțău': {'data': (2, 10, 1996), 'cadou': False},
    'Segnoru': {'data': (12, 10, 1992), 'cadou': False},
    'Kitti': {'data': (11, 11, 2003), 'cadou': True},
    'Silviu': {'data': (23, 11, 1999), 'cadou': True},
    'Bunis': {'data': (28, 11, 1948), 'cadou': True},
    'Mamis': {'data': (6, 12, 1968), 'cadou': True},
    'Theo': {'data': (28, 12, 1993), 'cadou': True}
}
ranks = {
    0: 'Troglodit',
    3: 'Țăran',
    7: 'Sulițaș',
    14: 'Halebardier',
    30: 'Arcaș',
    60: 'Țintaș',
    90: 'Grifin',
    100: 'Grifin Regal',
    120: 'Călugăr',
    150: 'Zelot',
    180: 'Spadasin',
    210: 'Cruciat',
    240: 'Cavaler',
    270: 'Paladin',
    300: 'Înger',
    330: 'Arhanghel',
    365: 'Arhanghel Suprem'
}
# endregion


def shutdown():
    os.system('shutdown /s /t 1')


def get_birthdays() -> (dict, dict):
    sarbatoriti, upcoming = [], []
    for pers in birthdays:
        bd = birthdays[pers]['data']
        bd_an_crt = dt(TODAY.year, bd[1], bd[0]).date()
        if bd_an_crt < TODAY or bd_an_crt > TODAY + timedelta(days=6):
            continue
        else:
            varsta = f' ({TODAY.year - bd[2]} ani)' if len(bd) > 2 else ''
            aniversare = {'nume': pers, 'varsta': varsta, 'cadou': birthdays[pers]['cadou']}
            if bd_an_crt == TODAY:
                sarbatoriti.append(aniversare)
            elif birthdays[pers]['cadou']:
                aniversare['zi'] = WEEKDAYS[bd_an_crt.weekday()]
                upcoming.append(aniversare)

    if sarbatoriti:    # notify_telegram
        notifs = pd.read_csv('birthday_notifs.csv')
        notifs_azi = notifs[notifs['data'] == str(TODAY)].reset_index(drop=True)
        for s in sarbatoriti:
            if s['nume'] not in notifs_azi['sarbatorit'].values:
                notifs_azi.loc[len(notifs_azi)] = {'sarbatorit': s['nume'], 'data': TODAY}
                notiff_telegram(f"🎂 {s['nume']}{s['varsta']}{' 🎁' if s['cadou'] else ''}")
        notifs_azi.to_csv('birthday_notifs.csv', index=False)

    return sarbatoriti, upcoming


def get_today_quests(lista=True):
    if not os.path.isfile(states_file):  # If today's states csv doesn't exist, delete previous and create it
        for f in os.listdir('.'):   # delete previous file
            if 'states_' in f and f.endswith('.csv'):
                os.remove(f)
        quests = dailies | questlog[AZI]
        quests = sorted(quests, key=quests.get)
        states = pd.DataFrame({'quest': quests, 'state': False})
        states.to_csv(states_file, index=False)
    today_quests = pd.read_csv(states_file)
    return list(today_quests.to_records(index=False)) if lista else today_quests


def update_quest(quest):
    today_quests = get_today_quests(False)
    curr_quest_state = today_quests[today_quests['quest'] == quest]['state'].iloc[0]
    today_quests.loc[today_quests['quest'] == quest, 'state'] = not curr_quest_state
    today_quests.to_csv(states_file, index=False)


def display_rank():
    streak = pd.read_pickle('streak.pickle')
    streak = (dt.today() - streak.iloc[0]['last_relapse']).days
    current_rank = 'Troglodit'
    for rank in ranks:
        if streak < rank:
            break
        current_rank = ranks[rank]
    try:
        st.image(f'media\\ranks\\{current_rank}.gif')
    except:
        st.image(f'media\\ranks\\{current_rank}.jpg')
    st.text(f'{current_rank} ({streak})')

    last_notified = pd.read_csv('last_notified.csv')
    if current_rank != last_notified.iloc[0]['rank']:
        notiff_telegram(current_rank, True)
        last_notified.loc[0, 'rank'] = current_rank
        last_notified.to_csv('last_notified.csv', index=False)


def reset_streak():
    rank = pd.read_pickle('streak.pickle')
    rank.to_pickle('last_streak.pickle')
    rank.iloc[0]['last_relapse'] = dt.today()
    rank.to_pickle('streak.pickle')

    last_notified = pd.read_csv('last_notified.csv')
    last_notified.loc[0, 'rank'] = '-'
    last_notified.to_csv('last_notified.csv', index=False)


def get_today_workout(force_day=0):
    zone = []
    for wk in ['piept', 'triceps', 'spate', 'biceps', 'legs', 'umeri']:
        for e in [k for k in list(questlog[AZI if not force_day else WEEKDAYS[force_day - 1]].keys())]:
            zone.append(wk) if wk.upper() in e else ''
    return list(set([move for move, prop in movement['Workout'].items() for zona in zone if zona in prop['zone']]))


def resize_images():
    resize_images_folder = 'C:\\Users\\Elvin\\Desktop\\resize'
    max_size_kb = 500
    max_resolution = (2048, 2048)

    def compress_image(file_path, max_size_kb, max_resolution):
        temp_path = None
        try:
            with Image.open(file_path) as img:
                img = ImageOps.exif_transpose(img)
                icc_profile = img.info.get('icc_profile')
                exif_data = img.info.get('exif')
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                if img.width > max_resolution[0] or img.height > max_resolution[1]:
                    img.thumbnail(max_resolution, Image.Resampling.LANCZOS)
                quality = 100

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_path = temp_file.name

                while True:
                    save_kwargs = dict(format='JPEG', quality=quality, optimize=True, progressive=True)
                    if icc_profile:
                        save_kwargs['icc_profile'] = icc_profile
                    if exif_data:
                        save_kwargs['exif'] = exif_data
                    img.save(temp_path, **save_kwargs)

                    if os.path.getsize(temp_path) <= max_size_kb * 1024 or quality <= 10:
                        break
                    quality -= 5

            if os.path.exists(file_path):
                os.remove(file_path)
            shutil.move(temp_path, file_path)

        except Exception as e:
            st.error(f"Error processing {file_path}: {e}")
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    imagini = os.listdir(resize_images_folder)
    for i, filename in enumerate(imagini):
        file_path = os.path.join(resize_images_folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                if os.path.getsize(file_path) > max_size_kb * 1024:
                    compress_image(file_path, max_size_kb, max_resolution)
                    st.toast(f'✅ Compressed {i+1}/{len(imagini)}: {filename}')
            except Exception as e:
                st.error(f'Error processing {filename}: {e}')


# def get_tasks():
#     with vericudb() as pool:
#         with pool.connection() as conn:
#             tasks = pd.read_sql('SELECT * FROM "tasks" WHERE "user" = %s', conn, params=(st.query_params['user'],))
#
#     taskuri = {}
#     for freq in FRECVENTE:
#         freq_df = tasks[tasks['frecventa'] == freq]
#
#         # Sort:
#         if freq == 'Lunar':
#             freq_df.sort_values(by=['timp'], inplace=True)
#         elif freq != 'Azi':
#             if freq == 'Zilnic':
#                 freq_df['temp'] = pd.to_datetime(freq_df['timp'], format='%H:%M').dt.time
#             elif freq == 'Săptămânal':
#                 freq_df['temp'] = freq_df['timp'].apply(lambda x: WEEKDAYS.index(x))
#             elif freq == 'Anual':
#                 freq_df['temp'] = pd.to_datetime(freq_df['timp'] + '2026', format='%d%b%Y')
#             freq_df.sort_values(by=['temp'], inplace=True)
#             freq_df.drop(columns=['temp'], inplace=True)
#
#         taskuri[freq] = freq_df[tasks['completed'].isin([False, None])]
#         taskuri[f'✓{freq}'] = freq_df[tasks['completed'] == True]
#
#     return taskuri
#
#
# def add_dialog(freq):
#     @st.dialog(f'Adaugă task {freq}')
#     def add_task():
#         cols = st.columns(2)
#         nume_col = 0 if freq == 'Azi' else 1
#         timp = '.'
#         if freq == 'Zilnic':
#             timp = cols[0].time_input('Ora')
#         elif freq == 'Săptămânal':
#             timp = cols[0].selectbox('Ziua', WEEKDAYS)
#         elif freq == 'Lunar':
#             timp = cols[0].number_input(TIMPI[freq], min_value=1, max_value=31)
#         elif freq == 'Anual':
#             colss = cols[0].columns(2)
#             ziua = colss[0].number_input('Ziua', min_value=1, max_value=31, step=1)
#             luna = colss[1].selectbox('Luna', list(calendar.month_abbr)[1:])
#             timp = f'{ziua}{luna}'
#
#         nume = cols[nume_col].text_input('', placeholder='nume', autocomplete='off')
#         info = st.text_area('', placeholder='ℹ info').replace('\n', '  \n')
#         if nume and timp and st.columns([6, 1])[1].button('➕'):
#             if ':' in str(timp):
#                 timp = ':'.join(str(timp).split(':')[:-1])
#             query = 'INSERT INTO tasks (nume, frecventa, timp, info, completed, "user") VALUES (%s, %s, %s, %s, %s, %s)'
#             with vericudb() as pool, pool.connection() as conn:
#                 conn.execute(query, (nume, freq, timp, info, False, st.query_params['user']))
#             st.rerun()
#     add_task()
#
#
# def edit_dialog(nume_i, freq, timp_i, info_i):
#     @st.dialog(f'✏️ Edit task {freq}: {nume_i}' + ('' if freq == 'Azi' else f' ({timp_i})'))
#     def edit_task():
#         cols = st.columns(2)
#         nume_col = 0 if freq == 'Azi' else 1
#         timp = '.'
#         if freq == 'Zilnic':
#             timp = cols[0].time_input('Ora', value=timp_i)
#         elif freq == 'Săptămânal':
#             timp = cols[0].selectbox('Ziua', WEEKDAYS, index=WEEKDAYS.index(timp_i))
#         elif freq == 'Lunar':
#             timp = cols[0].number_input(TIMPI[freq], min_value=1, max_value=31, value=int(timp_i))
#         elif freq == 'Anual':
#             colss = cols[0].columns(2)
#             day = ''.join(c for c in timp_i if c.isdigit())
#             ziua = colss[0].number_input('Ziua', min_value=1, max_value=31, step=1, value=int(day))
#             luna = colss[1].selectbox('Luna', list(calendar.month_abbr)[1:],
#                                       index=list(calendar.month_abbr).index(timp_i[len(day):]) - 1)
#             timp = f'{ziua}{luna}'
#
#         nume = cols[nume_col].text_input('Nume', placeholder='nume', autocomplete='off', value=nume_i)
#         info = st.text_area('', placeholder='ℹ info', value=info_i or '').replace('\n', '  \n')
#         if nume and timp and st.columns([6, 1])[1].button('✅'):
#             if ':' in str(timp):
#                 timp = ':'.join(str(timp).split(':')[:-1])
#             query = """
#                 UPDATE tasks SET nume = %s, timp = %s, info = %s
#                 WHERE "user" = %s AND nume = %s AND frecventa = %s AND timp = %s
#             """
#             with vericudb() as pool, pool.connection() as conn:
#                 conn.execute(query, (nume, timp, info, st.query_params['user'], nume_i, freq, timp_i))
#             st.rerun()
#     edit_task()
#
#
# def delete_task(nume, frecventa, timp):
#     query = 'DELETE FROM tasks WHERE "user" = %s AND nume = %s AND frecventa = %s AND timp = %s'
#     with vericudb() as pool, pool.connection() as conn:
#         conn.execute(query, (st.query_params['user'], nume, frecventa, timp))
#         conn.commit()
#
#
# def check_task(completed, nume, frecventa, timp):
#     query = 'UPDATE tasks SET completed = %s, last_completed = %s WHERE "user" = %s AND nume = %s AND frecventa = %s AND timp = %s'
#     with vericudb() as pool:
#         with pool.connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query, (completed, NOW if completed else None, st.query_params['user'], nume, frecventa, timp))
#             conn.commit()
#
#
# def reset_tasks():
#     with vericudb() as pool:
#         with pool.connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute('SELECT nume, frecventa, timp, last_completed FROM tasks')
#                 tasks = cursor.fetchall()
#
#                 for nume, frecventa, timp, last_completed in tasks:
#                     if not last_completed:
#                         continue
#
#                     reset = False
#
#                     if frecventa in ['Azi', 'Zilnic'] and NOW.day != last_completed.day:
#                         reset = True
#                     elif frecventa == 'Săptămânal' and NOW.isocalendar().week != last_completed.isocalendar().week:
#                         reset = True
#                     elif frecventa == 'Lunar' and NOW.month != last_completed.month:
#                         reset = True
#                     elif frecventa == 'Anual' and NOW.year != last_completed.year:
#                         reset = True
#
#                     if reset:
#                         if frecventa == 'Azi':
#                             cursor.execute('DELETE FROM tasks WHERE frecventa = %s', (frecventa,))
#                         else:
#                             cursor.execute(f'UPDATE tasks SET completed = FALSE WHERE nume = %s AND frecventa = %s AND timp = %s',
#                                        (nume, frecventa, timp))
#
#             conn.commit()
