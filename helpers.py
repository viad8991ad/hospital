from datetime import datetime, date
from re import sub
from random import choice
from logging import info as log_i

from constant import NEGATIVE, POSITIVE
from repo import find_new_directions, insert_receipt, insert_analyzes, insert_report, close_direction

regex = '[^A-Za-z0-9]+'


def check_data_from_str(value: str, type: str = ""):
    if value:
        if type == "date":
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return False
        elif type == "snils":
            line = sub(regex, '', value)
            if line.isdigit() and len(line) == 11:
                return line
            else:
                return False
        elif type == "polis":
            line = sub(regex, '', value)
            if line.isdigit() and len(line) == 16:
                return line
            else:
                return False
        elif type == "phone":
            line = sub(regex, '', value)
            if line.isdigit() and len(line) == 10:
                return line
            else:
                return False
        else:
            return value
    else:
        return False


def simulation():
    log_i(f'simulate work doctor')
    new_directions = find_new_directions()
    for direction in new_directions:
        receipt = insert_receipt(direction.doctor, direction.patient, random_receipt_description())
        analyzes = insert_analyzes(doctor=direction.doctor, patient=direction.patient,
                                   description=random_analyzes_description(), result=random_analyzes_result(),
                                   date=date.today())
        report = insert_report(direction.patient, direction, receipt, analyzes)
        log_i(f'for report {report.id} set receipt - {receipt.id} and analyzes - {analyzes.id}')
        close_direction(direction)


def random_receipt_description():
    list = ["рецепт 0", "рецепт 1", "рецепт 2", "рецепт 3"]
    return choice(list)


def random_analyzes_description():
    list = ["анализ 0", "анализ 1", "анализ 2", "анализ 3"]
    return choice(list)


def random_analyzes_result():
    list = [POSITIVE, NEGATIVE]
    return choice(list)
