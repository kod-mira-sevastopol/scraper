from src.models.resume import Resume

import src.helpers.skills_calcations as skills_calcs

class AnalyzeService:
    def __init__(self, resume_text: str, resume: Resume):
        self.resume_text = resume_text
        self.resume = resume

    def analyze(self):
        skills = self.__get_skills()
        return skills

    def __get_skills(self):
        skills = []

        work_history = skills_calcs.work_history(self.resume)
        middle_month = skills_calcs.middle_month_work(self.resume)
        freelans = skills_calcs.freelans(self.resume_text)
        stack = skills_calcs.get_stack(resume=self.resume)

        if work_history is not None:
            skills.append(work_history)

        if middle_month is not None:
            skills.append(middle_month)

        if freelans is not None:
            skills.append(freelans)

        if stack is not None:
            skills.append(stack)

        return skills