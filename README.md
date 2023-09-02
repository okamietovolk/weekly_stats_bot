# Бот для любителей статистики

Бот берет статистику из:
1. экспорт.zip из apple здоровье
2. Книги с bookmate.ru
3. Фильмы с letterboxd
4. Топ-трек с last-fm.

Парсеры находятся в scripts/parsers.py, парсер Apple HealthKit - scripts/utils.py. 

Данные healthkit экспортируются с помощью [healthkit-to-sqlite](https://github.com/dogsheep/healthkit-to-sqlite)