"""Quick test to verify the everything works"""

from src.database import VesselDatabase
from src.simulator import VoyageSimulator

def test_basic_simulation():
    print("Running basic test...")
    
    # Initialize
    db = VesselDatabase('data/test_vessel_data.db')
    simulator = VoyageSimulator(vessel_power_kw=5000)
    
    # Get data
    systems = db.get_propulsion_systems()
    profiles = db.get_operating_profiles()
    
    # Run simulation
    profile = profiles.iloc[0].to_dict()
    results = simulator.compare_systems(systems, profile)
    
    # Verify results
    assert len(results) == 3, "Should have 3 results"
    assert all('total_fuel_consumption' in r for r in results), "Missing fuel data"
    assert all('total_co2_emissions' in r for r in results), "Missing emissions data"
    
    print("✓ All tests passed!")
    
    db.close()
    
    # Clean up test database
    import os
    os.remove('data/test_vessel_data.db')

if __name__ == "__main__":
    test_basic_simulation()