from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Table, MetaData, select, insert
from sqlalchemy.exc import NoSuchTableError
from database.db import DATABASE_URL as SQLALCHEMY_DATABASE_URL, engine, SessionLocal
from typing import Dict, Any ,Optional

# Setup engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class SuperHelper:
    """
    Generic helper to fetch/insert records dynamically using table name.
    """

    @staticmethod
    def get_records(table_name: str, where: dict = None, select_columns="*"):

        db: Session = SessionLocal()
        metadata = MetaData()

        try:
            table = Table(table_name, metadata, autoload_with=engine)

            # SELECT columns
            if select_columns == "*":
                columns = [table.c[col.name] for col in table.columns]
            else:
                columns = [table.c[col] for col in select_columns]

            query = select(*columns)

            # WHERE condition
            if where:
                for key, value in where.items():

                    if key not in table.c:
                        raise Exception(f"Column '{key}' not found in table '{table_name}'")

                    query = query.where(table.c[key] == value)

            results = db.execute(query).fetchall()

            return [dict(row._mapping) for row in results]

        finally:
            db.close()
            

    @staticmethod
    def add(table_name: str, data: Dict[str, Any]):
        db: Session = SessionLocal()
        try:
            table = Table(table_name, MetaData(), autoload_with=engine)

            result = db.execute(insert(table).values(**data))
            db.commit()

            return result.inserted_primary_key[0] if result.inserted_primary_key else True

        except Exception as e:
            db.rollback()
            print(f"[SuperHelper] Insert Error: {e}")
            return None

        finally:
            db.close()
            
    @staticmethod
    def get_single_record(table_name: str, filters: Dict[str, Any], select_fields=None) -> Optional[Dict[str, Any]]:
        print("Method working")
        db: Session = SessionLocal()
        metadata = MetaData()

        try:
            table = Table(table_name, metadata, autoload_with=engine)

            stmt = select(table)
            for col, val in filters.items():
                stmt = stmt.where(getattr(table.c, col) == val)

            result = db.execute(stmt).first()
            if not result:
                return None

            row = dict(result._mapping)

            # Agar "*" diya hai ya kuch bhi nahi diya → sab fields
            if not select_fields or select_fields == "*":
                return row

            # Agar single column string hai
            if isinstance(select_fields, str):
                return {select_fields: row.get(select_fields)}

            # Agar list hai
            if isinstance(select_fields, list):
                return {k: row[k] for k in select_fields if k in row}

            return row

        except Exception as e:
            print(f"[SuperHelper] Error fetching record: {e}")
            return None
        finally:
            db.close()
            
    @staticmethod
    def delete_record(table_name: str, filters: Dict[str, Any]) -> bool:
        print("Delete method working")
        db: Session = SessionLocal()
        metadata = MetaData()

        try:
            table = Table(table_name, metadata, autoload_with=engine)

            stmt = table.delete()

            for col, val in filters.items():
                stmt = stmt.where(getattr(table.c, col) == val)

            result = db.execute(stmt)
            db.commit()

            return result.rowcount > 0  # True if something deleted

        except Exception as e:
            print(f"[SuperHelper] Error deleting record: {e}")
            db.rollback()
            return False

        finally:
            db.close()