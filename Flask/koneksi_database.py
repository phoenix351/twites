import mysql.connector

def connectDB():
    #Koneksi ke database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="mydatabase"
    )
    mycursor = mydb.cursor(buffered=True)
    return mydb, mycursor

def set_var(var, value1, value2):
    mydb, mycursor = connectDB()
    # Update query untuk menginput variabel ke database
    sql_set_query = "UPDATE `temp_output` SET `" + var + "` = %s WHERE `id` = %s"
    value = (value1, value2)
    mycursor.execute(sql_set_query, value)
    mydb.commit()
