import operator
import itertools

EMPTY_COLUMN = {
    'columns': 1,
}


def build_column_from_shift(shift):
    return {
        'columns': shift.shift_length,
    }


def get_num_columns(data):
    return sum(item['columns'] for item in data)


def shifts_to_tabular_data(shifts):
    data = []
    shifts = sorted(shifts, key=operator.attrgetter('start_time'), reverse=True)

    while get_num_columns(data) < 24:
        current_column = get_num_columns(data)
        if shifts:
            shift = shifts.pop()
            start_column = shift.start_time.hour
            column = build_column_from_shift(shift)
        else:
            start_column = 24
            column = None

        for i in range(current_column, start_column):
            data.append(EMPTY_COLUMN)

        if column:
            data.append(column)

    return data


def group_shifts(qs):
    shifts = qs.order_by(
        'start_time__year',
        'start_time__month',
        'start_time__day',
        'department',
        'shift_length',
        'start_time',
        'start_time__minute',
        'start_time__second'
    )
    date_getter = lambda shift: shift.start_time.date() 
    department_getter = lambda shift: shift.department
    length_getter = lambda shift: shift.shift_length
    start_getter = lambda shift: shift.start_time.time()

    date_groups = itertools.groupby(shifts, date_getter)

    for date, shifts_by_date in date_groups:
        department_groups = itertools.groupby(shifts_by_date, department_getter)
        for department, shifts_by_departments in department_groups:
            length_groups = itertools.groupby(shifts_by_department, length_getter)
            for length, shifts_by_length in length_groups:
                yield date, department, length, shifts_to_tabular_data(shifts_by_length)

