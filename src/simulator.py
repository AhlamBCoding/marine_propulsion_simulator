from datetime import datetime
from src.propulsion_models import create_propulsion_system

class VoyageSimulator:
    """Simulates annual vessel operations for different propulsion configurations"""
    
    def __init__(self):
        pass
    
    def simulate_annual_operation(self, config_data, profile_data):
        """
        Run complete annual simulation for a propulsion configuration
        
        Args:
            config_data: Dictionary with propulsion system configuration
            profile_data: Dictionary with operational profile
        
        Returns:
            Dictionary with annual results
        """
        # Create propulsion system
        propulsion = create_propulsion_system(config_data)
        
        # Extract operational profile
        sailing_hours = profile_data['sailing_hours']
        sailing_prop_power = profile_data['sailing_prop_power_kw']
        sailing_elec_power = profile_data['sailing_elec_power_kw']
        
        maneuvering_hours = profile_data['maneuvering_hours']
        maneuvering_prop_power = profile_data['maneuvering_prop_power_kw']
        maneuvering_elec_power = profile_data['maneuvering_elec_power_kw']
        
        port_hours = profile_data['port_hours']
        port_prop_power = profile_data['port_prop_power_kw']
        port_elec_power = profile_data['port_elec_power_kw']
        
        # Calculate total power for each mode
        sailing_total_power = sailing_prop_power + sailing_elec_power
        maneuvering_total_power = maneuvering_prop_power + maneuvering_elec_power
        port_total_power = port_prop_power + port_elec_power
        
        # Calculate fuel consumption for each mode
        sailing_fuel = propulsion.calculate_fuel_consumption(
            sailing_total_power, sailing_hours, mode='sailing'
        )
        
        maneuvering_fuel = propulsion.calculate_fuel_consumption(
            maneuvering_total_power, maneuvering_hours, mode='maneuvering'
        )
        
        port_fuel = propulsion.calculate_fuel_consumption(
            port_total_power, port_hours, mode='port'
        )
        
        # Total annual fuel consumption
        total_fuel_kg = sailing_fuel + maneuvering_fuel + port_fuel
        
        # Calculate emissions
        emissions = propulsion.calculate_emissions(total_fuel_kg)
        
        # Calculate costs
        fuel_cost = propulsion.calculate_cost(total_fuel_kg)
        
        # Capital cost (amortized over 20 years at 5% discount rate)
        # Using capital recovery factor: CRF = r(1+r)^n / ((1+r)^n - 1)
        discount_rate = 0.05
        lifespan_years = 20
        crf = discount_rate * (1 + discount_rate)**lifespan_years / \
              ((1 + discount_rate)**lifespan_years - 1)
        
        annual_capital_cost = config_data['initial_cost'] * crf
        
        # Total annual cost
        total_annual_cost = fuel_cost + annual_capital_cost
        
        # Compile results
        results = {
            'configuration': config_data['name'],
            'config_id': config_data['id'],
            
            # Annual totals
            'total_fuel_kg': total_fuel_kg,
            'total_fuel_tonnes': total_fuel_kg / 1000,
            'total_co2_kg': emissions['co2_kg'],
            'total_co2_tonnes': emissions['co2_tonnes'],
            'total_sox_kg': emissions['sox_kg'],
            'total_sox_tonnes': emissions['sox_tonnes'],
            
            # Costs
            'fuel_cost_usd': fuel_cost,
            'capital_cost_annual_usd': annual_capital_cost,
            'total_annual_cost_usd': total_annual_cost,
            
            # Breakdown by mode
            'breakdown': {
                'sailing': {
                    'hours': sailing_hours,
                    'power_kw': sailing_total_power,
                    'fuel_kg': sailing_fuel,
                    'percentage': (sailing_fuel / total_fuel_kg * 100) if total_fuel_kg > 0 else 0
                },
                'maneuvering': {
                    'hours': maneuvering_hours,
                    'power_kw': maneuvering_total_power,
                    'fuel_kg': maneuvering_fuel,
                    'percentage': (maneuvering_fuel / total_fuel_kg * 100) if total_fuel_kg > 0 else 0
                },
                'port': {
                    'hours': port_hours,
                    'power_kw': port_total_power,
                    'fuel_kg': port_fuel,
                    'percentage': (port_fuel / total_fuel_kg * 100) if total_fuel_kg > 0 else 0
                }
            },
            
            # Metadata
            'total_operating_hours': sailing_hours + maneuvering_hours + port_hours,
            'average_power_kw': (
                sailing_total_power * sailing_hours +
                maneuvering_total_power * maneuvering_hours +
                port_total_power * port_hours
            ) / (sailing_hours + maneuvering_hours + port_hours)
        }
        
        return results
    
    def compare_configurations(self, configs_df, profile_data):
        """
        Compare all configurations for a given operational profile
        
        Args:
            configs_df: DataFrame with all propulsion configurations
            profile_data: Dictionary with operational profile
        
        Returns:
            List of results dictionaries, one per configuration
        """
        results = []
        
        for _, config in configs_df.iterrows():
            result = self.simulate_annual_operation(
                config.to_dict(), 
                profile_data
            )
            results.append(result)
        
        return results
    
    def calculate_relative_performance(self, results, baseline_idx=0):
        """
        Calculate relative performance vs baseline
        
        Args:
            results: List of simulation results
            baseline_idx: Index of baseline configuration (default: 0)
        
        Returns:
            List of results with added relative metrics
        """
        baseline = results[baseline_idx]
        
        for i, result in enumerate(results):
            if i == baseline_idx:
                result['vs_baseline'] = {
                    'fuel_reduction_pct': 0.0,
                    'co2_reduction_pct': 0.0,
                    'cost_difference_pct': 0.0,
                    'is_baseline': True
                }
            else:
                fuel_reduction = (baseline['total_fuel_kg'] - result['total_fuel_kg']) / baseline['total_fuel_kg'] * 100
                co2_reduction = (baseline['total_co2_kg'] - result['total_co2_kg']) / baseline['total_co2_kg'] * 100
                cost_difference = (result['total_annual_cost_usd'] - baseline['total_annual_cost_usd']) / baseline['total_annual_cost_usd'] * 100
                
                result['vs_baseline'] = {
                    'fuel_reduction_pct': fuel_reduction,
                    'co2_reduction_pct': co2_reduction,
                    'cost_difference_pct': cost_difference,
                    'is_baseline': False
                }
        
        return results


if __name__ == "__main__":
    # Test simulator
    from src.database import VesselDatabase
    
    db = VesselDatabase()
    
    print("\n=== Running Voyage Simulation ===\n")
    
    # Get data
    configs = db.get_propulsion_systems()
    profile = db.get_profile(1).to_dict()
    
    print(f"Vessel: {profile['vessel_type']}")
    print(f"Annual operating hours: {profile['sailing_hours'] + profile['maneuvering_hours'] + profile['port_hours']:.0f}")
    print(f"\nSimulating {len(configs)} configurations...\n")
    
    # Run simulations
    simulator = VoyageSimulator()
    results = simulator.compare_configurations(configs, profile)
    results = simulator.calculate_relative_performance(results, baseline_idx=0)
    
    # Display results
    print("=" * 80)
    print("SIMULATION RESULTS")
    print("=" * 80)
    
    for result in results:
        print(f"\n{result['configuration']}")
        print("-" * 80)
        print(f"  Annual Fuel:       {result['total_fuel_tonnes']:>10,.1f} tonnes")
        print(f"  Annual CO₂:        {result['total_co2_tonnes']:>10,.1f} tonnes")
        print(f"  Fuel Cost:         ${result['fuel_cost_usd']:>10,.0f}")
        print(f"  Capital Cost:      ${result['capital_cost_annual_usd']:>10,.0f}")
        print(f"  Total Annual Cost: ${result['total_annual_cost_usd']:>10,.0f}")
        
        if not result['vs_baseline']['is_baseline']:
            print(f"\n  vs Baseline:")
            print(f"    Fuel reduction:  {result['vs_baseline']['fuel_reduction_pct']:>10.1f}%")
            print(f"    CO₂ reduction:   {result['vs_baseline']['co2_reduction_pct']:>10.1f}%")
            print(f"    Cost difference: {result['vs_baseline']['cost_difference_pct']:>+10.1f}%")
    
    print("\n" + "=" * 80)
    
    db.close()