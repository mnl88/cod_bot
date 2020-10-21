from sqlalchemy import create_engine, Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from datetime import datetime, date, time
import config


DATABASE = {
    'drivername': 'postgres',
    'host': config.DATABASE_HOST,
    'port': config.DATABASE_PORT,
    'username': config.DATABASE_USER,
    'password': config.DATABASE_PASSWORD,
    'database': config.DATABASE_NAME
}

DeclarativeBase = declarative_base()


class COD_User(DeclarativeBase):
    __tablename__ = 'cod_users'

    id = Column(Integer, primary_key=True)
    tg_id = Column('tg_id', Integer, unique=True, nullable=False)
    tg_name = Column('tg_name', String, default='unknown')
    name = Column('name', String, default='unknown')
    psn_id = Column('psn_id', String, default='unknown')
    activision_id = Column('activision_id', String, default='unknown')
    kd_warzone = Column('kd_warzone', String(50), default='unknown')
    kd_multiplayer = Column('kd_multiplayer', String(50), default='unknown')
    update_kd = Column('update_kd', TIMESTAMP, default=datetime.now())
    update_timestamp = Column('update_timestamp', TIMESTAMP, default=datetime.now())
    ready_to_play_timestamp = Column('ready_to_play_timestamp', TIMESTAMP)
    ready_to_play_comment = Column('ready_to_play_comment', String(250), default='')

    def __repr__(self):
        return "<COD-USER: ('%s','%s','%s','%s')>" % (self.tg_id, self.tg_name, self.activision_id, self.name)


engine = create_engine(URL(**DATABASE))
DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def is_row_exists(tg_id):
    """Проверяем, существует ли указанная запись в БД с данным ID"""

    with engine.connect() as conn:
        if session.query(COD_User).filter_by(tg_id=tg_id).first():
            return True
    return False


def get_member(tg_id):
    """По указанному ID получаем объект"""

    with engine.connect() as conn:
        if is_row_exists(tg_id):
            member = session.query(COD_User).filter_by(tg_id=tg_id).first()
            return member
    return False


def get_all_members(**config_filter):
    """По указанному ID получаем объект"""

    with engine.connect() as conn:
        members = session.query(COD_User).filter_by(**config_filter).all()
        return members


def add_member(tg_id, tg_name='empty'):
    """Добавляем участника"""

    with engine.connect() as conn:
        cod_user = COD_User(tg_id=tg_id, tg_name=tg_name)
        if not is_row_exists(session, cod_user.tg_id):
            try:
                session.add(cod_user)
                session.commit()
            finally:
                return True
        else:
            print('пользователь с данным ID уже есть в БД')
            return False

def update_member(cod_user):
    """Обновляем данные об участнике"""

    with engine.connect() as conn:
        if is_row_exists(session, cod_user.tg_id):
            try:
                session.add(cod_user)
                session.commit()
                return True
            finally:
                pass
        else:
            print('пользователь с данным ID уже есть в БД')
            return False


def create_all_to_test():
    """Заполняет базу данных несколькими придуманными пользователями"""

    with engine.connect() as conn:
        # nikita_user = COD_User(tg_id=202181776, tg_name='MaNiLe88', name='Никита')
        # session.add(nikita_user)
        # print(nikita_user)
        session.add_all([COD_User(tg_id=156134156, tg_name='MaNiLe90', name='Катя'),
                         COD_User(tg_id=984813515, tg_name='MaNiLe95', name='Даша'),
                         COD_User(tg_id=325861657, tg_name='MaNiLe97', name='Петя'),
                         COD_User(tg_id=101244567, tg_name='MaNiLe99', name='Вася')
                         ])
        try:
            session.commit()
        except:
            print('session.commit() fall down')

        # print(nikita_user)
        # print(nikita_user.id)


def main():
    members = get_all_members()
    create_all_to_test()
    print(members)
    # # Создаем новую запись.
    # new_post1 = COD_User(tg_id='123', tg_name='Погоняло в телеграме', name="Вася")
    # # Добавляем запись
    # session.add(new_post1)
    # # Создаем новую запись.
    # new_post2 = COD_User(tg_id='456', tg_name='Погоняло в телеграме2', name="Петя")
    # # Добавляем запись
    # session.add(new_post2)
    # # Благодаря этой строчке мы добавляем данные а таблицу
    # session.commit()
    # # А теперь попробуем вывести все посты , которые есть в нашей таблице
    # for post in session.query(COD_User):
    #     print(post)


if __name__ == "__main__":
    main()

