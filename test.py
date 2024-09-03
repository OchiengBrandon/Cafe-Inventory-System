import mysql.connector

conn  = mysql.connector.connect(
    host="sql.freedb.tech,",
    port = 3306,
    user="freedb_brandon",
    password = "bWfV$C2BGmeyp66",
    database="freedb_CafeInventorySystem"
)


print(conn)