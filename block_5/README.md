5.1 Запусти просто ubuntu без всяких флагов. Посмотри docker ps -a. Почему он сразу в Exited (0)? Как сделать, чтобы контейнер не умирал сразу после запуска?

- Потому что если мы посмотрим на COMMAND, то мы увидим /bin/bash - это означает, что мы просто
запустили  /bin/bash без аргументов НЕ в интерактивном режиме - в этом случае он просто завершил работу,
а значит, что завершился и процесс внутри контейнера с кодом 0 - и завершился и контейнер.


semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker run --name nigger_always_dies_first ubuntu:latest
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker ps -a
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                     PORTS     NAMES
7488ca8a0cf6   ubuntu:latest                 "/bin/bash"              3 seconds ago   Exited (0) 3 seconds ago             nigger_always_dies_first

5.2 Попробуй поднять два nginx на одном и том же порту 8080. Поймаешь ошибку. Через ss или lsof найди, кто порт занимает, и почини.

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker run -d -p 8080:80 --name nginx_1 nginx:alpine 
a3c0575b48a6f576c098a15131cf2564debd17a575198564bde1196fdad5ff2d

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker run -d -p 8080:80 --name nginx_2 nginx:alpine 
cc8cebc534cde384426754f4b67429eeff8bfdcd3a3841aa1bf6f2bbce1af641
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint nginx_2 (46f81e4e76678c17149e8f71409b6a92bc9ae3f2973d67859537df6b02bac630): Bind for :::8080 failed: port is already allocated

- чуда не случилось, посмотрим порты

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ sudo ss -tlpn | grep 8080
LISTEN 0      4096         0.0.0.0:8080      0.0.0.0:*    users:(("docker-proxy",pid=64691,fd=8))  
LISTEN 0      4096            [::]:8080         [::]:*    users:(("docker-proxy",pid=64698,fd=8)) 

- слушает его docker-proxy (и IPv6, и IPv4), но его убийство нам ничего не даст (как я сам выяснил на практике)
- вообще через него идет только лишь проброс портов в контейнер, так что нам остается либо остановить контейнер,
либо убить процесс внутри него - УБЕЙ ЕЁ, УБЕЙ ЕЁ!! (с) Красная королева из Обители Зла (2002)

- последуем ее совету (да, это немного извращенно, но мы вспоминаем команды и тыкаем docker)

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker top nginx_1 
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                64651               64624               0                   18:43               ?                   00:00:00            nginx: master process nginx -g daemon off;

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ sudo kill -15 64651
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

- УБИТ В ЖЕСТОКОЙ СХВАТКЕ!!

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker run -d -p 8080:80 --name nginx_2 nginx:alpine 
e649fce1c4efff80f5f6b38f3869b3aae9bfaade65f6df9711fb0082423f9b5d

- Боливард был слишком мал для них двоих, поэтому оставим только второй
- ЕЩЕ РАЗ: два контейнера не могут слушать один порт (проброшенный), поэтому мы оставляем только один
- Почему? Ограничения ядра - два процесса не могут слушать один порт, если нет флага SO_REUSE_PORTS

5.3 Запусти контейнер с лимитом памяти 50 мегабайт (--memory=50m) на python:3.12-slim. Внутри пусть крутится код, который жрёт память без остановки. Потом посмотри код выхода и через docker inspect проверь, убил ли его OOM Killer (поле OOMKilled).

- делаем Duckerfile

- а потом..

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ nano Dockerfile
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker build -t killer:v1 .
[+] Building 0.7s (8/8) FINISHED                                                                   docker:default
 => [internal] load build definition from Dockerfile                                                         0.0s
 => => transferring dockerfile: 120B                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                          0.0s
 => [internal] load .dockerignore                                                                            0.0s
 => => transferring context: 2B                                                                              0.0s
 => [1/3] FROM docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365df  0.0s
 => [internal] load build context                                                                            0.1s
 => => transferring context: 80B                                                                             0.0s
 => CACHED [2/3] WORKDIR /app                                                                                0.0s
 => [3/3] COPY killer.py .                                                                                   0.0s
 => exporting to image                                                                                       0.3s
 => => exporting layers                                                                                      0.1s
 => => exporting manifest sha256:6f491bef5418f1054d9cd7c7481f4f9c22c573d2b0065ee90d18bef99dec0638            0.0s
 => => exporting config sha256:80d676df606cd73a0da3c889238ea740e3b66af6ed44cbdd9e39305f2f71fa2f              0.0s
 => => exporting attestation manifest sha256:0cb74f1bf03ed4d38450c3fedecc0044d1f12d636a23d2953893eb08bbeb03  0.0s
 => => exporting manifest list sha256:c42cf89e2f54c291be77e7e9bacdcafd2df5cb98d91e43f546b6451c1818c570       0.0s
 => => naming to docker.io/library/killer:v1                                                                 0.0s
 => => unpacking to docker.io/library/killer:v1                                                              0.0s
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker run -d --memory=50m --name the_killers killer:v1 
4417d8cea0f7f230cf2ab85c91db56d2f30b7c456e71b153a1d5ce24438e8505
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker ps -a
CONTAINER ID   IMAGE                         COMMAND                  CREATED             STATUS                         PORTS     NAMES
4417d8cea0f7   killer:v1                     "python3 killer.py"      9 seconds ago       Exited (137) 8 seconds ago               the_killers

- Справедливость восторжествовала - убийца был убит - 137

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_5$ docker inspect the_killers | jq ".[0].State"
{
  "Status": "exited",
  "Running": false,
  "Paused": false,
  "Restarting": false,
  "OOMKilled": true,
  "Dead": false,
  "Pid": 0,
  "ExitCode": 137,
  "Error": "",
  "StartedAt": "2026-11-11T16:16:24.534978421Z",
  "FinishedAt": "2026-11-11T16:16:24.96681827Z"
}

5.4 Ты пересобрал образ с тем же тегом, а docker restart старого контейнера ничего не поменял. Почему так? Как правильно заставить контейнер подхватить новый образ?

- restart лишь перезапускает остановленный контейнер (увидел в man) без пересоздания образа, в отличие от compose, который эти изменения отслеживает
- поэтому единтсвенный правильный вариант это
1) снова build
2) снова run

