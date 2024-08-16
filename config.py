SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="",
    hostname="localhost",
    databasename="nwas",
)
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
threaded = True