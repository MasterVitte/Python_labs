import numpy as np
import json
from enum import Enum


class DataEnum(Enum):
    ARRAY = 'ARRAY'
    INTERVALS = 'INTERVALS'

FILE_PATH = 'data2.json'


def input_type():
    return input(f"Введите тип данных {DataEnum.ARRAY.value} или {DataEnum.INTERVALS.value} (1-2): ")

def input_file():
    operation_type = input_type()

    file_path = ''

    if operation_type == '1':
        file_path = 'data.json'
    elif operation_type == '2':
        file_path = 'data2.json'

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON в файле '{file_path}': {e}")
    except ValueError as e:
        print(f"Ошибка значения при чтении файла '{file_path}': {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка при чтении файла '{file_path}': {e}")


def input_keyboard():
    data: dict[str, list] = {
        "data": [],
        "type": input_type()
    }

    if data["type"] == DataEnum.ARRAY.value:
        data["data"] = [int(x) for x in input("Введите числа через пробел: ").split()]

    elif data["type"] == DataEnum.INTERVALS.value:
        num_values = int(input("Введите количество значений: "))

        for _ in range(num_values):
            print(f"Значение {_ + 1}:")
            start = float(input("Введите начало интервала: "))
            end = float(input("Введите конец интервала: "))
            frequency = float(input("Введите частоту: "))
            data["data"].append({"start": start, "end": end, "frequency": frequency})

    else:
        print("Неизвестный тип данных.")
        return

    return data


def show_data(data):
    data_type = data.get("type")

    if data_type == DataEnum.ARRAY.value:
        print("Содержимое файла:\n", np.array(data))
    elif data_type == DataEnum.ARRAY.value:
        print(np.array(data.get("data")))
    else:
        print("Неизвестный тип данных:", data_type)


def format_interval(start, end):
    return f"{start} ; {end}"


def calculate_variation_series(data):
    if data["type"] == DataEnum.ARRAY.value:
        return sorted(set(data["data"]))

    if data["type"] == DataEnum.ARRAY.value:
        return [format_interval(interval["start"], interval["end"]) for interval in data["data"]]


def display_variation_series(data):
    variation_series = calculate_variation_series(data)

    print("Вариационный ряд:", variation_series)


def calculate_frequency_distribution(data):
    variations = data["data"]
    variation_series = calculate_variation_series(data)
    frequencies = np.array([])
    relative_frequencies = np.array([])

    if data["type"] == DataEnum.ARRAY.value:
        frequencies = np.array([variations.count(value) for value in variations])
        relative_frequencies = frequencies / len(variations)

    if data["type"] == DataEnum.INTERVALS.value:
        frequencies = np.array([item["frequency"] for item in variations])
        relative_frequencies = frequencies / sum([item["frequency"] for item in variations])

    return variation_series, frequencies, relative_frequencies


def display_frequency_distribution(data):
    variation_series, frequencies, relative_frequencies = calculate_frequency_distribution(data)

    print("Статистический ряд частот:")
    for value, freq, rel_freq in zip(variation_series, frequencies, relative_frequencies):
        print(f"Значение: {value}, Частота: {freq}, Относительная частота: {rel_freq}")


def calculate_empirical_distribution(data):
    variation_series, frequencies, _ = calculate_frequency_distribution(data)

    sum_frequencies = len(data)

    probability_distribution = frequencies / sum_frequencies
    cumulative_distribution = np.cumsum(frequencies) / sum_frequencies

    return variation_series, probability_distribution, cumulative_distribution


def calculate_weighted_mean(xi_values, ni_values):
    return sum(xi * ni for xi, ni in zip(xi_values, ni_values)) / sum(ni_values)


def calculate_variance(xi_values, ni_values, mean):
    return sum(ni_values[i] * ((xi_values[i] - mean) ** 2) for i in range(len(xi_values))) / sum(ni_values)


def calculate_average_values(xi_values):
    return [(xi + xi_next) / 2 for xi, xi_next in zip(xi_values[:-1], xi_values[1:])]


def calculate_numerical_characteristics(data):
    mean = np.array([])
    variance = np.array([])
    std_deviation = np.array([])

    if data["type"] == DataEnum.ARRAY.value:
        variations = np.array(data["data"])

        mean = np.mean(variations)
        variance = np.var(variations)
        std_deviation = np.std(variations)

    if data["type"] == DataEnum.INTERVALS.value:
        variations = np.array([item["frequency"] for item in data["data"]])

        array = [start_interval for interval in data["data"] for start_interval in (interval["start"], interval["end"])]

        for interval in data["data"]:
            start_interval = interval["start"]
            end_interval = interval["end"]
            array.append(start_interval)
            array.append(end_interval)

        xi_values = list(set(array))
        ni_values = list(variations)

        average_values = calculate_average_values(xi_values)

        mean = calculate_weighted_mean(average_values, ni_values)
        variance = calculate_variance(average_values, ni_values, mean)
        std_deviation = np.sqrt(variance)

    return mean, variance, std_deviation


def display_numerical_characteristics(data):
    mean, variance, std_deviation = calculate_numerical_characteristics(data)

    print("\nЧисловые характеристики выборки:")
    print("Среднее значение (x̄):", mean)
    print("Дисперсия (D):", variance)
    print("Стандартное отклонение (σ):", std_deviation)


def display_menu_input():
    print("1. Ввод из файла")
    print("2. Ввод с клавиатуры")


def display_menu_main():
    print("\nМеню:")
    print("1. Вывести содержимое файла")
    print("2. Вывести вариационный ряд")
    print("3. Вывести статистический ряд частот и относительных частот")
    print("4. Вывести числовые характеристики выборки")
    print("0. Выход")


def main():
    data = {}

    while True:
        display_menu_input()
        choice = input("Выберите пункт меню (1-2): ")
        if choice == '0':
            print("Программа завершена.")
            break
        elif choice == '1':
            data = input_file()
            break
        elif choice == '2':
            data = input_keyboard()
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите 1 или 2.")

    while True:
        display_menu_main()
        choice = input("Выберите пункт меню (0-8): ")

        if choice == '0':
            print("Программа завершена.")
            break
        elif choice == '1':
            show_data(data)
        elif choice == '2':
            display_variation_series(data)
        elif choice == '3':
            display_frequency_distribution(data)
        elif choice == '4':
            display_numerical_characteristics(data)
        else:
            print("Некорректный выбор. Пожалуйста, выберите от 0 до 8.")


if __name__ == "__main__":
    main()