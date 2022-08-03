from django.db import connection

def insert_into(tblName,colList,valueList):
   
   colName=""
   for i in colList:
      colName=colName+i+","
   colName=colName[:-1]
   
   with connection.cursor() as cursor:
     sql="insert into "+tblName+"("+colName+") values"
     for i in valueList:
        sql=sql+str(i)+","
     sql=sql[:-1]
     cursor.execute(sql)
   return