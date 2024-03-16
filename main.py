import datetime
import json


def get_last_job_title_name(json_data):
    """
    Аргументы:

    json_data: Словарь JSON с данными о должностях. Должен содержать ключ 'data', который является списком словарей.
    Каждый словарь в списке должен содержать поле 'starttime', содержащее дату создания
    должности, в формате '%Y-%m-%d', и поле 'jobtitlename', содержащее название должности.

    Возвращает:

    tuple: Кортеж, содержащий последнюю дату (last_date) и соответствующее ей название должности (job_title_name).
    Если json_data['data'] пустой, функция вернет 1 января 1900 года как дату и пустую строку как название должности.
    """

    last_date = datetime.date(1900, 1, 1)
    job_title_name = ''

    for item in json_data['data']:
        item_date = datetime.datetime.strptime(item['starttime'], '%Y-%m-%d').date()

        if item_date > last_date:
            last_date = item_date
            job_title_name = item['jobtitlename']

    return last_date, job_title_name


def get_job_post_without_grade(json_data):
    """
    Аргументы:

    json_data: Словарь JSON с данными о работах. Должен содержать ключ 'data', который является списком словарей.
    Каждый словарь в списке должен содержать поле 'starttime', содержащее дату создания должности,
    и поле 'jobtitlename', содержащее название должности в формате, где уровень может быть указан в конце названия,
    например, "Operations Manager Junior".

    Возвращает:

    Список словарей, содержащих названия должностей без указания уровня и даты обновления должностей.
    Каждый словарь в списке имеет ключи 'job_name' и 'start_time'.
    Если json_data['data'] пустой, функция вернет пустой список.
    """

    list_jobs_without_grade = []
    for item in json_data['data']:
        job_name = item['jobtitlename'].split()
        job_name.pop()

        list_jobs_without_grade.append({'job_name': ' '.join(job_name),
                                        'start_time': item['starttime']})

    return list_jobs_without_grade


def get_last_date_update_job_title_name(json_data: json, job_name: str):
    """
    Аргументы:

    json_data: Словарь JSON с данными о должностях. Должен содержать ключ 'data', который является списком словарей.
    Каждый словарь в списке должен содержать поле 'starttime', содержащее дату создания должности,
    и поле 'jobtitlename', содержащее название должности в формате, где уровень может быть указан в конце названия,
    например, "Operations Manager Junior".

    job_name: Строка, представляющая название должности, для которой нужно найти последнюю дату обновления.

    Возвращает:

    Кортеж, содержащий последнее название должности (без указания уровня) и соответствующую ей последнюю дату обновления.
    Если указанная должность не найдена в данных json_data, возвращает пустую строку и 1 января 1900 года как дату.
    Если json_data['data'] пустой, функция также вернет пустую строку и 1 января 1900 года как дату.
    """

    list_jobs_without_grade = get_job_post_without_grade(json_data)

    last_date = datetime.date(1900, 1, 1)
    last_job_title_name = ''
    for job in list_jobs_without_grade:
        if job['job_name'] == job_name and (datetime.datetime.strptime(job['start_time'], '%Y-%m-%d').date() > last_date):
            last_date = datetime.datetime.strptime(job['start_time'], '%Y-%m-%d').date()
            last_job_title_name = job['job_name']

    return last_job_title_name, last_date


def main():
    with open('data.json', 'r') as read_file:
        json_load = json.load(read_file)

    print('Самая последняя созданная должность: ')
    max_date, job_name = get_last_job_title_name(json_data=json_load)
    print(f'Должность - {job_name}, дата создания - {max_date}')

    print('\nСписок всех должностей без grade: ')
    list_jobs_without_grade = get_job_post_without_grade(json_data=json_load)
    for job in list_jobs_without_grade:
        print(f"Должность - {job['job_name']}, дата создания - {job['start_time']}")

    print('\nДата последнего обновления должности Supervisor: ')
    last_job_title_name, last_date = get_last_date_update_job_title_name(json_data=json_load,
                                                                         job_name='Supervisor')
    print(f"Должность - {last_job_title_name},"
          f" дата последнего обновления - {last_date}")

    print('\nДата последнего обновления должности Operations Manager: ')
    last_job_title_name, last_date = get_last_date_update_job_title_name(json_data=json_load,
                                                                         job_name='Operations Manager')
    print(f"Должность - {last_job_title_name},"
          f" дата последнего обновления - {last_date}")


if __name__ == '__main__':
    main()
