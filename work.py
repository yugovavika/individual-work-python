FILENAME = "base.txt"
DELIMITER = "|" 

INITIAL_RECORDS = []


def initialize_file():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            pass 
    except FileNotFoundError:
        try:
            with open(FILENAME, 'w', encoding='utf-8') as f:
                for record in INITIAL_RECORDS:
                    f.write(record + "\n")
            print(f"[Успех] Файл '{FILENAME}' создан.")
        except IOError as e:
            print(f"[Ошибка] Не удалось создать файл '{FILENAME}': {e}")

def load_data():
    data = []
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.strip().split(DELIMITER)
                if len(p) == 9:
                    data.append({
                        'last_name': p[0],
                        'first_name': p[1],
                        'middle_name': p[2], 
                        'b_year': p[3], 
                        'b_month': p[4],
                        'b_day': p[5],
                        'rank': int(p[6]),
                        'wins': int(p[7]),
                        'country': p[8]
                    })
    except FileNotFoundError:
        print(f"[Ошибка] Файл '{FILENAME}' не найден. Пожалуйста, запустите программу заново для его создания.")
    except ValueError as e:
        print(f"[Ошибка] Ошибка преобразования данных в файле '{FILENAME}': {e}. Проверьте целостность данных.")
    except IOError as e:
        print(f"[Ошибка] Проблема с доступом к файлу '{FILENAME}': {e}")
    return data

def shaker_sort(arr, compare_func):
    n = len(arr)
    if n <= 1:
        return

    left, right = 0, n - 1
    while left < right:
        swapped = False

        for i in range(left, right):
            if compare_func(arr[i], arr[i+1]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
        right -= 1
        
        if not swapped:
            break
        
        swapped = False
        
        for i in range(right, left, -1):
            if compare_func(arr[i-1], arr[i]):
                arr[i-1], arr[i] = arr[i], arr[i-1]
                swapped = True
        left += 1
        
        if not swapped:
            break

def cmp_report_1_3(a, b):
    if a['rank'] < b['rank']: return True
    if a['rank'] > b['rank']: return False
    return a['last_name'].lower() > b['last_name'].lower()

def cmp_report_2(a, b):
    if a['wins'] < b['wins']: return True 
    if a['wins'] > b['wins']: return False 
    
    if a['rank'] < b['rank']: return True 
    if a['rank'] > b['rank']: return False 
    
    return a['last_name'].lower() > b['last_name'].lower()

def display_table(records, title):
    if not records:
        print(f"\n--- {title} ---\nСписок пуст или не содержит подходящих записей.")
        return

    header_len = 15 + 12 + 15 + 18 + 6 + 6 + 15 + 6
    print(f"\n{'=' * header_len}")
    print(f" {title}")
    print(f"{'=' * header_len}")
    print(f"{'Фамилия':15} | {'Имя':12} | {'Отчество':15} | {'Дата рожд.(Г.М.Ч)':18} | {'Разряд':6} | {'Побед':6} | {'Страна'}")
    print(f"{'-' * header_len}")
    
    for r in records:
        date_str = f"{r['b_year']}.{r['b_month']}.{r['b_day']}"
        print(f"{r['last_name']:15} | {r['first_name']:12} | {r['middle_name']:15} | {date_str:18} | {r['rank']:6} | {r['wins']:6} | {r['country']}")
    print(f"{'=' * header_len}\n")

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Ошибка: Ввод не может быть пустым. Пожалуйста, введите число.")
                continue
            
            num = int(value)
            
            if min_val is not None and num < min_val:
                print(f"Ошибка: Число должно быть не меньше {min_val}.")
                continue
            if max_val is not None and num > max_val:
                print(f"Ошибка: Число должно быть не больше {max_val}.")
                continue
            
            return num
        except ValueError:
            print("Ошибка: Введите целое число.")

def menu():
    initialize_file()

    while True:
        print("\n--- МЕНЮ 'ШАХМАТНОЕ СОРЕВНОВАНИЕ' ---")
        print("1. Полный список участников (Разряд убыв., Фамилия Возраст.)")
        print("2. Список участников определенной страны (Победы убыв., Разряд убыв., Фамилия Возраст)")
        print("3. Список участников по диапазону разрядов (Разряд убыв., Фамилия Возраст)")
        print("0. Выход из программы")
        
        choice = input("\nВыберите пункт меню: ").strip()
        
        if choice == '0':
            print("Завершение работы программы.")
            break

        all_participants = load_data()
        if not all_participants:
            print("Не удалось загрузить данные участников. Проверьте файл 'chess_database.txt'.")
            continue

        if choice == '1':
            report_data = list(all_participants) 
            shaker_sort(report_data, cmp_report_1_3)
            display_table(report_data, "ПОЛНЫЙ СПИСОК УЧАСТНИКОВ")
            
        elif choice == '2':
            country_name = input("Введите название страны для фильтрации: ").strip()
            if not country_name:
                print("Название страны не может быть пустым.")
                continue
            
            filtered_data = [p for p in all_participants if p['country'].lower() == country_name.lower()]
            
            if filtered_data:
                report_data = list(filtered_data)
                shaker_sort(report_data, cmp_report_2)
                display_table(report_data, f"УЧАСТНИКИ ИЗ СТРАНЫ: {country_name.upper()}")
            else:
                print(f"\n--- Участники из страны '{country_name}' не найдены. ---\n")
                
        elif choice == '3':
            print("\n--- Введите диапазон разрядов ---")
            n1 = get_int_input("Введите нижнюю границу разряда (N1): ")
            n2 = get_int_input("Введите верхнюю границу разряда (N2): ")
            start_rank, end_rank = min(n1, n2), max(n1, n2)
            filtered_data = [p for p in all_participants if start_rank <= p['rank'] <= end_rank]
            
            if filtered_data:
                report_data = list(filtered_data)
                shaker_sort(report_data, cmp_report_1_3)
                display_table(report_data, f"УЧАСТНИКИ С РАЗРЯДОМ ОТ {start_rank} ДО {end_rank}")
            else:
                print(f"\n--- Участники с разрядом в диапазоне от {start_rank} до {end_rank} не найдены. ---\n")
                
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт из меню (0-3).")

if __name__ == "__main__":
    menu()

