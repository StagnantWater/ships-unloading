from pymysql import connect
from pymysql.err import OperationalError

error_list = {2003: "Неверный хост или порт",
              1049: "Базы данных с заданным именем не существует",
              1064: "Синтаксическая ошибка в SQL-запросе",
              1146: "Ошибка в имени таблицы в SQL-запросе",
              1054: "Ошибка в имени колонки таблицы в SQL-запросе",
              1045: "Неверный логин или пароль"}


class UseDatabase:

    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except OperationalError:
            print(error_list[error.args[0]])
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None and self.cursor is not None:
            self.connection.commit()
            self.connection.close()
            self.cursor.close()
        elif exc_val.args[0] == "Cursor is None":
            print(exc_value.args[0])
        else:
            print(error_list[exc_value.args[0]])
        return True


def work_with_db(config, sql):
    result = []
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Cursor is None')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    return result
