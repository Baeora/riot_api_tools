from pangres import upsert
from sqlalchemy import create_engine

def df_to_sql(curr_df, db_engine, schema_name, table_name, pkeys):
    """Upserts DataFrame to SQL database at the designated schema.table

    Args:
        curr_df (dataframe): Dataframe that you're looking to upsert.
        db_engine (engine): SQLAlchemy engine, created via create_db_engine
        schema_name (str): Schema name.
        table_name (str): Table name.
        pkeys (str, list): Pkey column name, or list of Pkey column names.

    Returns:
        bool: True if succeeded, False if failed.
    """

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
    """Returns DB Connection String using input params

    Args:
        databse_url (str): Database Url (Ex: localhost).
        database_port (str): Database Port (Ex: 5432).
        username (str): Username (Ex: localhost).
        password (str): Password (Ex: admin).
        database (str): Database Name (Ex: Public).

    Returns:
        str: Formatted DB Connection String
    """

    return "postgresql+psycopg2://" + username + ":" + password + "@" + databse_url + ":" + database_port + "/" + database

def create_db_engine(database_url, database_port, db_username, db_password, database):
    """Creates DB Engine using the input params.

    Args:
        databse_url (str): Database Url (Ex: localhost).
        database_port (str): Database Port (Ex: 5432).
        username (str): Username (Ex: localhost).
        password (str): Password (Ex: admin).
        database (str): Database Name (Ex: Public).

    Returns:
        engine: SQLAlchemy engine
    """

    db_url = create_db_connection_string(
        database_url, database_port, db_username, db_password, database)
    alchemy_engine = create_engine(db_url, pool_recycle=3600, future=True)

    return alchemy_engine

