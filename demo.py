import os
from src.database import VesselDatabase
from src.simulator import VoyageSimulator
from src.visualizer import SimulationVisualizer

def quick_demo():
    
    print("\n" + "="*70)
    print("MARINE PROPULSION SIMULATOR - QUICK DEMO".center(70))
    print("="*70 + "\n")
    
    # Setup
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    db = VesselDatabase()
    simulator = VoyageSimulator()
    visualizer = SimulationVisualizer()
    
    # Get data
    configs = db.get_propulsion_systems()
    profile = db.get_profile(1).to_dict()
    
    print(f"📊 Vessel Type: {profile['vessel_type']}")
    print(f"📊 Route Profile: {profile['profile_name']}")
    print(f"📊 Design Speed: {profile['design_speed_knots']} knots @ {profile['design_power_kw']} kW")
    print(f"\n⚙️  Comparing {len(configs)} propulsion configurations...\n")
    
    # Run simulation
    results = simulator.compare_configurations(configs, profile)
    results = simulator.calculate_relative_performance(results, baseline_idx=0)
    
    # Quick summary
    print("RESULTS SUMMARY:")
    print("-"*70)
    print(f"{'Configuration':<30} {'CO₂ (t/year)':<15} {'Cost ($/year)':<15}")
    print("-"*70)
    
    for r in results:
        print(f"{r['configuration']:<30} {r['total_co2_tonnes']:<15,.0f} ${r['total_annual_cost_usd']:<14,.0f}")
    
    print("-"*70)
    
    # Key findings
    print("\n💡 KEY FINDINGS:")
    print(f"   • Dual-Fuel LNG reduces CO₂ by {results[1]['vs_baseline']['co2_reduction_pct']:.1f}%")
    print(f"   • Hybrid can operate zero-emission in port (1500 kWh battery)")
    print(f"   • Cost increase: {results[1]['vs_baseline']['cost_difference_pct']:.1f}% (LNG), {results[2]['vs_baseline']['cost_difference_pct']:.1f}% (Hybrid)")
    
    # Generate one quick visualization
    print("\n📈 Generating comparison chart...")
    visualizer.plot_comparison_dashboard(results, save_path='outputs/demo_comparison.png')
    
    print("\n✅ Demo complete! Check outputs/demo_comparison.png\n")
    
    db.close()
    
    return results


if __name__ == "__main__":
    quick_demo()