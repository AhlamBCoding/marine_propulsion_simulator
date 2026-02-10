# Marine Propulsion System Simulator
## Short-Sea Tanker Configuration Comparison

A Python-based simulation tool for comparing marine propulsion configurations using real Wärtsilä engine data.

---

## Overview

This simulator evaluates three propulsion configurations for a short-sea tanker:

1. **Conventional Diesel-Mechanical** (Baseline)
   - Main: Wärtsilä 8L32 (4640 kW)
   - Aux: 2× Wärtsilä 9L20 (1800 kW each)
   - Fuel: MDO
   - SFOC: 181.0 g/kWh (main), 195.1 g/kWh (aux)

2. **Dual-Fuel LNG**
   - Main: Wärtsilä 8V31DF (4800 kW)
   - Aux: 2× Wärtsilä 8L20DF (1280 kW each)
   - Fuel: 95% LNG, 5% MDO backup
   - SFOC: 149 g/kWh (gas mode), 176.9 g/kWh (diesel mode)

3. **Diesel-Electric Hybrid**
   - Gensets: 4× Wärtsilä 8L20 (1600 kW each)
   - Battery: 1500 kWh Li-ion
   - Electric motors: 4500 kW @ 97% efficiency
   - SFOC: 194.5 g/kWh

---

## Features

✅ Real Wärtsilä engine data from configurator  
✅ Physics-based fuel consumption models (SFOC)  
✅ Cubic interpolation for sailing power  
✅ SQLite database for configurations and results  
✅ Professional visualizations for presentation  
✅ Automated value proposition generation  
✅ Cost-benefit analysis with 20-year lifecycle

---

## Installation

```bash
# Clone or download the project
cd marine_propulsion_simulator

# Create virtual environment
python -m venv marine_sys_sim_venv
source marine_sys_sim_venv/bin/activate  # Windows: marine_sys_sim_venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt
```

---

## Usage

### Quick Demo (2 minutes)

```bash
python demo.py
```

This runs a quick comparison and generates one summary chart.

### Full Simulation

```bash
python main.py
```

This will:
1. Initialize database with real Wärtsilä engine data
2. Run annual simulations for all configurations
3. Generate comparison visualizations
4. Save results to database
5. Display value proposition summary

### Outputs

Generated in `outputs/` directory:
- `comparison_dashboard.png` - 2×2 comparison chart
- `emissions_reduction.png` - CO₂ reduction vs baseline
- `cost_breakdown.png` - Fuel vs capital costs

---

## Project Structure

```
marine_propulsion_simulator/
├── data/
│   └── vessel_data.db           # SQLite database
├── src/
│   ├── database.py              # Database management
│   ├── propulsion_models.py     # Engine models with real SFOC
│   ├── simulator.py             # Voyage simulation engine
│   └── visualizer.py            # Charts and value propositions
├── outputs/                     # Generated visualizations
├── main.py                      # Full simulation
├── demo.py                      # Quick demo
├── requirements.txt
└── README.md
```

---

## Operational Profile

**Vessel:** Short-Sea Tanker  
**Design Speed:** 14 knots @ 4500 kW  
**Sailing Speed:** 12.5 knots (cubic interpolation → 3200 kW)

| Mode | Hours/Year | Propulsion | Electric Load |
|------|------------|------------|---------------|
| Sailing | 5,694 (65%) | 3200 kW | 700 kW |
| Maneuvering | 438 (5%) | 1000 kW | 1200 kW |
| Port | 2,628 (30%) | 0 kW | 500 kW |

**Total:** 8,760 hours/year

---

## Key Results (Example)

| Configuration | CO₂ (t/year) | Annual Cost | vs Baseline |
|--------------|-------------|-------------|-------------|
| Diesel-Mechanical | 3,850 | $2.50M | Baseline |
| Dual-Fuel LNG | 2,900 | $2.80M | -24.7% CO₂ |
| Hybrid | 3,600 | $2.95M | -6.5% CO₂, Zero-emission port |

*Note: Actual results depend on fuel prices and operational assumptions*

---

## Technical Methodology

### Fuel Consumption

Using SFOC (Specific Fuel Oil Consumption):
```
Fuel (kg) = Power (kW) × Hours (h) × SFOC (g/kWh) / 1000
```

### Sailing Power (Cubic Interpolation)

```
P_sailing = P_design × (V_sailing / V_design)³
P_sailing = 4500 × (12.5 / 14)³ ≈ 3200 kW
```

### Emissions

```
CO₂ (kg) = Fuel (kg) × CO₂_factor
  - MDO: 3.206 kg CO₂/kg fuel
  - LNG: 2.75 kg CO₂/kg fuel (+ methane slip)
```

### Economics

- Capital cost amortized over 20 years @ 5% discount rate
- Fuel prices: MDO $650/t, LNG $400/t
- Total annual cost = Fuel cost + Amortized capital

---

## Engine Data Sources

All SFOC values from:
- Wärtsilä Engine Configurator (https://www.wartsila.com/marine/engine-configurator)
- Official Wärtsilä engine datasheets
- Values at 85% load (typical cruising condition)

---

## Assumptions & Limitations

**Assumptions:**
- SFOC constant at 85% load (simplified)
- Dual-fuel operates 95% on LNG, 5% on MDO
- Hybrid battery covers 3 hours of port operations
- 20-year economic lifespan
- No fuel price escalation

**Limitations:**
- Simplified part-load efficiency curves
- Does not model dynamic transients
- Weather impact not included
- Maintenance costs simplified

---

## Extensions & Improvements

Potential enhancements:
- [ ] Dynamic load-dependent SFOC curves
- [ ] Weather routing and sea state impact
- [ ] Multi-year fuel price scenarios
- [ ] Carbon pricing sensitivity
- [ ] Route optimization
- [ ] Real AIS data integration
- [ ] Monte Carlo uncertainty analysis

---

## License

Created for Marine Systems process, Educational and demonstration purposes.
