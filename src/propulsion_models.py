import numpy as np

class PropulsionSystem:
    """Base class for propulsion systems"""
    
    def __init__(self, name, efficiency, fuel_type, co2_factor, initial_cost):
        self.name = name
        self.efficiency = efficiency
        self.fuel_type = fuel_type
        self.co2_factor = co2_factor  # kg CO2 per kg fuel
        self.initial_cost = initial_cost
    
    def calculate_fuel_consumption(self, power_kw, hours):
        """
        Calculate fuel consumption in kg
        Simplified model: fuel = (power * hours) / (efficiency * fuel_energy_density)
        """
        # Energy density approximations (kWh/kg)
        energy_density = {
            'HFO': 11.8,  # Heavy Fuel Oil
            'MDO': 11.9,  # Marine Diesel Oil
            'electricity': 1.0  # Placeholder for battery discharge
        }
        
        density = energy_density.get(self.fuel_type, 11.8)
        fuel_consumption = (power_kw * hours) / (self.efficiency * density)
        
        return fuel_consumption
    
    def calculate_emissions(self, fuel_consumption):
        """Calculate CO2 emissions in kg"""
        return fuel_consumption * self.co2_factor
    
    def calculate_fuel_cost(self, fuel_consumption):
        """Calculate fuel cost"""
        # Fuel prices ($/kg or $/kWh for electricity)
        fuel_prices = {
            'HFO': 0.45,
            'MDO': 0.65,
            'electricity': 0.12
        }
        
        price = fuel_prices.get(self.fuel_type, 0.5)
        return fuel_consumption * price


class DieselPropulsion(PropulsionSystem):
    """Conventional diesel propulsion"""
    
    def __init__(self, system_data):
        super().__init__(
            name=system_data['name'],
            efficiency=system_data['efficiency'],
            fuel_type=system_data['fuel_type'],
            co2_factor=system_data['co2_factor'],
            initial_cost=system_data['initial_cost']
        )


class HybridPropulsion(PropulsionSystem):
    """Diesel-electric hybrid with battery support"""
    
    def __init__(self, system_data):
        super().__init__(
            name=system_data['name'],
            efficiency=system_data['efficiency'],
            fuel_type=system_data['fuel_type'],
            co2_factor=system_data['co2_factor'],
            initial_cost=system_data['initial_cost']
        )
        self.battery_capacity_kwh = 500  # kWh
    
    def calculate_fuel_consumption(self, power_kw, hours):
        """
        Hybrid can use battery for low power operations
        Assume battery covers 20% of low-power port operations
        """
        # Battery covers some energy
        total_energy = power_kw * hours
        battery_contribution = min(self.battery_capacity_kwh, total_energy * 0.2)
        diesel_energy = total_energy - battery_contribution
        
        # Calculate fuel for diesel portion
        fuel_consumption = (diesel_energy) / (self.efficiency * 11.9)
        
        return fuel_consumption


class ElectricPropulsion(PropulsionSystem):
    """Full battery electric propulsion"""
    
    def __init__(self, system_data):
        super().__init__(
            name=system_data['name'],
            efficiency=system_data['efficiency'],
            fuel_type=system_data['fuel_type'],
            co2_factor=system_data['co2_factor'],
            initial_cost=system_data['initial_cost']
        )
        self.battery_capacity_kwh = 5000  # kWh
    
    def calculate_fuel_consumption(self, power_kw, hours):
        """
        For electric, 'fuel consumption' is electrical energy
        Returns kWh consumed
        """
        energy_consumed = (power_kw * hours) / self.efficiency
        return energy_consumed


def create_propulsion_system(system_data):
    """Factory function to create appropriate propulsion system"""
    system_type = system_data['type']
    
    if system_type == 'diesel':
        return DieselPropulsion(system_data)
    elif system_type == 'hybrid':
        return HybridPropulsion(system_data)
    elif system_type == 'electric':
        return ElectricPropulsion(system_data)
    else:
        raise ValueError(f"Unknown propulsion type: {system_type}")