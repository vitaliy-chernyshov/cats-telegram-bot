# cats-telegram-bot
телеграм-бот для отправки котиков.

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

Умеет:
* откликаться на `/start` - приветственное сообщение
* по команде `/cat` отправляет рандомного котика
* отображает клавиатуру с выбором типа сообщения (gif, jpg)

перед запуском переименовать .env_example в .env и заполнить переменные. 
Возможные варианты `MODE - dev|prod`. В режиме prod бот готов к развертыванию на heroku. 

###Используемые технологии:
* Python
* API telegram, thecatapi.com
* Heroku для деплоя бота