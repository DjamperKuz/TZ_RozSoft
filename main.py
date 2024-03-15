import datetime
import json


def get_last_job(json_data):
    max_date = datetime.date(1900, 1, 1)
    job_name = ''

    for item in json_data['data']:
        item_date = datetime.datetime.strptime(item['starttime'], '%Y-%m-%d').date()

        if item_date > max_date:
            max_date = item_date
            job_name = item['jobtitlename']

    return max_date, job_name


def get_job_post_without_grade(json_data):

    list_jobs_without_grade = []
    for item in json_data['data']:
        job_name = item['jobtitlename'].split()
        job_name.pop()

        list_jobs_without_grade.append({'job_name': ' '.join(job_name),
                                        'start_time': item['starttime']})

    return list_jobs_without_grade

def main():
    with open('data.json', 'r') as read_file:
        json_load = json.load(read_file)

    print('Самая последняя созданная должность: ')
    max_date, job_name = get_last_job(json_data=json_load)
    print(f'Должность - {job_name}, дата создания - {max_date}')

    print('\nСписок всех должностей без grade: ')
    list_jobs_without_grade = get_job_post_without_grade(json_data=json_load)
    for job in list_jobs_without_grade:
        print(f"Должность - {job['job_name']}, дата создания - {job['start_time']}")

    print('\nДата опследнего обновления статуса должности: ')


if __name__ == '__main__':
    main()
