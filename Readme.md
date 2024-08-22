# GitHub Parser
Отображение топ 100 публичных репозиториев из GitHub

## Использование

Создать .env фаил:
```
Пример заполнения в файле .env.sample
```
Создание яндекс функции (в корне проекта):
```
yc serverless function create --name=<имя_функции>
в консоли появится информация:
id
folder_id
```
Создать версию функции:
```
yc serverless function version create \
  --function-name=<имя_функции> \
  --runtime python312 \
  --entrypoint parser.handler \
  --memory 128m \
  --execution-timeout 5s \
  --source-path parser.zip
```

Создать таймер, который вызывает функцию раз в час:
```
yc serverless trigger create timer \
  --name <имя_таймера> \
  --cron-expression '0 * ? * * *' \
  --payload <сообщение> \
  --invoke-function-id <id> \ Информация
  --invoke-function-service-account-id <folder_id>
```

## Запуск проекта через docker-compose

Для запуска через docker-compose выполнить команду находясь в корне проекта:
```
docker-compose up
```
