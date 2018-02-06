from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import String, DateTime

class DataBaseInitializer(object):
    """ This initializes the database and give basic facilities sql queries
     for the table"""
    
    def __init__(self):
        try:
            self.engine = create_engine('sqlite:///test.db')
        except Exception as e:
            print("Unable to load the database! " + str(e))

    def read(self, username=None, password=None):
        if username:
            result = self.engine.execute(
                'select Username, Password from PasswordManager where\
                username=:uname', uname=username)
            for row in result:
                print(row)
        elif password:
            result = self.engine.execute(
                'select Username, Password from PasswordManager where\
                passc=:password', passc=password)
            for row in result:
                print(row)
        else:
            result = self.engine.execute('select * from PasswordManager')
            for row in result:
                print(row)

    def write(self, uname, passcode):
        if uname == "" or passcode == "":
            print("Fill Username and Password fields")
            return None
        else:
            self.engine.execute(
                'insert into PasswordManager (Username, Password) values\
                (:name,:passc)', name=uname, passc=passcode)

    def remove(self, uname):
        if uname == "":
            print("Error! supply username to remove..")
            return None
        else:
            self.engine.execute(
                'delete from PasswordManager where Username=:name', name=uname)


class TableOperator(DataBaseInitializer):
        # TODO: More Table operations

    def __init__(self):
        self.interface = DataBaseInitializer()
        self.metadata = MetaData()

    def PasswordTableGenerator(self):
        self.RecordTable = Table(
            'PasswordManager', self.metadata,
            Column('Username', String),
            Column('Password', String, primary_key=True),
            Column('SiteInfo', String),
            Column('timestamp', DateTime),
        )
        self.metadata.create_all(self.interface.engine)

    def writer(self, username, password):
        self.interface.write(username, password)

    def reader(self, username=None, password=None):
        self.interface.read(username, password)

    def remove(self, username=None):
        self.interface.remove(username)

    def dropper(self):
        self.RecordTable.drop(self.interface.engine)


def main():
    operator = TableOperator()
    operator.PasswordTableGenerator()
    operator.reader()
    #operator.writer('Chirag', 'qwertyuiop')
    operator.reader('Chirag')
    operator.reader('qwertyuiop')
    #operator.remove('rasadajseq')
    #operator.dropper()


if __name__ == '__main__':
    main()