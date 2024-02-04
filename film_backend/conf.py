## database configs
#DBADDR = '0.0.0.0'  # Docker 容器映射到宿主机的地址
DBADDR = 'postgres-service'
DATABASE = 'moviesmanagement'   # 默认数据库名称
DBUSER = 'postgres'   # 默认用户名
DBPW = 'mysecretpassword'      # 设置的密码
DBPORT = 5432          # 映射到宿主机的端口

#HOST IP
HOST = '0.0.0.0'

#PORT
PORT = 5000

#secret key
SECRET_KEY = 'group35'