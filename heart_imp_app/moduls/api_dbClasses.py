from heart_imp_app.moduls.set_config_ap import generate_alphanum_crypt_string


class OperationDB():
    def __init__(self, DB):
        self.db = DB
    def new__getRows_for_value_field(self, dbTable, is_all=False, **kwargs):
        if is_all:
            return dbTable.query.filter_by(**kwargs).order_by(dbTable.id.desc()).all()
        return dbTable.query.filter_by(**kwargs).order_by(dbTable.id.desc()).first()
    def create_new_ID(self, dbTable):
        cash = self.db.session.query(dbTable.id).order_by(dbTable.id.desc()).first()
        if cash is None:
            new_ID = 1
        else:
            new_ID = cash.id + 1
        self.db.session.close()
        return new_ID

    # Получение строки из таблицы по ID
    def getRows(self, dbClass, ID):
        return dbClass.query.filter_by(id=int(ID)).first()

    def get_all(self, dbClass):
        return dbClass.query.all()

    # Получение нового ID
    def get_newId(self, dbName):
        cashRows = dbName.query.order_by(dbName.id.desc()).first()
        if cashRows is None:
            return 1
        else:
            return cashRows.id + 1

    # Новая запись в БД (INSERT)
    def insert_rows_DB(self, newRowsCash):
        self.db.session.add(newRowsCash)
        self.db.session.commit()
        self.db.session.close()

    # Обновление полей в таблице
    def update_op_table(self, dbTab, idRows, field_lst, data_list):
        print('\n||| update_op_table |||')
        print('idRows |==>', idRows)
        print('field_lst |==>', field_lst)
        print('data_list |==>', data_list)
        if len(field_lst) > 0:
            cash = self.db.session.query(dbTab).filter_by(
                id=int(idRows)).first()
            if cash is None:
                print('Нет такой строки!')
            for name, value in zip(field_lst, data_list):
                print('name=>', name, '|->|', 'value=>', value, )
                setattr(cash, name, value)
            self.db.session.commit()
            self.db.session.close()
            print('\t\t === Поля ОБНОВИЛИ! === ')
        else:
            print('--- Нет полей для обновления... ---')
        print('\n ---- ||| END update_op_table ||| ----')


# --------------------------------------------------------------------------------------------------
class allTable_api(OperationDB):
    def __init__(self, db, dbTable, nameTab='??'):
        super().__init__(DB=db)
        self.dbTable = dbTable
        self.__nameTab = nameTab

    def getRows_for_ID(self, intID):
        return self.dbTable.query.filter_by(id=intID).first()

    # Получает новый ID для записи нового шаблона
    def _get_newId_(self):
        cashRows = self.dbTable.query.order_by(self.dbTable.id.desc()).first()
        if cashRows is None:
            return 1
        else:
            return cashRows.id + 1

    def del_all_rows_for_user_id(self, idUser, id_owner=False, presentation_id=False):
        idUser = int(idUser)
        print(f'delete {self.__nameTab} ...')
        print('idUser, id_owner, presentation_id:',idUser, id_owner, presentation_id)
        self._id_cash_delete = []
        if presentation_id:
            all_rows = self.dbTable.query.filter_by(presentation_id=presentation_id).all()
        else:
            if id_owner:
                all_rows = self.dbTable.query.filter_by(id_owner=idUser).all()
            else:
                all_rows = self.dbTable.query.filter_by(user_id=idUser).all()
        print('all_rows:', all_rows)
        for rows in all_rows:
            self._id_cash_delete.append(rows.id)
            self.db.session.delete(rows)
            self.db.session.commit()
        print(f'delete {self.__nameTab} - OK')

    def delete_rows(self, rows):
        print(f'delete rows: {rows} in  {self.__nameTab} ....')
        self.db.session.delete(rows)
        self.db.session.commit()
        print(f'delete rows {self.__nameTab} - OK')

    def get_all_rows(self, idUser, id_owner=False):
        idUser = int(idUser)
        print(f'delete {self.__nameTab} ...')
        if id_owner:
            all_rows = self.dbTable.query.filter_by(id_owner=idUser).all()
        else:
            all_rows = self.dbTable.query.filter_by(user_id=idUser).all()
        return all_rows

    def get_all_rows_table(self):
        return self.dbTable.query.all()


from urllib.parse import unquote
class CodeDecodeSecret():
    ALPHABET = "@_-0123456789,.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def code_secret(self, key: int, user_email: str, secret_value=None) -> str:
        """Возвращает закодированное секретное сообщение"""
        if key >= len(self.ALPHABET):
            key = key % len(self.ALPHABET)
        size = len(self.ALPHABET)
        if secret_value is None:
            secret_value = user_email
        return generate_alphanum_crypt_string(len(user_email)) + ''.join(self.ALPHABET[rez] if (rez := self.ALPHABET.index(i) + key) <= size else self.ALPHABET[(rez - size)] for i in secret_value)

    def decode_secret(self, key: int, user_email: str, secret_value_for_decode: str) -> str:
        """Декодирует секретное сообщение, для проверки валидности токена"""
        if key >= len(self.ALPHABET):
            key = key % len(self.ALPHABET)
        secret_value_for_decode = secret_value_for_decode[len(user_email):]
        # return ''.join(self.ALPHABET[rez] if (rez := self.ALPHABET.index(i) - key) < 40 else self.ALPHABET[(rez + 41)] for i in secret_value_for_decode)
        return self.sol_decode(key=key, secret_value_for_decode=secret_value_for_decode)

    def sol_decode(self, key: int, secret_value_for_decode, sol=0):
        if key >= len(self.ALPHABET):
            key = key % len(self.ALPHABET)
        secret_value_for_decode = secret_value_for_decode[sol:]
        return ''.join(
            self.ALPHABET[rez] if (rez := self.ALPHABET.index(i) - key) < 40 else self.ALPHABET[(rez + 41)] for i in
            secret_value_for_decode)
    def sol_code_secret(self, key: int, secret_value: str, sol=0) -> str:
        """Возвращает закодированное секретное сообщение"""
        if key >= len(self.ALPHABET):
            key = key % len(self.ALPHABET)
        size = len(self.ALPHABET)
        return generate_alphanum_crypt_string(sol) + ''.join(self.ALPHABET[rez] if (rez := self.ALPHABET.index(i) + key) <= size else self.ALPHABET[(rez - size)] for i in secret_value)

    def decode_url_string(self, string_value):
        return ' '.join([unquote(i, 'utf-8') for i in string_value.split('+')])




