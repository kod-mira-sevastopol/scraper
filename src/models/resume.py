import json
import re

from src.models.achievements import Achievement
from src.models.contact import Contact
from src.models.jobs import Job
from src.models.person import Person
from src.models.stack import Stack
from src.models.stats import Stats

class Resume:
    def __init__(self, hh_url, person, contact, jobs, stack, educations, achievements, stats):
        self.hh_url = hh_url
        self.person = person
        self.contact = contact
        self.jobs = jobs
        self.stack = stack
        self.education = educations
        self.achievements = achievements
        self.stats = stats

    def to_dict(self):
        print(self.education)
        return {
            'hh-url': self.hh_url,
            'person': self.person.__dict__,
            'contact': self.contact.__dict__,
            'jobs': [job.__dict__ for job in self.jobs],
            'stack': [stack.__dict__ for stack in self.stack],
            'education': [edu for edu in self.education],
            'achievements': [desc.__dict__ for desc in self.achievements],
            'stats': self.stats.__dict__
        }

    @staticmethod
    def parse_json(data):
        data = json.loads(data)
        person = Person(
            data.get('firstname', None),
            data.get('middlename', None),
            data.get('lastname', None),
            data.get('date_of_birth', None),
            data.get('age', 0)
        )
        contact = Contact(
            data.get('email', None),
            data.get('phone', None),
            data.get('tg', '')
        )
        jobs = [
            Job(
                job.get('company', None),
                job.get('position', None),
                job.get('description', None),
                job.get('location', None),
                job.get('start_date', None),
                job.get('end_date', None)
            ) for job in data.get('jobs', [])
        ]
        stack = [
            Stack(stack_item)
            for stack_item in data.get('stack_list', [])
        ]
        '''
        skills = [
            Skill(
                skill.get('name', None),
                skill.get('type', None),
            ) for skill in data.get('skills', [])
        ]
        '''
        # degree = Education(data.get('degree', ''))
        education = [edu for edu in data.get('educations', [])]
        achievements = [
            Achievement(achievement)
            for achievement in data.get('achievements', [])
        ]

        exp_monts = data.get('experience_mounts', '')
        if isinstance(exp_monts, str):  # Check if exp_monts is a string
            experience_finded = re.findall(r'\d+', exp_monts)
            if len(experience_finded) > 0:
                experience = int(experience_finded[0]) * 12 - len(jobs) * 3
            else:
                experience = 0
        else:
            experience = 0

        stats = Stats(
            data.get('position', ''),
            experience,
            data.get('degree', '')
        )
        resume = Resume('', person, contact, jobs, stack, education, achievements, stats)

        return resume