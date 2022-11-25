# reCREARTIVE


![flake8 test](https://github.com/Prrromanssss/reCREARTIVE_bot/actions/workflows/python-package.yml/badge.svg)


## Contens
* [About](#about)
* [Functional](#functional)
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
* [Examples](#examples)




## About
Hi, the reCREARTIVE team is waiting for you!

We have created a bot that will train your creativity and share with you a look at the world of different artists.

Solve tasks or just look at the world the way different artists did, and then try to use their methods.

Press the button to get a task for the day or come up with your own and write it to us. Who knows who will get it :)

Also, if you want to receive a new task every day, just click the "notify" button, and you will become creative every day.

P.s. : By the way, you can throw us your favorite stickers to make our communication more fun!



## Functional

* __/help__ - help (learn available commands)

### Tasks
* __/get_task__ - get the task
![Image of the "get_task"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/get_task.png)
* __/write_task__- send the task that another participant will receive
![Image of the "write_task"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/write_task.png)
* __/confirm__ - confirm the task (what if you made a mistake :) )
![Image of the "confirm"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/confirm.png)
* __/not_confirm__ - cancel the task recording (and really made a mistake :( )
![Image of the "not_confirm"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/not_confirm.png)

After writing the task, it will be sent to the admins for confirmation or not.

* admin confirmation in admin chat

![Image of the "admin confirmation in the admin group"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/admin_confirm_group.png)

* admin confirmation in user chat

 ![Image of the "admin confirmation"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/admin_confirm.png)

 * admin non-confirmation in admin chat

![Image of the "admin non-confirmation in the admin group"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/admin_not_confirm_group.png)

 * admin non-confirmation in user chat

 ![Image of the "admin non-confirmation"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/admin_not_confirm.png)


"confirm" and "not_confirm" used after button "write_task".

### Notifications
* __/notify_settings__ - set up notifications (you don’t want us to wake you up, do you? Set up the time zone and time for sending notifications) or find out about the time already selected
![Image of the "notify_settingd"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/notify_settings.png)
* __/notify__ - enable notifications
![Image of the "notify number 1"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/notify_1.png)

![Image of the "notify number 2"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/notify_2.png)

![Image of the "notify number 3"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/notify_3.png)
* __/exist_notify__ - find out about existing notifications (and suddenly
have you set everything up yet? )
![Image of the "exist_notify"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/exist_notify.png)
* __/not_notify__ - turn off notifications (after that, notifications will be turned off)
![Image of the "not_notify"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/not_notify.png)

### Stickers
* __/stickers__ - set up your favorite stickers (these stickers will come with other messages)
![Image of the "stickers"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/stickers.png)

* __/add_stickers__ - add stickers (after clicking this button stickers will be added to your collection
* __/del_stickers__ - remove stickers (when you get tired of them)
![Image of the "add/del_stickers"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/add_stickers.png)
* __/stop_stickers__ - stop sending stickers (when you want
talk seriously). Used after buttons "add_stickers" and "del_stickers".
![Image of the "stop_stickers"](https://github.com/Prrromanssss/reCREARTIVE_bot/raw/master/media/stop_stickers.png)


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

### 6. Deployment

6.1 This bot was deployed to heroku, but from November 28, free heroku Dynos no longer available :(


## Examples

You can find some examples in the examples folder.
