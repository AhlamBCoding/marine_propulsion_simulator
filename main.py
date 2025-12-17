#!/usr/bin/env python3
"""
Marine Propulsion System Simulator
Compares different propulsion configurations for marine vessels
"""

import os
from datetime import datetime
from src.database import VesselDatabase
from src.simulator import VoyageSimulator
from src.visualizer import SimulationVisualizer

def main():
    print("\n" + "="*70)
    print("MARINE PROPULSION SYSTEM SIMULATOR".center(70))
    print("="*70 + "\n")
    
    # Initialize database
    print("📊 Initializing database...")
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    db = VesselDatabase()
    
    # Load data
    propulsion_systems = db.get_propulsion_systems()
    operating_profiles = db.get_operating_profiles()
    
    print(f"✓ Loaded {len(propulsion_systems)} propulsion systems")
    print(f"✓ Loaded {len(operating_profiles)} operating profiles\n")
    
    # Display available systems
    print("Available Propulsion Systems:")
    for _, system in propulsion_systems.iterrows():
        print(f"  • {system['name']} ({system['type']})")
    
    print("\nAvailable Operating Profiles:")
    for _, profile in operating_profiles.iterrows():
        print(f"  • {profile['profile_name']}")
    
    # Select profile for simulation (using first one)
    selected_profile = operating_profiles.iloc[0].to_dict()
    print(f"\n🚢 Simulating: {selected_profile['profile_name']}")
    print(f"   Duration: {selected_profile['cruising_hours'] + selected_profile['maneuvering_hours'] + selected_profile['port_hours']:.1f} hours")
    
    # Run simulation
    print("\n⚙️  Running simulations...")
    simulator = VoyageSimulator(vessel_power_kw=5000)
    results = simulator.compare_systems(propulsion_systems, selected_profile)
    
    print("✓ Simulations complete\n")
    
    # Save results to database
    timestamp = datetime.now().isoformat()
    for result in results:
        db.save_simulation_result((
            timestamp,
            result['system_id'],
            result['profile_id'],
            result['total_fuel_consumption'],
            result['total_co2_emissions'],
            result['total_voyage_cost']
        ))
    
    print("💾 Results saved to database")
    
    # Visualize results
    print("\n📈 Generating visualizations...")
    visualizer = SimulationVisualizer()
    
    # Main comparison plot
    fig1 = visualizer.plot_comparison(results, save_path='outputs/comparison.png')
    print("✓ Saved: outputs/comparison.png")
    
    # Emissions savings plot
    fig2 = visualizer.plot_emissions_savings(results, baseline_idx=0)
    fig2.savefig('outputs/emissions_savings.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: outputs/emissions_savings.png")
    
    # Sensitivity analysis
    fig3 = visualizer.plot_sensitivity_analysis(results)
    fig3.savefig('outputs/sensitivity.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: outputs/sensitivity.png")
    
    # Generate value proposition
    visualizer.create_value_proposition(results, baseline_idx=0, years=10)
    
    # Print summary table
    print("\n📋 Simulation Results Summary:")
    print("-" * 90)
    print(f"{'System':<30} {'Fuel (kg)':<15} {'CO₂ (kg)':<15} {'Cost ($)':<15}")
    print("-" * 90)
    for result in results:
        print(f"{result['propulsion_system']:<30} "
              f"{result['total_fuel_consumption']:<15.1f} "
              f"{result['total_co2_emissions']:<15.1f} "
              f"{result['total_voyage_cost']:<15.2f}")
    print("-" * 90 + "\n")
    
    # Close database
    db.close()
    
    print("✅ Analysis complete! Check the outputs/ folder for visualizations.\n")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
Marine Propulsion System Simulator
Compares different propulsion configurations for marine vessels
"""

import os
from datetime import datetime
from src.database import VesselDatabase
from src.simulator import VoyageSimulator
from src.visualizer import SimulationVisualizer

def main():
    print("\n" + "="*70)
    print("MARINE PROPULSION SYSTEM SIMULATOR".center(70))
    print("="*70 + "\n")
    
    # Initialize database
    print("📊 Initializing database...")
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    db = VesselDatabase()
    
    # Load data
    propulsion_systems = db.get_propulsion_systems()
    operating_profiles = db.get_operating_profiles()
    
    print(f"✓ Loaded {len(propulsion_systems)} propulsion systems")
    print(f"✓ Loaded {len(operating_profiles)} operating profiles\n")
    
    # Display available systems
    print("Available Propulsion Systems:")
    for _, system in propulsion_systems.iterrows():
        print(f"  • {system['name']} ({system['type']})")
    
    print("\nAvailable Operating Profiles:")
    for _, profile in operating_profiles.iterrows():
        print(f"  • {profile['profile_name']}")
    
    # Select profile for simulation (using first one)
    selected_profile = operating_profiles.iloc[0].to_dict()
    print(f"\n🚢 Simulating: {selected_profile['profile_name']}")
    print(f"   Duration: {selected_profile['cruising_hours'] + selected_profile['maneuvering_hours'] + selected_profile['port_hours']:.1f} hours")
    
    # Run simulation
    print("\n⚙️  Running simulations...")
    simulator = VoyageSimulator(vessel_power_kw=5000)
    results = simulator.compare_systems(propulsion_systems, selected_profile)
    
    print("✓ Simulations complete\n")
    
    # Save results to database
    timestamp = datetime.now().isoformat()
    for result in results:
        db.save_simulation_result((
            timestamp,
            result['system_id'],
            result['profile_id'],
            result['total_fuel_consumption'],
            result['total_co2_emissions'],
            result['total_voyage_cost']
        ))
    
    print("💾 Results saved to database")
    
    # Visualize results
    print("\n📈 Generating visualizations...")
    visualizer = SimulationVisualizer()
    
    # Main comparison plot
    fig1 = visualizer.plot_comparison(results, save_path='outputs/comparison.png')
    print("✓ Saved: outputs/comparison.png")
    
    # Emissions savings plot
    fig2 = visualizer.plot_emissions_savings(results, baseline_idx=0)
    fig2.savefig('outputs/emissions_savings.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: outputs/emissions_savings.png")
    
    # Sensitivity analysis
    fig3 = visualizer.plot_sensitivity_analysis(results)
    fig3.savefig('outputs/sensitivity.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: outputs/sensitivity.png")
    
    # Generate value proposition
    visualizer.create_value_proposition(results, baseline_idx=0, years=10)
    
    # Print summary table
    print("\n📋 Simulation Results Summary:")
    print("-" * 90)
    print(f"{'System':<30} {'Fuel (kg)':<15} {'CO₂ (kg)':<15} {'Cost ($)':<15}")
    print("-" * 90)
    for result in results:
        print(f"{result['propulsion_system']:<30} "
              f"{result['total_fuel_consumption']:<15.1f} "
              f"{result['total_co2_emissions']:<15.1f} "
              f"{result['total_voyage_cost']:<15.2f}")
    print("-" * 90 + "\n")
    
    # Close database
    db.close()
    
    print("✅ Analysis complete! Check the outputs/ folder for visualizations.\n")

if __name__ == "__main__":
    main()