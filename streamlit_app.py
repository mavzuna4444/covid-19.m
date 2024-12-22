import streamlit as st
import folium
import pandas as pd
import random
from datetime import datetime
from streamlit_folium import st_folium

# Генерация случайных данных для автобусов
stops = [
    "Улица Ленина", "Центральный рынок", "Площадь Республики", "ЖД Вокзал", "Университет",
    "Торговый центр", "Бульвар Мира", "Площадь Победы", "Мост через реку", "Автовокзал",
    "Государственная библиотека", "Ботанический сад", "Парк культуры", "Рынок Баракат",
    "Дворец спорта", "Музей истории", "Магазин электроники", "Стадион", "Сельский рынок",
    "Кинотеатр", "Школа №3", "Гимназия", "Фитнес клуб", "Зоопарк", "Государственная больница",
    "Магазин Окей", "Супермаркет Ашан", "Гармония", "Кафе \"Березка\""
]

# Количество новых строк для генерации
num_new_rows = 5000

# Функция для генерации случайных данных для автобусов
def generate_random_data():
    bus_id = random.randint(1000, 9999)  # случайный ID автобуса
    current_lat = random.uniform(38.5800, 38.6000)  # случайная широта
    current_lon = random.uniform(68.7800, 68.8200)  # случайная долгота
    next_stop = random.choice(stops)  # случайная остановка из списка
    time_to_next_stop = random.randint(5, 20)  # случайное время до следующей остановки
    return [bus_id, current_lat, current_lon, next_stop, time_to_next_stop]

# Генерация данных для автобусов
new_rows = [generate_random_data() for _ in range(num_new_rows)]
bus_data = pd.DataFrame(new_rows, columns=['bus_id', 'current_lat', 'current_lon', 'next_stop', 'time_to_next_stop'])

# Сохранение данных в CSV файл
bus_data.to_csv('bus_data.csv', index=False)

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_csv('bus_data.csv')

# Функция для отображения карты с автобусами и остановками
def show_map(bus_data):
    # Центр карты (примерный центр города Душанбе)
    map_center = [38.5833, 68.7869]
    bus_map = folium.Map(location=map_center, zoom_start=14)

    # Добавление остановок на карту
    for stop in stops:
        folium.Marker(
            location=[random.uniform(38.5800, 38.6000), random.uniform(68.7800, 68.8200)],
            popup=f'{stop}',
            icon=folium.Icon(color='blue', icon='cloud')
        ).add_to(bus_map)

    # Добавление автобусов на карту
    for _, bus in bus_data.iterrows():
        folium.Marker(
            location=[bus['current_lat'], bus['current_lon']],
            popup=f"Bus {bus['bus_id']} | Next stop: {bus['next_stop']} | Time to next stop: {bus['time_to_next_stop']} minutes",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(bus_map)
    
    return bus_map

# Заголовок и описание
st.title("Транспортная навигация: Отслеживание общественного транспорта")
st.write("""
    Это приложение позволяет отслеживать местоположение автобусов в реальном времени на основе симулированных данных.
    Вы можете увидеть ближайшие остановки и время до прибытия транспорта.
""")

# Sidebar для поиска
st.sidebar.header("Поиск")

# Поиск остановки
stop_search = st.sidebar.text_input("Поиск остановки:", "")
if stop_search:
    filtered_stops = [stop for stop in stops if stop_search.lower() in stop.lower()]
    st.sidebar.write(f"Результаты поиска для '{stop_search}':")
    for stop in filtered_stops:
        st.sidebar.write(stop)
else:
    st.sidebar.write("Введите название остановки для поиска.")

# Поиск автобуса
bus_search = st.sidebar.text_input("Поиск автобуса:", "")
if bus_search:
    bus_id_search = int(bus_search) if bus_search.isdigit() else None
    if bus_id_search:
        bus_info = bus_data[bus_data['bus_id'] == bus_id_search]
        if not bus_info.empty:
            st.sidebar.write(f"Информация для автобуса {bus_id_search}:")
            st.sidebar.write(bus_info[['bus_id', 'current_lat', 'current_lon', 'next_stop', 'time_to_next_stop']])
        else:
            st.sidebar.write(f"Автобус с ID {bus_id_search} не найден.")
    else:
        st.sidebar.write("Введите корректный номер автобуса.")
else:
    st.sidebar.write("Введите ID автобуса для поиска.")

# Загрузка данных
bus_data = load_data()

# Отображение карты с автобусами
bus_map = show_map(bus_data)

# Отображение карты в Streamlit
st_folium(bus_map, width=700)

# Опционально: кнопка для обновления данных
if st.button('Обновить данные'):
    # Симуляция обновления данных (в реальном проекте можно получать данные через API)
    bus_data['current_lat'] = bus_data['current_lat'] + random.uniform(-0.001, 0.001)
    bus_data['current_lon'] = bus_data['current_lon'] + random.uniform(-0.001, 0.001)
    st.write("Данные обновлены!")
    bus_map = show_map(bus_data)
    st_folium(bus_map, width=700)
