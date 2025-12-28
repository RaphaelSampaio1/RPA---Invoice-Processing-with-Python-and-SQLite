import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
     
    def connect(self):
        """Establish a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path) 
        self.connection.row_factory = sqlite3.Row

        if not self.connection:
            raise ConnectionError("Failed to connect to the database.")

    def disconnect(self):
        """Close the connection to the SQLite database."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query (self, query, params=None):
        """Execute a SQL query and return the results."""
        if not self.connection:
            raise ConnectionError("No active database connection.")
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
            self.connection.commit()
        else:
            cursor.execute(query)
            self.connection.commit()
        print("Executed query:", query)
        return cursor

    def create_tables(self):
        """Create necessary tables in the database."""
        create_faturas_table = """
        CREATE TABLE IF NOT EXISTS faturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_fatura TEXT NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
            nif_emissor TEXT NOT NULL,
            nome_emissor TEXT NOT NULL,
            data_emissao TEXT DEFAULT CURRENT_TIMESTAMP,
            data_vencimento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            status TEXT NOT NULL,
            arquivo_path TEXT NOT NULL,
            data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(nif_emissor, numero_fatura)
        );
        """
        self.execute_query(create_faturas_table)
        self.connection.commit()

    def insert_fatura(self, nif_emissor, nome_emissor, data_emissao, data_vencimento, valor_total, status, arquivo_path):
        """Insert a new fatura record into the database."""
        insert_query = """ 
        INSERT INTO faturas 
            (
            nif_emissor, nome_emissor, data_emissao, data_vencimento, valor_total, status, arquivo_path
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (nif_emissor, nome_emissor, data_emissao, data_vencimento, valor_total, status, arquivo_path)
        try:
            self.execute_query(insert_query, params)
            print(f"✅ Fatura inserida: {arquivo_path} / {nif_emissor}")
            return True
        except sqlite3.IntegrityError as e:
            print(f"⚠️ Fatura duplicada: {arquivo_path} / {nif_emissor} -> {e}")
            return False



if __name__ == "__main__":
    db_manager = DatabaseManager("faturas.db")
    ## At the first run, create the tables
    db_manager.connect()
    db_manager.disconnect()
