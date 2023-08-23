from datetime import datetime

from heart_imp_app.moduls.api_dbClasses import allTable_api


class UserPulse():
    def __init__(self,
                 objUsers: allTable_api,
                 objUserPulse: allTable_api,
                 request):
        self.objUser = objUsers
        self.objUserPulse = objUserPulse
        self.request = request
        self.user_id = None
        self.midle_pulse = 0

    def add_information(self):
        if (email := self.request.args.get('email', None)) and (pulse := self.request.args.get('pulse', None)):

            if (is_user := self.objUser.new__getRows_for_value_field(self.objUser.dbTable, email=email)) is None:
                self.user_id = self.objUser.get_newId(self.objUser.dbTable)
                self.objUser.insert_rows_DB(self.objUser.dbTable(
                    id=self.user_id,
                    email=email
                ))
            else:
                self.user_id = is_user.id

            self.objUserPulse.insert_rows_DB(self.objUserPulse.dbTable(
                user_id=self.user_id,
                pulse=pulse,
                date=datetime.now()
            ))
    def response_information(self, all_rows) -> dict:
        return {
            'all_rows': all_rows,
            'midle_pulse': self.midle_pulse,
            'curent_pulse': pulse if (pulse:= self.request.args.get('pulse', None)) is None else int(pulse),
            'user': self.request.args.get('email', None)
        }

    def information(self) -> dict:
        self.add_information()
        print('self.user_id', self.user_id)
        if ((all_rows := self.objUserPulse.new__getRows_for_value_field(
            self.objUserPulse.dbTable, is_all=True, user_id=self.user_id)) is None) or (self.user_id is None):
            return self.response_information(None)
        else:
            print('all_rows:', all_rows)
            self.midle_pulse = sum([i.pulse for i in all_rows]) / len(all_rows)
            return self.response_information(all_rows)
