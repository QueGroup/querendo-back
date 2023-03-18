from datetime import datetime

from config.celery import app
from .models import QueUser


@app.task()
def check_age():
    users = QueUser.objects.all()
    for user in users:
        birth_date = user.birthday
        now_date = datetime.now()
        if user.age.isnull():
            user.age = now_date.year - birth_date.year
            user.save()
        elif birth_date.day == now_date.day and birth_date.month == now_date.month and birth_date.year != now_date.year:
            new_age = now_date.year - birth_date.year
            user.age = new_age
            user.save()
