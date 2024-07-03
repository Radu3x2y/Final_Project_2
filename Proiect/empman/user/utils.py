import random
from django.contrib.auth.models import User


def generate_unique_username(first_name, last_name):
    while True:
        rand_num = random.randint(100000, 999999)
        username = f"{first_name[0].lower()}{last_name.lower()}_{rand_num}"
        if not User.objects.filter(username=username).exists():
            break
    return username
