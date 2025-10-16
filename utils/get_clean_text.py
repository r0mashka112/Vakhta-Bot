import re

def get_clean_text(text):
    return re.sub(r'[^\w\s]', '', text)\
        .strip()