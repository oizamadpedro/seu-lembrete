from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
#from app.settings import MYSQL_DB_HOST, MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_NAME, MYSQL_DB_PORT, DATABASE

class Database:
    def __init__(self):
        self.engine = create_engine(
            f"sqlite:///database.db",
            echo=False,  # Defina como True para depuração de SQL
        )
        self.Session = sessionmaker(bind=self.engine)

    def execute(self, query, params=None, commit=False):
        session = self.Session()
        try:
            stmt = text(query)
            print(params)
            result = session.execute(stmt, params or {})

            if commit:
                session.commit()
                return result.lastrowid

            #print(result.mappings().all())
            response = result.mappings().all()
            
            for i in range(len(response)):
                if not isinstance(response[i], dict):
                    response[i] = dict(response[i])  # Converte o objeto `Row` para um dicionário

            return response
        except Exception as e:
            print(f"Error on database execute: {e}")
            session.rollback()
            return []
        finally:
            session.close()

    def executemany(self, query, params_list):
        session = self.Session()
        try:
            stmt = text(query)
            session.execute(stmt, params_list)
            session.commit()
            return True
        except Exception as e:
            print(f"Error on database executemany: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def close(self): pass