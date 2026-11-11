4.1 Собери стек в compose.yaml из трёх сервисов:
- app (твой myapp:v1, порт 8000)
- db (postgres:16)
- adminer

Нужно:
- У app переменная окружения DB_HOST=db

- В коде связи с БД нет, но переменную я добавил

- У postgres volume для данных и healthcheck через pg_isready (внимательно к синтаксису)
- У app depends_on с условием, что база healthy
- Наружу проброшены только порты app и adminer

4.2 Подними всё через docker compose up -d. Зайди в Adminer через браузер, залогинься и создай какую-нибудь тестовую таблицу.

- сделано, все взлетело

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_4$ docker compose ps
NAME              IMAGE           COMMAND                  SERVICE   CREATED          STATUS                    PORTS
adminer_block_4   adminer:6.3.0   "entrypoint.sh docke…"   adminer   30 minutes ago   Up 30 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
app_block_4       myapp:v1        "uvicorn main:app --…"   app       30 minutes ago   Up 30 minutes             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
db_block_4        postgres:16     "docker-entrypoint.s…"   db        30 minutes ago   Up 30 minutes (healthy)   5432/tcp

- Заходим в БДшку

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_4$ docker exec -it db_block_4 /bin/bash
root@87c61c15991c:/# psql -U user -d postgres
psql (16.15 (Debian 16.15-1.pgdg13+2))
Type "help" for help.

postgres=# \dt
           List of relations
 Schema |     Name     | Type  | Owner 
--------+--------------+-------+-------
 public | Toyota_Supra | table | user
(1 row)

postgres=# 


4.3 Сделай docker compose down, потом снова up -d. Таблица на месте? Почему данные сохранились (или не сохранились, если вдруг сделал down -v).

- Данные сохранились, так как мы не ставили флаг -v, который удаляет volumes

- заведем эту тарахтелочку еще раз!

semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_4$ docker compose down
[+] down 4/4
 ✔ Container app_block_4     Removed                                                                          0.4s
 ✔ Container adminer_block_4 Removed                                                                          0.2s
 ✔ Container db_block_4      Removed                                                                          0.2s
 ✔ Network network_block_4   Removed                                                                          0.1s
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_4$ docker compose up -d
[+] up 4/4
 ✔ Network network_block_4   Created                                                                          0.0s
 ✔ Container db_block_4      Healthy                                                                          5.3s
 ✔ Container app_block_4     Started                                                                          5.4s
 ✔ Container adminer_block_4 Started                                                                          5.6s
semio@semio-HYM-WXX:~/Desktop/Docker_homework/block_4$ docker exec -it db_block_4 /bin/bash
root@6bdc0fe70174:/# psql -U user -d postgres
psql (16.15 (Debian 16.15-1.pgdg13+2))
Type "help" for help.

postgres=# \dt
           List of relations
 Schema |     Name     | Type  | Owner 
--------+--------------+-------+-------
 public | Toyota_Supra | table | user
(1 row)

postgres=# 

- вуаля, легенда Форсажа 1 все еще у нас в гараже, так как мы не удаляли volume
