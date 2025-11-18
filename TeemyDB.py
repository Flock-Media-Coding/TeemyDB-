import json
from colorama import Fore, Style, init

# Инициализация colorama для цветного вывода
init(autoreset=True)

DATABASE_FILE = 'database.json'

# Загрузка данных
try:
    with open(DATABASE_FILE, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = []

def print_header(text):
    """ Заголовок """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Style.RESET_ALL}")

def print_success(message):
    """ Сообщение об успехе """
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    """ Сообщение об ошибке """
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_info(message):
    """ Информационное сообщение """
    print(f"{Fore.BLUE}→ {message}{Style.RESET_ALL}")

def save_data():
    """ Сохраняем изменения в файл """
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_person(name, surname, age, city):
    global data
    new_entry = {
        'id': len(data) + 1,
        'name': name,
        'surname': surname,
        'age': age,
        'city': city
    }
    data.append(new_entry)
    save_data()
    print_success(f'Пользователь {name} {surname} успешно добавлен.')

def view_all_people():
    if len(data) > 0:
        print_header("ВСЕ ЗАПИСИ В БАЗЕ ДАННЫХ")
        for entry in data:
            print(f"{Fore.CYAN}ID: {entry['id']}{Style.RESET_ALL}")
            print(f"  Имя: {entry['name']}")
            print(f"  Фамилия: {entry['surname']}")
            print(f"  Возраст: {entry['age']}")
            print(f"  Город: {entry['city']}")
            print("-" * 40)
        show_statistics()
    else:
        print_error('Нет записей в базе данных.')

def search_by_name(name):
    found_entries = [entry for entry in data if name.lower() in entry['name'].lower()]
    if found_entries:
        print_header(f"РЕЗУЛЬТАТЫ ПОИСКА ПО ИМЕНИ: '{name}'")
        for entry in found_entries:
            print(f"ID: {entry['id']}")
            print(f"  Имя: {entry['name']}")
            print(f"  Фамилия: {entry['surname']}")
            print(f"  Возраст: {entry['age']}")
            print(f"  Город: {entry['city']}")
            print("-" * 40)
    else:
        print_error(f'Записи с именем "{name}" не найдены.')

def search_by_surname(surname):
    found_entries = [entry for entry in data if surname.lower() in entry['surname'].lower()]
    if found_entries:
        print_header(f"РЕЗУЛЬТАТЫ ПОИСКА ПО ФАМИЛИИ: '{surname}'")
        for entry in found_entries:
            print(f"ID: {entry['id']}")
            print(f"  Имя: {entry['name']}")
            print(f"  Фамилия: {entry['surname']}")
            print(f"  Возраст: {entry['age']}")
            print(f"  Город: {entry['city']}")
            print("-" * 40)
    else:
        print_error(f'Записи с фамилией "{surname}" не найдены.')

def search_by_id(person_id):
    found_entries = [entry for entry in data if entry['id'] == person_id]
    if found_entries:
        print_header(f"РЕЗУЛЬТАТЫ ПОИСКА ПО ID: {person_id}")
        for entry in found_entries:
            print(f"ID: {entry['id']}")
            print(f"  Имя: {entry['name']}")
            print(f"  Фамилия: {entry['surname']}")
            print(f"  Возраст: {entry['age']}")
            print(f"  Город: {entry['city']}")
            print("-" * 40)
    else:
        print_error(f'Запись с ID "{person_id}" не найдена.')

def delete_person(person_id):
    global data
    filtered_data = [entry for entry in data if entry['id'] != person_id]
    if len(filtered_data) < len(data):
        data = filtered_data
        # Пересчитываем ID после удаления
        for i, entry in enumerate(data, 1):
            entry['id'] = i
        save_data()
        print_success(f'Пользователь с ID {person_id} удалён.')
    else:
        print_error(f'Пользователь с ID {person_id} не найден.')

def update_person(person_id, new_name=None, new_surname=None, new_age=None, new_city=None):
    global data
    updated = False
    for i, entry in enumerate(data):
        if entry['id'] == person_id:
            if new_name is not None:
                entry['name'] = new_name
            if new_surname is not None:
                entry['surname'] = new_surname
            if new_age is not None:
                entry['age'] = new_age
            if new_city is not None:
                entry['city'] = new_city
            updated = True
            break
    if updated:
        save_data()
        print_success(f'Данные пользователя с ID {person_id} обновлены.')
    else:
        print_error(f'Пользователь с ID {person_id} не найден.')

def show_statistics():
    """ Показать статистику по базе данных """
    if not data:
        print_error("Нет данных для статистики")
        return
    
    print_header("СТАТИСТИКА БАЗЫ ДАННЫХ")
    
    total_users = len(data)
    avg_age = sum(entry['age'] for entry in data) / total_users
    cities = {}
    age_groups = {'Дети (0-17)': 0, 'Молодежь (18-35)': 0, 'Взрослые (36-60)': 0, 'Пенсионеры (60+)': 0}
    
    for entry in data:
        # Статистика по городам
        city = entry['city']
        cities[city] = cities.get(city, 0) + 1
        
        # Статистика по возрастным группам
        age = entry['age']
        if age <= 17:
            age_groups['Дети (0-17)'] += 1
        elif age <= 35:
            age_groups['Молодежь (18-35)'] += 1
        elif age <= 60:
            age_groups['Взрослые (36-60)'] += 1
        else:
            age_groups['Пенсионеры (60+)'] += 1
    
    # Общая статистика
    print(f"{Fore.CYAN}📊 ОБЩАЯ СТАТИСТИКА:{Style.RESET_ALL}")
    print(f"  Всего пользователей: {total_users}")
    print(f"  Средний возраст: {avg_age:.1f} лет")
    
    # Статистика по городам
    print(f"\n{Fore.CYAN}🏙️  РАСПРЕДЕЛЕНИЕ ПО ГОРОДАМ:{Style.RESET_ALL}")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_users) * 100
        print(f"  {city}: {count} ({percentage:.1f}%)")
    
    # Статистика по возрастным группам
    print(f"\n{Fore.CYAN}👥 ВОЗРАСТНЫЕ ГРУППЫ:{Style.RESET_ALL}")
    for group, count in age_groups.items():
        if count > 0:
            percentage = (count / total_users) * 100
            print(f"  {group}: {count} ({percentage:.1f}%)")
    
    # Самый популярный город
    if cities:
        most_common_city = max(cities.items(), key=lambda x: x[1])
        print(f"\n{Fore.CYAN}🎯 САМЫЙ ПОПУЛЯРНЫЙ ГОРОД:{Style.RESET_ALL}")
        print(f"  {most_common_city[0]}: {most_common_city[1]} пользователей")

def display_menu():
    """ Отображение меню """
    print_header("Teemy DB - СИСТЕМА УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ")
    
    menu_items = [
        "1. Добавить запись",
        "2. Показать все записи",
        "3. Найти запись по имени",
        "4. Найти запись по фамилии",
        "5. Найти запись по ID",
        "6. Изменить запись",
        "7. Удалить запись",
        "8. Показать статистику",
        "9. Выход"
    ]
    
    for item in menu_items:
        print(f"{item}")

if __name__ == '__main__':
    print_header("Teemy DB - СИСТЕМА УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ")
    print_info(f"Загружено записей: {len(data)}                                     ")
    
    while True:
        display_menu()
        
        choice = input(f'\n{Fore.CYAN}Выберите пункт меню (1-9): {Style.RESET_ALL}')

        if choice == '1':
            print_header("ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ")
            name = input('Имя: ')
            surname = input('Фамилия: ')
            try:
                age = int(input('Возраст: '))
                city = input('Город: ')
                add_person(name, surname, age, city)
            except ValueError:
                print_error("Возраст должен быть числом!")

        elif choice == '2':
            view_all_people()

        elif choice == '3':
            print_header("ПОИСК ПО ИМЕНИ")
            name = input('Введите имя для поиска: ')
            search_by_name(name)

        elif choice == '4':
            print_header("ПОИСК ПО ФАМИЛИИ")
            surname = input('Введите фамилию для поиска: ')
            search_by_surname(surname)

        elif choice == '5':
            print_header("ПОИСК ПО ID")
            try:
                person_id = int(input('Введите ID для поиска: '))
                search_by_id(person_id)
            except ValueError:
                print_error("ID должен быть числом!")

        elif choice == '6':
            print_header("ИЗМЕНЕНИЕ ЗАПИСИ")
            try:
                person_id = int(input('ID пользователя для изменения: '))
                new_name = input('Новое имя (оставьте пустым, если менять не надо): ') or None
                new_surname = input('Новая фамилия (оставьте пустым, если менять не надо): ') or None
                new_age_input = input('Новый возраст (оставьте пустым, если менять не надо): ') or None
                new_age = int(new_age_input) if new_age_input else None
                new_city = input('Новый город (оставьте пустым, если менять не надо): ') or None
                update_person(person_id, new_name, new_surname, new_age, new_city)
            except ValueError:
                print_error("Возраст должен быть числом!")

        elif choice == '7':
            print_header("УДАЛЕНИЕ ЗАПИСИ")
            try:
                person_id = int(input('ID пользователя для удаления: '))
                delete_person(person_id)
            except ValueError:
                print_error("ID должен быть числом!")

        elif choice == '8':
            show_statistics()

        elif choice == '9':
            print_header("ВЫХОД ИЗ СИСТЕМЫ")
            print_success("Данные сохранены. До свидания!")
            break

        else:
            print_error('Неверный выбор пункта меню. Пожалуйста, выберите от 1 до 9.')