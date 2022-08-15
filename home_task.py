import re

import pytest
from sqlalchemy import create_engine

# For Trusted Connection string
#db_config_params='DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\\SQLEXPRESS;DATABASE=TRN;Trusted_Connection=yes;'

# For Server Connection string
database = 'TRN'
login = 'TestUserLogin2'
password = '12345'
db_config_param = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=192.168.1.2,1433;DATABASE=%(database)s;UID=%(login)s;PWD=%(password)s;TrustServerCertificate=yes;' % {'database': database, 'login': login, 'password': password}


class CreateDataBatch:
    def __init__(self, db_config_params, query):
        self.db_config = db_config_params
        self.query = query

    def create_engine_db(self):
        return create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.db_config)

    def query_result(self):
        engine = self.create_engine_db()
        result = engine.execute(self.query)
        engine.dispose()
        return result


class TestEmployer:
    def test_table_duplicates(self):
        query = """
              SELECT 
                   [employee_id]
                  ,[first_name]
                  ,[last_name]
                  ,[email]
                  ,[phone_number]
                  ,[hire_date]
                  ,[job_id]
                  ,[salary]
                  ,[manager_id]
                  ,[department_id]
                  , count(*)
              FROM [TRN].[hr].[employees]
              group by [employee_id]
                  ,[first_name]
                  ,[last_name]
                  ,[email]
                  ,[phone_number]
                  ,[hire_date]
                  ,[job_id]
                  ,[salary]
                  ,[manager_id]
                  ,[department_id]
             having count(*)>1
        """
        batch_result = CreateDataBatch(db_config_params=db_config_param, query=query).query_result()
        id_name_amount = []
        for r in batch_result:
            id_name_amount.append(r)

        assert len(id_name_amount) == 0, f'Ids are not unique: {id_name_amount}'


class TestRegion:
    def test_table_duplicates(self):
        query = """
              SELECT 
                   [region_id]
                  ,[region_name]
                  , count(*)
              FROM [TRN].[hr].[regions]
              group by [region_id]
                  ,[region_name]
             having count(*)>1
        """
        batch_result = CreateDataBatch(db_config_params=db_config_param, query=query).query_result()
        id_name_amount = []
        for r in batch_result:
            id_name_amount.append(r)

        assert len(id_name_amount) == 0, f'Fields are duplicated: {id_name_amount}'

    def test_validity_of_region_name(self):
        query = """
              SELECT 
                   [region_id]
                  ,[region_name]
              FROM [TRN].[hr].[regions]
        """
        batch_result = CreateDataBatch(db_config_params=db_config_param, query=query).query_result()
        id_name_amount = []
        for r in batch_result:
            if r.region_name not in ['Europe', 'Americas', 'Asia', 'Middle East and Africa']:
                id_name_amount.append(r)

        assert len(id_name_amount) == 0, f"region_name not in 'Europe', 'Americas', 'Asia', 'Middle East and Africa': {id_name_amount}"

