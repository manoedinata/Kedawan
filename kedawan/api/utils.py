import random
import string

def generateSlug() -> str:
    availableLength = [5, 6]
    length = random.choice(availableLength)

    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))
