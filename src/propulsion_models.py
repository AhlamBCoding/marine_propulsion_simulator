import numpy as np

class PropulsionSystem:
    """Base class for marine propulsion systems using real SFOC data"""
    
    def __init__(self, config_data):
        self.name = config_data['name']
        self.type = config_data['type']
        self.config = config_data
    
    def calculate_fuel_consumption(self, power_kw, hours, mode='normal'):
        """
        Calculate fuel consumption using SFOC (Specific Fuel Oil Consumption)
        
        SFOC units: g/kWh (grams of fuel per kilowatt-hour)
        Formula: Fuel (kg) = Power (kW) × Hours (h) × SFOC (g/kWh) / 1000
        
        Args:
            power_kw: Power demand in kW
            hours: Operating hours
            mode: Operating mode (for hybrid battery usage)
        
        Returns:
            Fuel consumption in kg
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def calculate_emissions(self, fuel_kg):
        """Calculate emissions from fuel consumption"""
        co2_kg = fuel_kg * self.config['co2_factor']
        sox_kg = fuel_kg * self.config['sox_factor']
        
        return {
            'co2_kg': co2_kg,
            'sox_kg': sox_kg,
            'co2_tonnes': co2_kg / 1000,
            'sox_tonnes': sox_kg / 1000
        }
    
    def calculate_cost(self, fuel_kg):
        """Calculate fuel cost"""
        fuel_tonnes = fuel_kg / 1000
        fuel_cost = fuel_tonnes * self.config['fuel_price']
        return fuel_cost


class DieselMechanicalPropulsion(PropulsionSystem):
    """
    Configuration A: Conventional Diesel-Mechanical
    - Main: Wärtsilä 8L32 (4640 kW) - SFOC: 181.0 g/kWh
    - Aux: 2× Wärtsilä 9L20 (1800 kW) - SFOC: 195.1 g/kWh
    """
    
    def __init__(self, config_data):
        super().__init__(config_data)
        self.main_sfoc = config_data['main_engine_sfoc']  # 181.0 g/kWh
        self.aux_sfoc = config_data['aux_engine_sfoc']    # 195.1 g/kWh
    
    def calculate_fuel_consumption(self, power_kw, hours, mode='normal'):
        """
        For diesel-mechanical:
        - Propulsion power goes to main engine
        - Electric power goes to auxiliary gensets
        
        We use a weighted average SFOC based on power distribution
        """
        # Simplified: use weighted average of main and aux SFOC
        # In reality, would split propulsion vs electric loads
        # For this study, we'll use a conservative weighted average
        
        # Assume 80% of total power is propulsion (main engine)
        # and 20% is electric (auxiliaries)
        main_power_ratio = 0.80
        aux_power_ratio = 0.20
        
        weighted_sfoc = (self.main_sfoc * main_power_ratio + 
                        self.aux_sfoc * aux_power_ratio)
        
        fuel_kg = (power_kw * hours * weighted_sfoc) / 1000
        return fuel_kg


class DualFuelLNGPropulsion(PropulsionSystem):
    """
    Configuration B: Dual-Fuel LNG
    - Main: Wärtsilä 8V31DF (4800 kW)
      - Gas mode: SFOC 157.5 g/kWh
      - Diesel mode: SFOC 176.9 g/kWh
    - Aux: 2× Wärtsilä 8L20DF (1280 kW)
      - Gas mode: SFOC 172.0 g/kWh
    - Operation: 95% LNG, 5% MDO backup
    """
    
    def __init__(self, config_data):
        super().__init__(config_data)
        self.sfoc_gas = config_data['sfoc_gas']          # 157.5 g/kWh
        self.sfoc_diesel = config_data['sfoc_diesel']    # 176.9 g/kWh
        self.lng_ratio = config_data['lng_ratio']        # 0.95
        self.pilot_fuel = config_data['pilot_fuel']      # 5.2 g/kWh
        self.aux_sfoc_gas = config_data['aux_engine_sfoc']  # 172.0 g/kWh
        
        # Weighted SFOC based on main/aux split (similar to Config A)
        self.sfoc_gas_weighted = (self.sfoc_gas * 0.80 + 
                                 self.aux_sfoc_gas * 0.20)
        self.sfoc_diesel_weighted = self.sfoc_diesel * 0.95  # Approximate
    
    def calculate_fuel_consumption(self, power_kw, hours, mode='normal'):
        """
        Calculate combined LNG and MDO consumption
        95% operation on LNG, 5% on MDO backup
        """
        # Gas mode operation (95% of time)
        gas_hours = hours * self.lng_ratio
        gas_fuel_kg = (power_kw * gas_hours * self.sfoc_gas_weighted) / 1000
        
        # Add pilot fuel (small amount of diesel even in gas mode)
        pilot_fuel_kg = (power_kw * gas_hours * self.pilot_fuel) / 1000
        
        # Diesel mode operation (5% of time)
        diesel_hours = hours * (1 - self.lng_ratio)
        diesel_fuel_kg = (power_kw * diesel_hours * self.sfoc_diesel_weighted) / 1000
        
        # Return LNG equivalent for primary metric
        # (In reality, would track separately)
        total_fuel_kg = gas_fuel_kg + diesel_fuel_kg + pilot_fuel_kg
        
        return total_fuel_kg
    
    def calculate_emissions(self, fuel_kg):
        """
        Calculate emissions accounting for LNG and MDO mix
        LNG: 2.75 kg CO2/kg fuel
        MDO: 3.206 kg CO2/kg fuel
        Plus methane slip consideration
        """
        # Weighted CO2 factor
        lng_co2_factor = 2.75
        mdo_co2_factor = 3.206
        
        weighted_co2_factor = (lng_co2_factor * self.lng_ratio + 
                              mdo_co2_factor * (1 - self.lng_ratio))
        
        # Add 1.5% methane slip (CH4 has 28× GWP of CO2)
        methane_slip_factor = 0.015 * 28
        total_co2_factor = weighted_co2_factor + methane_slip_factor
        
        co2_kg = fuel_kg * total_co2_factor
        sox_kg = fuel_kg * (1 - self.lng_ratio) * 0.001  # Only from diesel mode
        
        return {
            'co2_kg': co2_kg,
            'sox_kg': sox_kg,
            'co2_tonnes': co2_kg / 1000,
            'sox_tonnes': sox_kg / 1000
        }
    
    def calculate_cost(self, fuel_kg):
        """Calculate combined fuel cost (LNG + MDO)"""
        lng_cost = fuel_kg * self.lng_ratio * self.config['fuel_price'] / 1000
        mdo_cost = fuel_kg * (1 - self.lng_ratio) * self.config['fuel_price_gas'] / 1000
        return lng_cost + mdo_cost


class HybridElectricPropulsion(PropulsionSystem):
    """
    Configuration C: Diesel-Electric Hybrid
    - Gensets: 4× Wärtsilä 8L20 (1600 kW) - SFOC: 194.5 g/kWh
    - Battery: 1500 kWh
    - Electric motors: 97% efficiency
    """
    
    def __init__(self, config_data):
        super().__init__(config_data)
        self.genset_sfoc = config_data['aux_engine_sfoc']  # 194.5 g/kWh
        self.battery_capacity = config_data['battery_capacity']  # 1500 kWh
        self.battery_efficiency = config_data['battery_efficiency']  # 0.95
        self.motor_efficiency = config_data['motor_efficiency']  # 0.97
    
    def calculate_fuel_consumption(self, power_kw, hours, mode='sailing'):
        """
        For hybrid diesel-electric:
        - All power goes through gensets (except battery-powered port ops)
        - Propulsion power has motor losses
        - Port operations can use battery
        
        Args:
            mode: 'sailing', 'maneuvering', or 'port'
        """
        # Assume 80% of power is propulsion, 20% is electric load
        propulsion_power = power_kw * 0.80
        electric_load = power_kw * 0.20
        
        # Propulsion goes through electric motor (97% efficient)
        # So gensets must produce: propulsion / motor_efficiency
        genset_power_for_propulsion = propulsion_power / self.motor_efficiency
        
        # Total genset power needed
        total_genset_power = genset_power_for_propulsion + electric_load
        
        # Port mode can use battery
        if mode == 'port':
            # Battery can cover up to 3 hours of port operations
            max_battery_hours = self.battery_capacity / power_kw
            battery_hours = min(hours, max_battery_hours)
            genset_hours = max(0, hours - battery_hours)
            
            # Fuel only for genset operation
            fuel_kg = (total_genset_power * genset_hours * self.genset_sfoc) / 1000
        else:
            # Normal operation - all from gensets
            fuel_kg = (total_genset_power * hours * self.genset_sfoc) / 1000
        
        return fuel_kg


def create_propulsion_system(config_data):
    """Factory function to create appropriate propulsion system"""
    system_type = config_data['type']
    
    if system_type == 'diesel':
        return DieselMechanicalPropulsion(config_data)
    elif system_type == 'dual-fuel':
        return DualFuelLNGPropulsion(config_data)
    elif system_type == 'hybrid':
        return HybridElectricPropulsion(config_data)
    else:
        raise ValueError(f"Unknown propulsion type: {system_type}")


if __name__ == "__main__":
    # Test propulsion models
    print("Testing propulsion models with real Wärtsilä data...")
    
    # Test Configuration A
    config_a = {
        'name': 'Diesel-Mechanical',
        'type': 'diesel',
        'main_engine_sfoc': 181.0,
        'aux_engine_sfoc': 195.1,
        'co2_factor': 3.206,
        'sox_factor': 0.001,
        'fuel_price': 650.0
    }
    
    system_a = create_propulsion_system(config_a)
    fuel = system_a.calculate_fuel_consumption(4000, 100)  # 4000 kW, 100 hours
    print(f"\nConfig A - Fuel consumption: {fuel:.1f} kg")
    print(f"  Emissions: {system_a.calculate_emissions(fuel)}")
    print(f"  Cost: ${system_a.calculate_cost(fuel):,.0f}")