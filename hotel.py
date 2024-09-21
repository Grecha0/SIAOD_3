import random

def create_hotel(budget_limit):
    return (random.randint(1, 5), random.randint(1, budget_limit))

def preliminary_selection(evaluation_count, budget_limit):
    top_rated_hotel = (1, budget_limit)  
    best_value_ratio = 1 / budget_limit  
    considered_hotels = [] 

    # Перебор заданного количества отелей
    for _ in range(evaluation_count):
        current_hotel = create_hotel(budget_limit)
        considered_hotels.append(current_hotel)  

        if (current_hotel[0] / current_hotel[1]) > best_value_ratio and current_hotel[0] >= top_rated_hotel[0]:
            top_rated_hotel = current_hotel
            best_value_ratio = current_hotel[0] / current_hotel[1]

    print("Отели, рассмотренные на этапе первичной оценки:")
    for hotel in considered_hotels:
        print(f'Рейтинг: {hotel[0]}, Цена: {hotel[1]}')

    return top_rated_hotel

def continuous_search(eval_hotels_count, budget_limit):

    best_initial_hotel = preliminary_selection(eval_hotels_count, budget_limit)
    print(f'\nЛучший отель после первичной оценки: {best_initial_hotel}\n')
    
    while True:
        new_hotel = create_hotel(budget_limit)
        print(f'Новый отель: Рейтинг {new_hotel[0]}, Цена {new_hotel[1]}')

        if new_hotel[0] >= best_initial_hotel[0] and new_hotel[1] <= best_initial_hotel[1]:
            print(f'\nНайден лучший отель: Рейтинг {new_hotel[0]}, Цена {new_hotel[1]}')
            return new_hotel

# Запуск программы поиска лучшего отеля с 10 итерациями оценки и бюджетом 1000
continuous_search(10, 1000)
