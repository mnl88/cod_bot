# FROM — задаёт базовый (родительский) образ
FROM python:3.8

# RUN - выполняет команду и создаёт слой образа. Используется для установки в контейнер пакетов
# WORKDIR — задаёт рабочую директорию для следующей инструкции
RUN mkdir -p /usr/src/app
# (-p тут означает, что мы создаем все папки из заданного пути)
WORKDIR /usr/src/app

# копирует в контейнер файлы и папки (в данном случае точка означает, что из нашей активной директории)
COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

# описывает команду с аргументами, которую нужно выполнить когда контейнер будет запущен.
# Аргументы могут быть переопределены при запуске контейнера. В файле может присутствовать лишь одна инструкция CMD
CMD ["python", "bot.py"]