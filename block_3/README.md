Блок 3. Данные и сети

3.1 Сначала поиграйся с named volume. 
Создай volume, подключи его к nginx, положи туда свой index.html.

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_2$ docker volume create nginx-volume
nginx-volume

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Письмо Дженсену Хуангу</title>
</head>
<body>
  <h1>Дженсенг Хуанг! Соси мой хуй!!</h1>
  <button onclick="alert('Гоуп гоуп гоуп гоуп')">Лежать+Сосать</button>
</body>
</html>


semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ sudo cp -i index.html /var/lib/docker/volumes/nginx-volume/_data

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker run -d -v nginx-volume:/usr/share/nginx/html/ --name dizzy -p 80:80 nginx:alpine
9d2ba8e3a0caa645969417287a58e99aa7bf318781c099b841dc336f6a10c712

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker stop dizzy && docker rm $_
dizzy
dizzy

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker run -d -v nginx-volume:/usr/share/nginx/html/ --name dizzel -p 80:80 nginx:alpine
13d2e6463806ea91285dcb8def4e505d7356841640f38f789d1f3fc63b6de6d5
 
Удали контейнер, подними новый с тем же volume. 
Файл на месте?

- О да, Дженсен чувствует себя отлично (лежит+сосет, похотливая сучка)

Потом сделай bind mount (папка с хоста в контейнер).

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker run -d -p 80:80 -v ./index.html:/usr/share/nginx/html/index.html --name dizzel nginx:alpine
b1adcbbdf3d5db90490aac6259a118a871c03af98b6ae042db50b1b01eeafa14

Поменяй файл на хосте.

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Письмо Дженсену Хуангу</title>
</head>
<body>
  <h1>Дженсенг Хуанг! Соси мой хуй!!</h1>
  <button onclick="alert('О да, Семён, я готов быть твоим унитазом!!')">Отсосать у Сёмы</button>
</body>
</html>


Изменение сразу видно внутри контейнера без перезапуска?

- да, так как nginx заново читает один и тот же файл при обращении к нему
 
Напиши, что получилось и чем эти два подхода отличаются (не в рамках прода или компании нвидиа, просто фактически, как есть).

- по большому счету отличаются только путями и способом создания- путь на хосте и путь /var/lib/docker/volumes/<volume>/_data

3.2 Сети. Запусти два контейнера alpine в обычной сети (с sleep 1000). Попробуй из одного пингануть второй по имени контейнера. Получится?

- Хуюшки, ничего не получится, так они смотрят в дефолтный мост, где нет DNS резолвинга

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker run -d --name izzy alpine:latest sleep 900 
57853c799d597cbc68e8e2503d351bcecf81d5faf5b9854638583d37ea93850a
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker run -d --name pizzy alpine:latest sleep 900 
9bfe9e06ec9ab30546ed2833bdc082d56f9aa24fdec19aa1f26d8c07f84d3a3b
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker exec -it izzy /bin/sh
/ # ping dizzy
ping: bad address 'dizzy'
/ # getent hosts
/ #

...Поэтому я решил приготовить пиццу (да, я просто хочу кушац)


semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker network connect pizza izzy 
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker network connect pizza pizzy 
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_3$ docker exec -it izzy /bin/sh
/ # ping pizzy
PING pizzy (172.21.0.3): 56 data bytes
64 bytes from 172.21.0.3: seq=0 ttl=64 time=0.227 ms
64 bytes from 172.21.0.3: seq=1 ttl=64 time=0.272 ms
64 bytes from 172.21.0.3: seq=2 ttl=64 time=0.157 ms
^C
--- pizzy ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.157/0.218/0.272 ms
/ # 



Потом создай свою сеть через docker network create, перекинь туда оба контейнера и попробуй снова. Почему во втором случае заработало?

Потому что сеть pizza user-defined и поэтому в ней работает DNS-резолвинг


