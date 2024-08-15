field=[[" "]*3 for i in range(3)]

def print_field():
    print('  | 0 | 1 | 2 |')
    print('---------------')
    for i,row in enumerate(field):
        row_str=f'{i} | {' | '.join(row)} | '
        print(row_str)
        print('---------------')
print_field()
def winner_check():
    for row in field:
            if row[0]==row[1]==row[2]!=' ':
                return row[0]
    for column in range(len(field)):
            if field[0][column]==field[1][column]==field[2][column]!=' ':
                return field[0][column]
    if field[0][0]==field[1][1]==field[2][2]!=' ':
            return field[0][0]
    if field[0][2]==field[1][1]==field[2][0]!=' ':
            return field[0][2]
    return None

def winner_print():
    winner_symbol=winner_check()
    if winner_symbol:
        print(f'Игрок №{1 if winner_symbol == "X" else 2} победил!')
        return True
    elif all(cell != ' ' for row in field for cell in row):
        print('Ничья!')
        return True
    return False

def value_input():
    valid=False
    while not valid:
        string_index=input('введи индекс строки, куда хочешь поставить символ')
        if string_index.isdigit():
            string_index=int(string_index)
            if string_index in (0, 1, 2):
                valid=True
            else:
                print('Индекс строки должен быть 0, 1 или 2')
        else:
            print('Введи только числовое значение для строки без других символов.')

    valid=False
    while not valid:
        column_index=input('введи индекс столбца, куда хочешь поставить символ')
        if column_index.isdigit():
            column_index=int(column_index)
            if column_index in (0, 1, 2):
                valid=True
            else:
                print('Индекс столбца должен быть 0, 1 или 2.')
        else:
            print('Введи только числовое значение для столбца без других символов.')

    return string_index, column_index

def game_start():
    step_number=1
    while True:
        print(f'Ход игрока №{2 if step_number % 2 == 0 else 1}')
        string_index, column_index=value_input()
        field_value = "O" if step_number % 2 == 0 else "X"
        if field[string_index][column_index] not in ["X", "O"]:
            field[string_index][column_index]=field_value
            print_field()
            if winner_print():
                break
            step_number+=1
        else:
            print('выбранная клетка уже занята, выбери другую')
            print_field()
game_start()