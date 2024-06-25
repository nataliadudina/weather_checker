from random import choice

# Словарь для вывода прощального пожелания
goodbyes = [
    "Have a good day!",
    "Check that your head is not in the clouds.",
    "Enjoy the day and don't make storm in a teacup.",
    "Wishing you a productive day and clear the air if needed.",
    "May your heart be filled with joy today.",
    "Sunny disposition is a good remedy on rainy days."
]


def get_random_goodbye():
    # Получает случайное предложение из словаря goodbyes
    return choice(goodbyes)
