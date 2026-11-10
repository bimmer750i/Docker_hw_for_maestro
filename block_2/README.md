Блок 2. Dockerfile и кэш

2.1 Напиши простое приложение на Flask или FastAPI. Один эндпоинт "/", возвращает {"status": "ok"}.

- Есть

2.2 Напиши под него Dockerfile. Требования:
- Базовый образ python:3.12-slim
- Сначала копируешь только requirements.txt и ставишь зависимости
- Потом уже весь остальной код
- CMD обязательно в exec-форме (через квадратные скобки напоминаю!!!!)
- Контейнер должен запускаться не от root. Создай пользователя через useradd и переключись на него через USER

2.3 Собери образ с тегом myapp:v1, замерь время сборки. Потом поменяй что-нибудь мелочь в коде приложения и собери заново. 
Снова замерь время. 
Какой слой взялся из кэша и почему?

---- Время сборки до изменения кода -----

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_2$ time docker build -t myapp:v1 .
[+] Building 16.7s (11/11) FINISHED                                                                docker:default
 => [internal] load build definition from Dockerfile                                                         0.0s
 => => transferring dockerfile: 314B                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                          0.0s
 => [internal] load .dockerignore                                                                            0.0s
 => => transferring context: 66B                                                                             0.0s
 => [1/6] FROM docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  1.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  0.0s
 => => extracting sha256:37fb86c2a767b88d500c6872195f88078f64765fe0d2f9cc375cc2efbd4c0a41                    0.5s
 => => extracting sha256:68bced9e0afa4479df17c3646e27c7c7e9ce9ba70c0e6c73b6826487b89037d9                    0.1s
 => => extracting sha256:2dc99d2d0a39fce31e37615eb4c932e16dcc4c2b0ce9993714280081b5dbe085                    0.3s
 => => extracting sha256:05e0eee5572e9c9f50408a2132590133b830a668a1cf2ff2b150f19c57707e2b                    0.0s
 => [internal] load build context                                                                            0.1s
 => => transferring context: 3.62kB                                                                          0.0s
 => [2/6] WORKDIR /app                                                                                       0.1s
 => [3/6] COPY requirements.txt .                                                                            0.1s
 => [4/6] RUN pip install -r requirements.txt                                                               13.2s
 => [5/6] COPY . .                                                                                           0.1s 
 => [6/6] RUN groupadd -g 10001 user &&     useradd -g 10001 user &&     chown -R user:user /app             0.4s 
 => exporting to image                                                                                       1.6s 
 => => exporting layers                                                                                      1.1s 
 => => exporting manifest sha256:6aaba72c8af200c13f5825c9ba5461f7677ecbbfc15b4eec48d251a6a12a201c            0.0s 
 => => exporting config sha256:c4141f0b099c591db27636f86e34efac4258b10af2e5d9408b51b8235216b5bc              0.0s 
 => => exporting attestation manifest sha256:433b0cb9f398945b68faf47462e03198a2f181cb4a30d488465e2644287e18  0.0s
 => => exporting manifest list sha256:5f3227b20851afa51f82fcb76ec074856fef8d3e88736bd78b225a48ec03b2e2       0.0s
 => => naming to docker.io/library/myapp:v1                                                                  0.0s
 => => unpacking to docker.io/library/myapp:v1                                                               0.3s

real	0m16.797s
user	0m0.138s
sys	0m0.085s

---- Время сборки ПОСЛЕ изменения кода (время не засёк, позор мне на мою пока еще не седую голову) ----

- Вышло 1.3 секунды - у нас не закешировались

COPY . . - так как поменялись файлы
RUN groupadd - так как поменялся предыдущий слой

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_2$ docker build -t myapp:v2 .
[+] Building 1.3s (11/11) FINISHED                                                                 docker:default
 => [internal] load build definition from Dockerfile                                                         0.0s
 => => transferring dockerfile: 314B                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                          0.0s
 => [internal] load .dockerignore                                                                            0.0s
 => => transferring context: 66B                                                                             0.0s
 => [1/6] FROM docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  0.0s
 => [internal] load build context                                                                            0.0s
 => => transferring context: 2.67kB                                                                          0.0s
 => CACHED [2/6] WORKDIR /app                                                                                0.0s
 => CACHED [3/6] COPY requirements.txt .                                                                     0.0s
 => CACHED [4/6] RUN pip install -r requirements.txt                                                         0.0s
 => [5/6] COPY . .                                                                                           0.0s
 => [6/6] RUN groupadd -g 10001 user &&     useradd -g 10001 user &&     chown -R user:user /app             0.5s
 => exporting to image                                                                                       0.4s
 => => exporting layers                                                                                      0.2s
 => => exporting manifest sha256:7b4814b1f2c590938e37bec29d0db2c91cd3e3dc3ae11bc5855eeddbe1a6dbc2            0.0s
 => => exporting config sha256:40d6ffaaa11a1eb7e4a4b088848a71aca402b9527d2e94542b45c756acc56658              0.0s
 => => exporting attestation manifest sha256:0c8bc2c587ae857b0c44f22718b7ce0471bfa24f24618b8478d4b2d0ffe5ff  0.0s
 => => exporting manifest list sha256:6b5b521dbf5ee67af9159ad1164d9a384316857066274c589c1d1a5ae89bf047       0.0s
 => => naming to docker.io/library/myapp:v2                                                                  0.0s
 => => unpacking to docker.io/library/myapp:v2

2.4 Добавь .dockerignore (убери __pycache__, .venv, .git и всё такое).

- Решил сделать его сразу

2.5 Небольшой эксперимент. Сначала напиши Dockerfile, где CMD написан в shell-форме: CMD nginx -g "daemon off;"
Собери, запусти, сделай docker stop и засеки, сколько времени тухнет. Потом поменяй на exec-форму: CMD ["nginx", "-g", "daemon off;"]
Снова собери, запусти, останови и сравни время. Напиши, почему разница есть.

- в этом же виде по причине docker-entrypoint.sh эксперимент провести не удалось, но опишу суть

1)  Shell форма делает PID 1 /bin/sh - как результат, сигналы обрабатывает /bin/sh и не отправляет их дочерним процессам
2)  EXEC форма от того так и называется - она запускает exec команды внутри CMD

- А так как при stop PID 1 получает SIGTERM и не отправляет его дочерним процессам, то docker по истечении
таймаута отправлит SIGKILL и будет таков. 
