# Coursera Dump

Данный скрипт парсит данные случайных курсов с сайта [Coursera](https://www.coursera.org) и создает xlsx файл с собранными данными по переданному скрипту адресу.

Принцип работы: выбираем 20 случайных курсов из [xml-фида Курсеры](https://www.coursera.org/sitemap~www~courses.xml), затем заходим на страницы выбранных курсов и парсим их данные.

Программа извлекает из страницы: 
 * название курса;
 * язык;
 * ближайшую дату начала;
 * количество недель;
 * среднюю оценку.  

Полученные данные выгружаются в xlsx-файл.

## Использование
Запуск через терминал, при помощи python 3:

    python3.5 coursera.py <xlsx_output_location>(необязательно)

Если путь для файла с результатом работы не будет указан явно, в папке со скриптом будет создан файл с именем 'Random coursera courses (текущая дата)'.



# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
