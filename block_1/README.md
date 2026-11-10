Блок 1. Базовые команды и жизненный цикл

1.1 Запусти nginx в фоне так, чтобы он слушал порт 8080 на хосте. Проверь через curl, что страница отдаётся.

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker run -d -p 8080:80 --name block_1_nginx nginx:alpine
686d5c8048aef49fce6e710b9c36acc2d9201a8abf64b627f2583615d9b990bb

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ curl -I http://localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Tue, 10 Nov 2026 13:31:23 GMT
Content-Type: text/html
Content-Length: 896
Last-Modified: Wed, 21 Oct 2026 17:54:44 GMT
Connection: keep-alive
ETag: "6ad8fc64-380"
Accept-Ranges: bytes

1.2 Не останавливая контейнер, зайди внутрь через docker exec. Найди index.html и поменяй его содержимое прямо там.

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker exec -it block_1_nginx /bin/sh
/ # vi /usr/share/nginx/html/index.html 
/ # nginx -s reload
2026/11/10 13:46:53 [notice] 55#55: signal process started

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ curl http://localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, Simon has mastered Vim!<p>
<p> What a crazy muthafucka ! <p>
<p> Damn!!!!! So cool AF !!! <p>
<p> Hail to Master Daniel for this task!!! <p>
<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional 
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>


1.3 Снова проверь через curl. Потом сделай docker stop и docker start этого контейнера. Изменения сохранились или нет? Напиши почему (вспомни про writable layer).

- Конечно сохранились, так как к каждому контейнеру привязан свой writable слой который хранится до того, пока мы не удалим контейнер

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker stop block_1_nginx 
block_1_nginx
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker start block_1_nginx 
block_1_nginx
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ curl http://localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, Simon has mastered Vim!<p>
<p> What a crazy muthafucka ! <p>
<p> Damn!!!!! So cool AF !!! <p>
<p> Hail to Master Daniel for this task!!! <p>
<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional 
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

 
1.4 Удали контейнер. Запусти новый из alpine с командой sleep 1000. Через docker top посмотри процессы внутри. Почему у главного процесса PID = 1?

- Маленькая оговорка - PID 1 у процесса только внутри контейнера, так как для /proc используется отдельный namespace.
docker top показывает PIDы с номерами хоста - то есть без учета namespace.

docker rm block_1_nginx 
block_1_nginx
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker run -d --name sleepy_container alpine sleep 1000
74b04cff341574594b91c1f150763e1df7a17ce2ca2865e6aeb04b0b21239ae2
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_1$ docker top sleepy_container 
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                16552               16527               0                   17:15               ?                   00:00:00            sleep 1000
