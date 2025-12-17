from datetime import datetime
from src.propulsion_models import create_propulsion_system

class VoyageSimulator:
    """Simulates vessel voyages with different propulsion systems"""
    
    def __init__(self, vessel_power_kw=5000):
        self.vessel_power_kw = vessel_power_kw  # Maximum power rating
    
    def simulate_voyage(self, propulsion_system_data, operating_profile_data):
        """
        Run a complete voyage simulation
        Returns dict with fuel, emissions, and cost
        """
        # Create propulsion system
        propulsion = create_propulsion_system(propulsion_system_data)
        
        # Extract operating profile
        cruising_hours = operating_profile_data['cruising_hours']
        maneuvering_hours = operating_profile_data['maneuvering_hours']
        port_hours = operating_profile_data['port_hours']
        
        cruising_power_pct = operating_profile_data['cruising_power_pct']
        maneuvering_power_pct = operating_profile_data['maneuvering_power_pct']
        port_power_pct = operating_profile_data['port_power_pct']
        
        # Calculate power for each phase
        cruising_power = self.vessel_power_kw * cruising_power_pct
        maneuvering_power = self.vessel_power_kw * maneuvering_power_pct
        port_power = self.vessel_power_kw * port_power_pct
        
        # Calculate fuel consumption for each phase
        cruising_fuel = propulsion.calculate_fuel_consumption(cruising_power, cruising_hours)
        maneuvering_fuel = propulsion.calculate_fuel_consumption(maneuvering_power, maneuvering_hours)
        port_fuel = propulsion.calculate_fuel_consumption(port_power, port_hours)
        
        total_fuel = cruising_fuel + maneuvering_fuel + port_fuel
        
        # Calculate emissions
        total_emissions = propulsion.calculate_emissions(total_fuel)
        
        # Calculate costs
        fuel_cost = propulsion.calculate_fuel_cost(total_fuel)
        
        # Annualized capital cost (10 year lifespan, 5% discount rate)
        annual_capital_cost = propulsion.initial_cost * 0.1295  # Capital recovery factor
        
        # Assume 250 voyages per year for total annual cost
        voyages_per_year = 250
        total_voyage_cost = fuel_cost + (annual_capital_cost / voyages_per_year)
        
        return {
            'propulsion_system': propulsion.name,
            'total_fuel_consumption': total_fuel,
            'total_co2_emissions': total_emissions,
            'fuel_cost': fuel_cost,
            'total_voyage_cost': total_voyage_cost,
            'breakdown': {
                'cruising': {'fuel': cruising_fuel, 'hours': cruising_hours},
                'maneuvering': {'fuel': maneuvering_fuel, 'hours': maneuvering_hours},
                'port': {'fuel': port_fuel, 'hours': port_hours}
            }
        }
    
    def compare_systems(self, propulsion_systems_df, operating_profile):
        """Compare all propulsion systems for a given operating profile"""
        results = []
        
        for _, system in propulsion_systems_df.iterrows():
            result = self.simulate_voyage(system.to_dict(), operating_profile)
            result['system_id'] = system['id']
            result['profile_id'] = operating_profile['id']
            results.append(result)
        
        return results