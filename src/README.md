# Marine Propulsion System Simulator

A Python-based simulation tool for comparing fuel consumption, emissions, and costs across different marine propulsion configurations.

## Overview

This project demonstrates data-driven decision making for marine system design by:
- Modeling diesel, hybrid, and electric propulsion systems
- Simulating realistic voyage profiles
- Calculating fuel consumption, CO₂ emissions, and operating costs
- Providing visual comparisons and value propositions

## Features

- **SQLite Database**: Stores propulsion systems, operating profiles, and simulation results
- **Physics-Based Models**: Simplified but realistic propulsion system simulations
- **Comparative Analysis**: Side-by-side comparison of different configurations
- **Value Propositions**: Automated generation of business cases with ROI calculations
- **Visualizations**: Professional charts for presentations and reports

## Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd marine_propulsion_simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the complete simulation:
```bash
python main.py
```

This will:
1. Initialize the database with sample data
2. Run simulations for all propulsion systems
3. Generate comparison visualizations in `outputs/`
4. Display a value proposition summary
5. Save results to the database

## Project Structure
```
marine_propulsion_simulator/
├── data/
│   └── vessel_data.db          # SQLite database
├── src/
│   ├── database.py             # Database management
│   ├── propulsion_models.py    # System simulation models
│   ├── simulator.py            # Voyage simulation engine
│   └── visualizer.py           # Plotting and reporting
├── outputs/                     # Generated visualizations
├── main.py                      # Main execution script
├── requirements.txt
└── README.md
```

## Key Results

The simulator compares three propulsion systems:

1. **Conventional Diesel** (Baseline)
   - Heavy fuel oil
   - 40% efficiency
   - Lowest capital cost

2. **Diesel-Electric Hybrid**
   - Marine diesel + battery support
   - 45% efficiency
   - Reduced emissions in port

3. **Battery Electric**
   - Zero direct emissions
   - 90% efficiency
   - Higher capital cost, lowest operating cost

## Extending the Project

Potential enhancements:
- Add more propulsion types (LNG, hydrogen fuel cells)
- Include weather conditions and route optimization
- Integrate real vessel performance data
- Add economic scenario analysis (carbon pricing)
- Implement multi-vessel fleet optimization

## Technical Notes

- Fuel consumption uses simplified energy balance equations
- CO₂ factors from IMO guidelines
- Cost models include capital amortization over 10 years
- Operating profiles based on typical ferry operations

## Author

Created as a demonstration project for marine system simulation capabilities.

## License

MIT License