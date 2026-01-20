import os
import sys
from datetime import datetime
from src.database import VesselDatabase
from src.simulator import VoyageSimulator
from src.visualizer import SimulationVisualizer

def main():
    """Run complete simulation and generate all outputs"""
    
    print("\n" + "="*80)
    print("SHORT-SEA TANKER PROPULSION SYSTEM COMPARISON".center(80))
    print("Wärtsilä Marine Systems Simulation Study".center(80))
    print("="*80 + "\n")
    
    # Create output directory
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Initialize database
    print("📊 Step 1: Initializing database with real Wärtsilä engine data...")
    db = VesselDatabase()
    
    # Load configurations and profile
    configs = db.get_propulsion_systems()
    profile = db.get_profile(1).to_dict()
    
    print(f"   ✓ Loaded {len(configs)} propulsion configurations")
    print(f"   ✓ Operational profile: {profile['profile_name']}")
    print(f"   ✓ Annual operating hours: {profile['sailing_hours'] + profile['maneuvering_hours'] + profile['port_hours']:.0f}\n")
    
    # Display configurations
    print("Configurations to be evaluated:")
    for _, config in configs.iterrows():
        print(f"\n   {config['name']}:")
        if config['main_engine_model']:
            print(f"      Main: {config['main_engine_model']} ({config['main_engine_power']:.0f} kW)")
        if config['aux_engine_model']:
            count = config['aux_engine_count'] if config['aux_engine_count'] else 0
            print(f"      Aux:  {count}× {config['aux_engine_model']} ({config['aux_engine_power']:.0f} kW each)")
        if config['battery_capacity']:
            print(f"      Battery: {config['battery_capacity']:.0f} kWh")
    
    print("\n" + "-"*80 + "\n")
    
    # Run simulations
    print("⚙️  Step 2: Running voyage simulations...")
    simulator = VoyageSimulator()
    results = simulator.compare_configurations(configs, profile)
    results = simulator.calculate_relative_performance(results, baseline_idx=0)
    print("   ✓ Simulations complete\n")
    
    # Save results to database
    print("💾 Step 3: Saving results to database...")
    timestamp = datetime.now().isoformat()
    for result in results:
        db.save_simulation_result((
            timestamp,
            result['config_id'],
            1,  # profile_id
            result['total_fuel_kg'],
            result['total_co2_tonnes'],
            result['total_sox_tonnes'],
            result['fuel_cost_usd'],
            result['capital_cost_annual_usd'],
            result['total_annual_cost_usd'],
            result['breakdown']['sailing']['fuel_kg'],
            result['breakdown']['maneuvering']['fuel_kg'],
            result['breakdown']['port']['fuel_kg']
        ))
    print("   ✓ Results saved\n")
    
    # Generate visualizations
    print("📈 Step 4: Generating visualizations...")
    visualizer = SimulationVisualizer()
    
    # Main comparison dashboard
    fig1 = visualizer.plot_comparison_dashboard(
        results, 
        save_path='outputs/comparison_dashboard.png'
    )
    
    # Emissions reduction chart
    fig2 = visualizer.plot_emissions_reduction(
        results, 
        baseline_idx=0,
        save_path='outputs/emissions_reduction.png'
    )
    
    # Cost breakdown
    fig3 = visualizer.plot_cost_breakdown(
        results,
        save_path='outputs/cost_breakdown.png'
    )
    
    print("   ✓ All visualizations generated\n")
    
    # Display results
    print("="*80)
    print("SIMULATION RESULTS")
    print("="*80)
    
    visualizer.export_summary_table(results)
    
    # Detailed breakdown
    print("\nDETAILED RESULTS BY CONFIGURATION:")
    print("="*80)
    
    for result in results:
        print(f"\n{result['configuration']}")
        print("-"*80)
        print(f"  Annual Fuel Consumption:   {result['total_fuel_tonnes']:>10,.1f} tonnes")
        print(f"  Annual CO₂ Emissions:      {result['total_co2_tonnes']:>10,.1f} tonnes")
        print(f"  Annual SOx Emissions:      {result['total_sox_tonnes']:>10,.2f} tonnes")
        print(f"\n  Fuel Cost:                 ${result['fuel_cost_usd']:>10,.0f}")
        print(f"  Amortized Capital Cost:    ${result['capital_cost_annual_usd']:>10,.0f}")
        print(f"  Total Annual Cost:         ${result['total_annual_cost_usd']:>10,.0f}")
        
        print(f"\n  Fuel Breakdown:")
        print(f"    Sailing:      {result['breakdown']['sailing']['fuel_kg']/1000:>6.1f} tonnes ({result['breakdown']['sailing']['percentage']:>5.1f}%)")
        print(f"    Maneuvering:  {result['breakdown']['maneuvering']['fuel_kg']/1000:>6.1f} tonnes ({result['breakdown']['maneuvering']['percentage']:>5.1f}%)")
        print(f"    Port:         {result['breakdown']['port']['fuel_kg']/1000:>6.1f} tonnes ({result['breakdown']['port']['percentage']:>5.1f}%)")
        
        if not result['vs_baseline']['is_baseline']:
            print(f"\n  Performance vs Baseline:")
            print(f"    Fuel Reduction:  {result['vs_baseline']['fuel_reduction_pct']:>10.1f}%")
            print(f"    CO₂ Reduction:   {result['vs_baseline']['co2_reduction_pct']:>10.1f}%")
            print(f"    Cost Difference: {result['vs_baseline']['cost_difference_pct']:>+10.1f}%")
    
    print("\n" + "="*80 + "\n")
    
    # Value proposition summary
    print("📊 Step 5: Generating value proposition summary...\n")
    visualizer.create_value_proposition_summary(results, baseline_idx=0)
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print("\n✅ Simulation Complete!")
    print(f"\n   Configurations evaluated: {len(results)}")
    print(f"   Outputs generated:")
    print(f"      • outputs/comparison_dashboard.png")
    print(f"      • outputs/emissions_reduction.png")
    print(f"      • outputs/cost_breakdown.png")
    print(f"      • Database: data/vessel_data.db")
    
    print("\n" + "="*80 + "\n")
    
    # Close database
    db.close()
    
    return results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)