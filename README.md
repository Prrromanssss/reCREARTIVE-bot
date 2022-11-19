# reCREARTIVE


![flake8 test](https://github.com/Prrromanssss/reCREARTIVE_bot/actions/workflows/python-package.yml/badge.svg)


## Contens
* [About](#about)
* [Functonal](#functional)
  * [Tasks](#tasks)
  * [Notifications](#notifications)
  * [Stickers](#stickers)
* [Deployment instructions](#deployment-instructions)
  * [Cloning project](#1-cloning-project-from-github)
  * [Activation venv](#2-creation-and-activation-venv)
  * [Requirements](#3-installation-all-requirements)
  * [.Env](#4-generate-file-with-virtual-environment-variables-env)
  * [Running](#5-running-project)
  * [Deployment](#6-deployment)




## About
Привет, тебя встречает команда __reCREARTIVE__!

Мы создали бота, который будет тренировать твою креативность
и делиться с тобой взглядом на мир разных художников.

Решай задания или просто посмотри на мир так, как это делали
разные художники, а потом
попробуй воспользоваться их методами.

Нажимай кнопку, чтобы получить задание на день или придумай
свое и напиши его нам.Кто знает, кому оно попадется  :)

Так же, если вы хотите получать каждый день новое задание
просто нажмите кнопку "notify", и вы будете становиться
креативными каждый день

P.s. : Кстати, можешь накидать нам любимых стикеров, чтобы наше общение
было веселее!



## Functional

* __/help__ - помощь (узнать доступные команды)

### Tasks
* __/get_task__ - получить задание
* __/write_task__- прислать задание, которое получит другой участник
* __/confirm__ - подтвердить задание (а вдруг вы ошиблись :) )
* __/not_confirm__ - отменить запись задания (и вправду ошиблись :( )

"confirm" и "not_confirm" используются после кнопки "write_task".

### Notifications
* __/notify_settings__ - настроить уведомления (ты же не хочешь, чтобы мы тебя разбудили? Настрой часовой пояс и время отправки уведомлений) или узнать о уже выбранном времени
* __/notify__ - включить уведомления
* __/exist_notify__ - узнать о существующих уведомлениях (а вдруг
 ты все уже настроил? )
* __/not_notify__ - выключить уведомления (после этого уведомления будут выключены)

### Stickers
* __/stickers__ - настроить любимые стикеры (данные стикеры будут приходить вместе с остальными сообщениями)
* __/add_stickers__ - добавить стикеры (после нажатия данной кнопки стикеры будут добавлены в вашу коллекцию)
* __/del_stickers__ - удалить стикеры (когда они тебе надоели)
* __/stop_stickers__ - остановить отправку стикеров (когда хочется
поговорить серьезнее). Используется после кнопок "add_stickers" и "del_stickers".


## Deployment instructions


### 1. Cloning project from GitHub

1.1 Run this command
```commandline
git clone https://github.com/Prrromanssss/reCREARTIVE_bot.git
```

### 2. Creation and activation venv

2.1 First of all, from root directory run this command
```commandline
python -m venv venv
```
2.2 Then run this command to activate venv
#### Mac OS / Linux
```commandline
source venv/bin/activate
```
#### Windows
```commandline
.\venv\Scripts\activate
```

### 3. Installation all requirements

3.3 Run this command 
```commandline
pip install -r requirements.txt
```

### 4. Generate file with virtual environment variables (.env)

4.1 Generate file '.env' in root directory with structure specified in the 'examples/env_example.txt' file


### 5. Running project

5.1 Run this command
```commandline
python main.py
```
***

### 6. Deployment

6.1 This bot was deployed to heroku, but from November 28, free heroku Dynos no longer available :(
