from pangres import upsert
from sqlalchemy import create_engine

def df_to_sql(curr_df, db_engine, schema_name, table_name, pkeys):
    with db_engine.connect() as connection:
        if curr_df.empty:
            print("DataFrame is empty")
            return True

        if pkeys:
            curr_df = curr_df.set_index(pkeys)
        else:
            raise Exception("Primary keys must be set")

        try:
            upsert(con=connection, df=curr_df, schema=schema_name, table_name=table_name, 
                   add_new_columns=True, if_row_exists='update', create_schema=True)
            connection.commit()  # Committing the transaction
            print("Upsert operation completed successfully.")
        except Exception as e:
            print(f"An error occurred during the upsert operation: {e}")
            connection.rollback()  # Rolling back in case of error
            return False

        return True

def create_db_connection_string(databse_url, database_port, username, password, database):
    return "postgresql+psycopg2://" + username + ":" + password + "@" + databse_url + ":" + database_port + "/" + database

def create_db_engine(database_url, database_port, db_username, db_password, database):
    db_url = create_db_connection_string(
        database_url, database_port, db_username, db_password, database)
    alchemy_engine = create_engine(db_url, pool_recycle=3600, future=True)

    return alchemy_engine

