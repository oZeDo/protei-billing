###Перед запуском тестов
1. Установить зависимости `pip install -r requirements.txt`
2. Для работы с бд необходимо установить oracle instant client на машину, с которой будут запускаться тесты, инструкция 
по установке [здесь](https://wiki.protei.ru/doku.php?id=protei:qa:billing.ocs:oracle_instantclient_installation)
3. Отрефлектить БД `sqlacodegen oracle+cx_oracle://pbill:sql@<ip базы>:1521/orcl --outfile reflected_db.py`
4. Отредактировать файл /config/testrail.cfg, добавить туда свои логин и ключ для тестреила

###Запуск тестов
1. Для запуска тестов при помощи pytest используйте `pytest ./tests/functional/test_group_adding.py`
2. Для запуска теста с выгрузкой результатов в testrail используйте флаг --testrail, а также укажите пусть до файла
конфигурации, если он не находится в корневом каталоге `pytest --testrail --tr-config=./config/testrail.cfg
./tests/functional/test_group_adding.py`
3. Для создания allure-отчетов используйте флаг `--alluredir=reports`