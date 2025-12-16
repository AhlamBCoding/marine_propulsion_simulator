import sqlite3
import pandas as pd

class VesselDatabase:
    def __init__(self, db_path='data/vessel_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.populate_sample_data()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Propulsion systems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS propulsion_systems (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                efficiency REAL,
                fuel_type TEXT,
                co2_factor REAL,
                initial_cost REAL
            )
        ''')
        
        # Operating profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operating_profiles (
                id INTEGER PRIMARY KEY,
                profile_name TEXT NOT NULL,
                cruising_hours REAL,
                maneuvering_hours REAL,
                port_hours REAL,
                cruising_power_pct REAL,
                maneuvering_power_pct REAL,
                port_power_pct REAL
            )
        ''')
        
        # Simulation results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                propulsion_system_id INTEGER,
                profile_id INTEGER,
                total_fuel_consumption REAL,
                total_co2_emissions REAL,
                total_cost REAL,
                FOREIGN KEY (propulsion_system_id) REFERENCES propulsion_systems(id),
                FOREIGN KEY (profile_id) REFERENCES operating_profiles(id)
            )
        ''')
        
        self.conn.commit()
    
    def populate_sample_data(self):
        cursor = self.conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM propulsion_systems')
        if cursor.fetchone()[0] > 0:
            return
        
        # Propulsion systems data
        propulsion_data = [
            (1, 'Conventional Diesel', 'diesel', 0.40, 'HFO', 3.114, 1000000),
            (2, 'Diesel-Electric Hybrid', 'hybrid', 0.45, 'MDO', 3.206, 1500000),
            (3, 'Battery Electric', 'electric', 0.90, 'electricity', 0.5, 2500000)
        ]
        
        cursor.executemany('''
            INSERT INTO propulsion_systems 
            (id, name, type, efficiency, fuel_type, co2_factor, initial_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', propulsion_data)
        
        # Operating profiles (typical ferry route)
        profile_data = [
            (1, 'Short Route Ferry', 4, 1, 2, 0.75, 0.40, 0.10),
            (2, 'Long Route Ferry', 8, 1.5, 1, 0.80, 0.45, 0.15),
            (3, 'Cargo Vessel', 20, 2, 3, 0.70, 0.35, 0.05)
        ]
        
        cursor.executemany('''
            INSERT INTO operating_profiles 
            (id, profile_name, cruising_hours, maneuvering_hours, port_hours,
             cruising_power_pct, maneuvering_power_pct, port_power_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', profile_data)
        
        self.conn.commit()
    
    def get_propulsion_systems(self):
        return pd.read_sql_query('SELECT * FROM propulsion_systems', self.conn)
    
    def get_operating_profiles(self):
        return pd.read_sql_query('SELECT * FROM operating_profiles', self.conn)
    
    def save_simulation_result(self, result_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_results 
            (timestamp, propulsion_system_id, profile_id, 
             total_fuel_consumption, total_co2_emissions, total_cost)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', result_data)
        self.conn.commit()
    
    def get_all_results(self):
        return pd.read_sql_query('''
            SELECT sr.*, ps.name as propulsion_name, op.profile_name
            FROM simulation_results sr
            JOIN propulsion_systems ps ON sr.propulsion_system_id = ps.id
            JOIN operating_profiles op ON sr.profile_id = op.id
        ''', self.conn)
    
    def close(self):
        self.conn.close()