from sqlalchemy import create_engine, text, Column, Integer, String, Sequence, DateTime, BigInteger, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


def get_sql_files():
    """
    获取当前目录的.sql文件名列表
    :return:
    """
    sql_files = filter(lambda x: x.endswith('.sql'), os.listdir(os.getcwd()))
    print(sql_files)


Base = declarative_base()


class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(64))
    gender = Column(String(64))
    age = Column(Integer)

    def __repr__(self):
        return "Product(id=%d, name=%s, gender=%s, age=%d)"(self.id, self.name, self.gender, self.age)


def sqlacodegen(dbname, outfile_name):
    """
    根据数据库逆向生成model.py
    :param dbname:
    :param outfile_name:
    :return:
    """
    cmd = 'sqlacodegen --noviews --noconstraints --noindexes --outfile ./%s.py mysql+pymysql://root:ut123456@localhost:3306/%s' % (
    outfile_name, dbname)
    ret = os.system(cmd)
    print(ret)


def __insert_demo(mysession):
    newuser = User()
    newuser.id = 3
    newuser.name = '小刚'
    newuser.gender = 'female'
    newuser.age = 12
    mysession.add(newuser)
    mysession.commit()
    mysession.close()


def __query_demo(mysession):
    res = mysession.query(User).filter(text("id=3")).one()
    print(res.id, res.name, res.gender, res.age)
    mysession.close()


def __update_demo(mysession):
    res = mysession.query(User).filter(text("id=3")).one()
    res.name = "大刚"
    mysession.commit()
    mysession.close()


def __delete_demo(mysession):
    res = mysession.query(User).filter(text("id=3")).one()
    mysession.delete(res)
    mysession.commit()
    mysession.close()


def get_mysql_session(user, password, db_name):
    """
    获取数据库连接
    :param user:
    :param password:
    :param db_name:
    :return:
    """
    DB_CON_STR = 'mysql+pymysql://%s:%s@localhost/%s?charset=utf8mb4' % (user, password, db_name)
    print(DB_CON_STR)
    engine = create_engine(DB_CON_STR, echo=False)
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def execute_sqls(mysession, sqls):
    """
    执行完整的sql语句
    :param mysession:
    :param sqls:
    :return:
    """
    if isinstance(sqls, str):  # 单句sql直接执行
        mysession.execute(sqls)
    elif isinstance(sqls, list):  # 多句sql遍历执行
        for sql in sqls:
            mysession.execute(sql)
    elif isinstance(sqls, tuple):  # 多句sql遍历执行
        for sql in sqls:
            mysession.execute(sql)


if __name__ == '__main__':
    mysession = get_mysql_session('root', 'ut123456', 'testdatabase')
    __query_demo(mysession)
    # sqlacodegen('shortmsg','nodelnew')
