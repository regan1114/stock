from data_manager import db_service
import pandas

def setting_parameter(name):
    dbService = db_service.DbService()
    sqlStr = ' SELECT * FROM setting'
    sqlStr += " WHERE name = '%s'" % name
    dataTable = dbService.query_all(sqlStr)
    return dataTable

def get_parameter(name):
    results = setting_parameter(name)
    dataTable = pandas.DataFrame(results)
    dataTable.columns = ['id', 'name', 'value', 'note']    
    return dataTable

def update_parameter(value, name):
    dbService = db_service.DbService()
    actionSql = "UPDATE setting SET value = '%s' WHERE name = '%s'" %(value, name)
    dbService.execute(actionSql)
    
def get_schedule_status():
    dbService = db_service.DbService()
    sqlStr = ' SELECT * FROM setting'
    sqlStr += " WHERE name = 'DailySchedule'"
    array = dbService.query_one(sqlStr)
    return array[2]