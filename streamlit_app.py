import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
import random
from datetime import datetime
# Количество новых строк, которые нужно добавить
num_new_rows = 1000  # Добавим 1000 новых автобусов

# Функция для генерации случайных данных
def generate_random_data():
    bus_id = random.randint(1000, 9999)  # случайный ID автобуса
    current_lat = random.uniform(38.5800, 38.6000)  # случайная широта
    current_lon = random.uniform(68.7800, 68.8200)  # случайная долгота
    next_stop = random.choice(['Stop 1', 'Stop 2', 'Stop 3', 'Stop 4'])  # случайная остановка
    time_to_next_stop = random.randint(5, 20)  # случайное время до следующей остановки
    return [bus_id, current_lat, current_lon, next_stop, time_to_next_stop]

# Генерация новых данных
new_rows = [generate_random_data() for _ in range(num_new_rows)]

# Создание нового DataFrame
new_data = pd.DataFrame(new_rows, columns=['bus_id', 'current_lat', 'current_lon', 'next_stop', 'time_to_next_stop'])

# Сохранение данных в CSV файл
new_data.to_csv('bus_data.csv', index=False)

print("Данные успешно сгенерированы и сохранены в bus_data.csv")

# Загрузка данных
@st.cache_data
def load_data():
    # Убедитесь, что файл в корневой папке проекта
    return pd.read_csv('bus_data.csv')

# Отображение карты с автобусами
def show_map(bus_data):
    # Центр карты (примерный центр города Душанбе)
    map_center = [38.5833, 68.7869]
    bus_map = folium.Map(location=map_center, zoom_start=14)

    # Остановка маршрутов
    stops = {
        'Stop 1': [38.5820, 68.7866],
        'Stop 2': [38.5865, 68.7945],
        'Stop 3': [38.5900, 68.8000],
        'Stop 4': [38.5950, 68.8050],
    }
    
    # Добавление остановок на карту
    for stop, coords in stops.items():
        folium.Marker(
            location=coords,
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
    Это приложение позволяет отслеживать местоположение автобусов в реальном времени
    на основе симулированных данных. Вы можете увидеть ближайшие остановки и время до
    прибытия транспорта.
""")

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
