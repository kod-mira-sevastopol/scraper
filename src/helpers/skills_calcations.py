from datetime import datetime
import dateparser
from src.models.skills import Skill

def freelans(resume_text):
    if resume_text.lower().find('фриланс') == -1 and resume_text.lower().find('аутсорс') == -1:
        return Skill('Честный', 'good')
    else:
        return Skill('Не совпадения', 'bad')


def work_history(resume):
    try:
        between_months = 0
        for i in range(len(resume['jobs']) - 1):
            if resume['jobs'][i]["end_date"] == '':
                continue

            end_date = dateparser.parse(resume['jobs'][i]["end_date"])
            start_date = dateparser.parse(resume['jobs'][i]["start_date"])
            between_months += (start_date.year - end_date.year) * 12 + start_date.month - end_date.month

        if len(resume['jobs']) == 0:
            return Skill('Отсутствие опыта', 'bad')

        if between_months > len(resume['jobs']):
            return Skill('Непрерывная работа', 'good')
        else:
            return Skill('Пропуски в истории работы', 'middle')
    except Exception as e:
        return None

def middle_month_work(resume):
    middle_month_work = 0

    try:

        for i in range(len(resume['jobs']) - 1):
            if resume['jobs'][i]["end_date"] == '':
                continue

            if resume['jobs'][i]["end_date"].lower() == 'настоящее время':
                resume['jobs'][i]["end_date"] = datetime.now().strftime("%Y-%m-%d")

            end_date = dateparser.parse(resume['jobs'][i]["end_date"])
            start_date = dateparser.parse(resume['jobs'][i]["start_date"])
            middle_month_work += (end_date - start_date).days / 30

        middle_month_work = round(middle_month_work / len(resume['jobs']))
        if middle_month_work >= 8:
            return Skill('Верность', 'good')
        else:
            return Skill('В погоне за деньгами', 'bad')

    except Exception as ex:
        return None

def get_stack(resume):
    if (len(resume['stack']) <= 3):
        return Skill('Маленький стек', 'bad')

    if (len(resume['stack']) > 10):
        return Skill('Обширный стек', 'good')

def get_planing(resume):
    for item in resume['stack']:
        if item['name'].lower() == 'agile' or item['name'].lower() == 'scrum':
            return Skill('Планеровщик', 'good')