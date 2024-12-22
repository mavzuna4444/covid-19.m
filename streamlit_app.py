import streamlit as st
import pandas as pd
import random
import geopy.distance

# Инициализация данных (если еще не были загружены)
if 'bus_data' not in st.session_state:
    bus_data = pd.DataFrame([
        {'bus_id': random.randint(1000, 9999),
         'current_lat': random.uniform(38.5800, 38.6000),
         'current_lon': random.uniform(68.7800, 68.8200),
         'arrival_time': pd.Timestamp.now() + pd.Timedelta(minutes=random.randint(1, 30))}
        for _ in range(500)
    ])
    st.session_state.bus_data = bus_data
else:
    bus_data = st.session_state.bus_data

# Заголовок и описание
st.title("Транспортная Навигация")
st.write("Используйте приложение для отслеживания автобусов и остановок в городе.")

# Сайдбар
st.sidebar.header("Поиск")
search_option = st.sidebar.selectbox('Выберите опцию поиска:', ['Поиск остановки', 'Поиск автобуса'])

# Функции для поиска
def search_stop(stop_name):
    return bus_data[bus_data['bus_id'].astype(str).str.contains(stop_name)]

def search_bus(bus_id):
    return bus_data[bus_data['bus_id'] == bus_id]

# Поиск остановки
if search_option == 'Поиск остановки':
    stop_name = st.sidebar.text_input('Введите название остановки:')
    if stop_name:
        stops_found = search_stop(stop_name)
        if not stops_found.empty:
            st.write("Найденные остановки:")
            st.write(stops_found)
        else:
            st.write("Остановки не найдены.")

# Поиск автобуса
if search_option == 'Поиск автобуса':
    bus_id = st.sidebar.number_input('Введите ID автобуса:')
    if bus_id:
        bus_found = search_bus(bus_id)
        if not bus_found.empty:
            st.write(f"Информация о автобусе с ID {bus_id}:")
            st.write(bus_found)
        else:
            st.write(f"Автобус с ID {bus_id} не найден.")

# Кнопка для обновления данных
if st.button('Обновить данные'):
    # Генерация случайных данных для обновления
    new_data = pd.DataFrame([
        {'bus_id': random.randint(1000, 9999),
         'current_lat': random.uniform(38.5800, 38.6000),
         'current_lon': random.uniform(68.7800, 68.8200),
         'arrival_time': pd.Timestamp.now() + pd.Timedelta(minutes=random.randint(1, 30))}
        for _ in range(50)  # Дополнительные данные
    ])
    # Обновление данных в session_state
    st.session_state.bus_data = pd.concat([bus_data, new_data], ignore_index=True)
    st.write("Данные обновлены!")

# Отображение данных
st.write(st.session_state.bus_data)

# Добавление функции для отображения времени прибытия
def get_arrival_time(bus_id):
    bus_info = bus_data[bus_data['bus_id'] == bus_id]
    if not bus_info.empty:
        arrival_time = bus_info['arrival_time'].values[0]
        time_left = arrival_time - pd.Timestamp.now()
        return f"Время прибытия: {arrival_time.strftime('%H:%M:%S')} ({time_left.seconds // 60} мин до прибытия)"
    else:
        return "Автобус не найден."

# Пример вывода времени прибытия для конкретного автобуса
bus_id_input = st.sidebar.number_input('Введите ID автобуса для времени прибытия:', 1000, 9999)
if bus_id_input:
    arrival_info = get_arrival_time(bus_id_input)
    st.sidebar.write(arrival_info)

