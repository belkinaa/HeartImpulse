from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



from heart_imp_app.moduls.api_obj import UserPulse
from heart_imp_app.project_setting import Settings_app
from heart_imp_app.moduls.set_config_ap import __set_config_ap
from heart_imp_app.moduls.api_dbClasses import allTable_api

db = SQLAlchemy()
HI_App = Flask(__name__)

HI_App = __set_config_ap(HI_App, Settings_app())

db.init_app(HI_App)


from heart_imp_app.models import Users, UsersPulse

with HI_App.app_context():
    db.create_all()





@HI_App.route("/", methods=['GET'])
def hello_world():


    return render_template("addInformation.html",
                           informationUser=UserPulse(allTable_api(db, Users, 'dbUsers'),
                                                     allTable_api(db, UsersPulse, 'dbUsersPulse'),
                                                     request).information(),
                           round=round)



