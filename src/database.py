import sqlite3
import pandas as pd
import json

class VesselDatabase:
    def __init__(self, db_path='data/vessel_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.populate_sample_data()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Enhanced propulsion systems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS propulsion_systems (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                
                -- Main engine data
                main_engine_model TEXT,
                main_engine_power REAL,
                main_engine_count INTEGER,
                main_engine_sfoc REAL,
                
                -- Auxiliary/genset data
                aux_engine_model TEXT,
                aux_engine_power REAL,
                aux_engine_count INTEGER,
                aux_engine_sfoc REAL,
                
                -- Dual-fuel specific
                sfoc_gas REAL,
                sfoc_diesel REAL,
                lng_ratio REAL,
                pilot_fuel REAL,
                
                -- Battery data (for hybrid)
                battery_capacity REAL,
                battery_efficiency REAL,
                motor_efficiency REAL,
                
                -- Fuel properties
                primary_fuel TEXT,
                backup_fuel TEXT,
                co2_factor REAL,
                sox_factor REAL,
                
                -- Economic
                initial_cost REAL,
                fuel_price REAL,
                fuel_price_gas REAL,
                
                -- Compliance
                imo_tier TEXT,
                eca_compliant BOOLEAN
            )
        ''')
        
        # Operating profiles table (updated for short-sea tanker)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operating_profiles (
                id INTEGER PRIMARY KEY,
                profile_name TEXT NOT NULL,
                vessel_type TEXT,
                
                -- Design parameters
                design_speed_knots REAL,
                design_power_kw REAL,
                
                -- Operational hours (annual)
                sailing_hours REAL,
                maneuvering_hours REAL,
                port_hours REAL,
                
                -- Sailing operation
                sailing_speed_knots REAL,
                sailing_prop_power_kw REAL,
                sailing_elec_power_kw REAL,
                
                -- Maneuvering operation
                maneuvering_prop_power_kw REAL,
                maneuvering_elec_power_kw REAL,
                
                -- Port operation
                port_prop_power_kw REAL,
                port_elec_power_kw REAL
            )
        ''')
        
        # Simulation results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                config_id INTEGER,
                profile_id INTEGER,
                
                -- Annual totals
                total_fuel_kg REAL,
                total_co2_tonnes REAL,
                total_sox_tonnes REAL,
                fuel_cost_usd REAL,
                capital_cost_annual_usd REAL,
                total_annual_cost_usd REAL,
                
                -- Breakdown by mode
                sailing_fuel_kg REAL,
                maneuvering_fuel_kg REAL,
                port_fuel_kg REAL,
                
                FOREIGN KEY (config_id) REFERENCES propulsion_systems(id),
                FOREIGN KEY (profile_id) REFERENCES operating_profiles(id)
            )
        ''')
        
        self.conn.commit()
    
    def populate_sample_data(self):
        cursor = self.conn.cursor()
        
        # Check if data exists
        cursor.execute('SELECT COUNT(*) FROM propulsion_systems')
        if cursor.fetchone()[0] > 0:
            return
        
        # =================================================================
        # CONFIGURATION A: Conventional Diesel-Mechanical
        # =================================================================
        cursor.execute('''
            INSERT INTO propulsion_systems VALUES (
                1,                                  -- id
                'Conventional Diesel-Mechanical',   -- name
                'diesel',                           -- type
                'Main: Wärtsilä 8L32 (4640 kW), Aux: 2× Wärtsilä 9L20 (1800 kW)',
                
                'Wärtsilä 8L32',  -- main_engine_model
                4640.0,            -- main_engine_power
                1,                 -- main_engine_count
                181.0,             -- main_engine_sfoc @ 85% (REAL DATA)
                
                'Wärtsilä 9L20',   -- aux_engine_model
                1800.0,            -- aux_engine_power
                2,                 -- aux_engine_count
                195.1,             -- aux_engine_sfoc @ 85% (REAL DATA)
                
                NULL, NULL, NULL, NULL,  -- dual-fuel fields (not used)
                NULL, NULL, NULL,        -- battery fields (not used)
                
                'MDO',             -- primary_fuel
                NULL,              -- backup_fuel
                3.206,             -- co2_factor (kg CO2/kg fuel)
                0.001,             -- sox_factor (kg SOx/kg fuel, 0.1% sulfur)
                
                2800000.0,         -- initial_cost (USD)
                650.0,             -- fuel_price (USD/tonne MDO)
                NULL,              -- fuel_price_gas
                
                'IMO Tier III',    -- imo_tier
                1                  -- eca_compliant
            )
        ''')
        
        # =================================================================
        # CONFIGURATION B: Dual-Fuel LNG
        # =================================================================
        cursor.execute('''
            INSERT INTO propulsion_systems VALUES (
                2,
                'Dual-Fuel LNG',
                'dual-fuel',
                'Main: Wärtsilä 8V31DF (4800 kW), Aux: 2× Wärtsilä 8L20DF (1280 kW)',
                
                'Wärtsilä 8V31DF',
                4800.0,
                1,
                157.5,             -- main SFOC in gas mode @ 85% (REAL DATA)
                
                'Wärtsilä 8L20DF',
                1280.0,
                2,
                172.0,             -- aux SFOC in gas mode @ 85% (calculated)
                
                157.5,             -- sfoc_gas (main engine)
                176.9,             -- sfoc_diesel (LFO mode)
                0.95,              -- lng_ratio (95% on gas)
                5.2,               -- pilot_fuel (g/kWh)
                
                NULL, NULL, NULL,  -- battery fields
                
                'LNG',
                'MDO',
                2.75,              -- co2_factor for LNG
                0.0,               -- sox_factor (no sulfur in LNG)
                
                4200000.0,
                400.0,             -- LNG price
                650.0,             -- MDO backup price
                
                'IMO Tier III (Gas)',
                1
            )
        ''')
        
        # =================================================================
        # CONFIGURATION C: Diesel-Electric Hybrid
        # =================================================================
        cursor.execute('''
            INSERT INTO propulsion_systems VALUES (
                3,
                'Diesel-Electric Hybrid',
                'hybrid',
                'Gensets: 4× Wärtsilä 8L20 (1600 kW), Battery: 1500 kWh',
                
                NULL,              -- no main engine (electric propulsion)
                NULL,
                NULL,
                NULL,
                
                'Wärtsilä 8L20',
                1600.0,
                4,
                194.5,             -- genset SFOC @ 85% (REAL DATA)
                
                NULL, NULL, NULL, NULL,  -- dual-fuel fields
                
                1500.0,            -- battery_capacity (kWh)
                0.95,              -- battery_efficiency
                0.97,              -- motor_efficiency
                
                'MDO',
                NULL,
                3.206,
                0.001,
                
                4500000.0,         -- higher cost (gensets + motors + batteries)
                650.0,
                NULL,
                
                'IMO Tier III',
                1
            )
        ''')
        
        # =================================================================
        # OPERATIONAL PROFILE: Short-Sea Tanker (Lorenzo's Assignment)
        # =================================================================
        
        # Calculate sailing power using cubic interpolation
        design_speed = 14.0      # knots
        design_power = 4500.0    # kW
        sailing_speed = 12.5     # knots
        
        # P_sailing = P_design × (V_sailing / V_design)³
        sailing_prop_power = design_power * (sailing_speed / design_speed) ** 3
        # Result: 4500 × (12.5/14)³ ≈ 3578 kW
        
        cursor.execute('''
            INSERT INTO operating_profiles VALUES (
                1,                          -- id
                'Short-Sea Tanker',         -- profile_name
                'Product Tanker',           -- vessel_type
                
                14.0,                       -- design_speed_knots
                4500.0,                     -- design_power_kw
                
                5694.0,                     -- sailing_hours (65% × 8760)
                438.0,                      -- maneuvering_hours (5% × 8760)
                2628.0,                     -- port_hours (30% × 8760)
                
                12.5,                       -- sailing_speed_knots
                ?,                          -- sailing_prop_power_kw (calculated)
                700.0,                      -- sailing_elec_power_kw
                
                1000.0,                     -- maneuvering_prop_power_kw
                1200.0,                     -- maneuvering_elec_power_kw
                
                0.0,                        -- port_prop_power_kw
                500.0                       -- port_elec_power_kw
            )
        ''', (sailing_prop_power,))
        
        self.conn.commit()
        print("✓ Database populated with real Wärtsilä engine data")
        print(f"  - Sailing propulsion power (cubic interpolation): {sailing_prop_power:.1f} kW")
    
    def get_propulsion_systems(self):
        """Get all propulsion system configurations"""
        return pd.read_sql_query('SELECT * FROM propulsion_systems', self.conn)
    
    def get_operating_profiles(self):
        """Get all operating profiles"""
        return pd.read_sql_query('SELECT * FROM operating_profiles', self.conn)
    
    def get_configuration(self, config_id):
        """Get specific configuration details"""
        query = 'SELECT * FROM propulsion_systems WHERE id = ?'
        return pd.read_sql_query(query, self.conn, params=(config_id,)).iloc[0]
    
    def get_profile(self, profile_id):
        """Get specific operational profile"""
        query = 'SELECT * FROM operating_profiles WHERE id = ?'
        return pd.read_sql_query(query, self.conn, params=(profile_id,)).iloc[0]
    
    def save_simulation_result(self, result_data):
        """Save simulation results to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO simulation_results (
                timestamp, config_id, profile_id,
                total_fuel_kg, total_co2_tonnes, total_sox_tonnes,
                fuel_cost_usd, capital_cost_annual_usd, total_annual_cost_usd,
                sailing_fuel_kg, maneuvering_fuel_kg, port_fuel_kg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', result_data)
        self.conn.commit()
    
    def get_all_results(self):
        """Get all simulation results with configuration names"""
        return pd.read_sql_query('''
            SELECT 
                sr.*,
                ps.name as config_name,
                op.profile_name
            FROM simulation_results sr
            JOIN propulsion_systems ps ON sr.config_id = ps.id
            JOIN operating_profiles op ON sr.profile_id = op.id
            ORDER BY sr.timestamp DESC
        ''', self.conn)
    
    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Test database creation
    import os
    os.makedirs('data', exist_ok=True)
    
    db = VesselDatabase()
    
    print("\n=== Propulsion Systems ===")
    configs = db.get_propulsion_systems()
    for _, config in configs.iterrows():
        print(f"\n{config['name']}:")
        print(f"  Main: {config['main_engine_model']} ({config['main_engine_power']} kW)")
        print(f"  Aux: {config['aux_engine_count']}× {config['aux_engine_model']}")
        print(f"  SFOC: {config['main_engine_sfoc']} g/kWh")
    
    print("\n=== Operating Profile ===")
    profile = db.get_profile(1)
    print(f"Vessel: {profile['vessel_type']}")
    print(f"Design: {profile['design_speed_knots']} knots @ {profile['design_power_kw']} kW")
    print(f"Sailing: {profile['sailing_hours']:.0f} hours @ {profile['sailing_prop_power_kw']:.0f} kW")
    print(f"Annual hours: {profile['sailing_hours'] + profile['maneuvering_hours'] + profile['port_hours']:.0f}")
    
    db.close()