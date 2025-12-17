import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class SimulationVisualizer:
    """Create visualizations for simulation results"""
    
    def __init__(self, style='darkgrid'):
        sns.set_style(style)
        self.colors = ['#2E86AB', '#A23B72', '#F18F01']  # Blue, Purple, Orange
    
    def plot_comparison(self, results, save_path=None):
        """Create a comprehensive comparison plot"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Marine Propulsion System Comparison', fontsize=16, fontweight='bold')
        
        systems = [r['propulsion_system'] for r in results]
        
        # 1. Fuel Consumption
        fuel_data = [r['total_fuel_consumption'] for r in results]
        axes[0, 0].bar(systems, fuel_data, color=self.colors)
        axes[0, 0].set_title('Total Fuel/Energy Consumption', fontweight='bold')
        axes[0, 0].set_ylabel('Consumption (kg or kWh)')
        axes[0, 0].tick_params(axis='x', rotation=15)
        
        # Add value labels on bars
        for i, v in enumerate(fuel_data):
            axes[0, 0].text(i, v + max(fuel_data)*0.02, f'{v:.0f}', 
                           ha='center', va='bottom', fontweight='bold')
        
        # 2. CO2 Emissions
        emissions_data = [r['total_co2_emissions'] for r in results]
        axes[0, 1].bar(systems, emissions_data, color=self.colors)
        axes[0, 1].set_title('CO₂ Emissions', fontweight='bold')
        axes[0, 1].set_ylabel('Emissions (kg CO₂)')
        axes[0, 1].tick_params(axis='x', rotation=15)
        
        for i, v in enumerate(emissions_data):
            axes[0, 1].text(i, v + max(emissions_data)*0.02, f'{v:.0f}', 
                           ha='center', va='bottom', fontweight='bold')
        
        # 3. Operating Cost
        cost_data = [r['total_voyage_cost'] for r in results]
        axes[1, 0].bar(systems, cost_data, color=self.colors)
        axes[1, 0].set_title('Total Voyage Cost (Fuel + Amortized Capital)', fontweight='bold')
        axes[1, 0].set_ylabel('Cost ($)')
        axes[1, 0].tick_params(axis='x', rotation=15)
        
        for i, v in enumerate(cost_data):
            axes[1, 0].text(i, v + max(cost_data)*0.02, f'${v:.0f}', 
                           ha='center', va='bottom', fontweight='bold')
        
        # 4. Operational Phase Breakdown (stacked bar for first system as example)
        if len(results) > 0:
            breakdown = results[0]['breakdown']
            phases = list(breakdown.keys())
            fuel_by_phase = [breakdown[phase]['fuel'] for phase in phases]
            
            x_pos = np.arange(len(systems))
            width = 0.6
            
            bottom = np.zeros(len(systems))
            
            for i, phase in enumerate(phases):
                phase_data = [r['breakdown'][phase]['fuel'] for r in results]
                axes[1, 1].bar(x_pos, phase_data, width, label=phase.capitalize(),
                             bottom=bottom, color=self.colors[i % len(self.colors)])
                bottom += phase_data
            
            axes[1, 1].set_title('Fuel Consumption by Operational Phase', fontweight='bold')
            axes[1, 1].set_ylabel('Fuel (kg or kWh)')
            axes[1, 1].set_xticks(x_pos)
            axes[1, 1].set_xticklabels(systems, rotation=15)
            axes[1, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_emissions_savings(self, results, baseline_idx=0):
        """Plot emissions savings compared to baseline"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        systems = [r['propulsion_system'] for r in results]
        emissions = [r['total_co2_emissions'] for r in results]
        
        baseline_emissions = emissions[baseline_idx]
        savings = [(baseline_emissions - e) / baseline_emissions * 100 for e in emissions]
        
        colors_mapped = [self.colors[i % len(self.colors)] for i in range(len(systems))]
        bars = ax.bar(systems, savings, color=colors_mapped)
        
        # Color baseline differently
        bars[baseline_idx].set_color('#cccccc')
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.set_title('CO₂ Emissions Reduction vs Baseline', fontsize=14, fontweight='bold')
        ax.set_ylabel('Emissions Reduction (%)', fontsize=12)
        ax.tick_params(axis='x', rotation=15)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, savings)):
            height = bar.get_height()
            label = 'Baseline' if i == baseline_idx else f'{val:.1f}%'
            ax.text(bar.get_x() + bar.get_width()/2., height + (2 if height >= 0 else -5),
                   label, ha='center', va='bottom' if height >= 0 else 'top', 
                   fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def create_value_proposition(self, results, baseline_idx=0, years=10):
        """Generate a value proposition summary"""
        baseline = results[baseline_idx]
        
        print("\n" + "="*70)
        print("VALUE PROPOSITION SUMMARY".center(70))
        print("="*70)
        print(f"\nBaseline System: {baseline['propulsion_system']}")
        print(f"Analysis Period: {years} years | 250 voyages/year\n")
        
        for i, result in enumerate(results):
            if i == baseline_idx:
                continue
            
            print(f"\n{'─'*70}")
            print(f"Alternative: {result['propulsion_system']}")
            print(f"{'─'*70}")
            
            # Calculate per voyage differences
            fuel_saving = baseline['total_fuel_consumption'] - result['total_fuel_consumption']
            fuel_saving_pct = (fuel_saving / baseline['total_fuel_consumption']) * 100
            
            emissions_saving = baseline['total_co2_emissions'] - result['total_co2_emissions']
            emissions_saving_pct = (emissions_saving / baseline['total_co2_emissions']) * 100
            
            cost_diff = result['total_voyage_cost'] - baseline['total_voyage_cost']
            
            # Annual calculations
            annual_voyages = 250
            annual_emissions_saving = emissions_saving * annual_voyages / 1000  # tonnes
            annual_cost_diff = cost_diff * annual_voyages
            
            # Lifetime calculations
            lifetime_emissions_saving = annual_emissions_saving * years
            lifetime_cost_diff = annual_cost_diff * years
            
            print(f"\n📊 Per Voyage Comparison:")
            print(f"   Fuel/Energy Reduction:  {fuel_saving:>10.1f} kg  ({fuel_saving_pct:>6.1f}%)")
            print(f"   CO₂ Reduction:          {emissions_saving:>10.1f} kg  ({emissions_saving_pct:>6.1f}%)")
            print(f"   Cost Difference:        ${cost_diff:>10.2f}")
            
            print(f"\n📅 Annual Impact (250 voyages):")
            print(f"   CO₂ Avoided:            {annual_emissions_saving:>10.1f} tonnes")
            print(f"   Cost Impact:            ${annual_cost_diff:>10,.0f}")
            
            print(f"\n🌍 {years}-Year Lifecycle Impact:")
            print(f"   Total CO₂ Avoided:      {lifetime_emissions_saving:>10,.0f} tonnes")
            print(f"   Total Cost Impact:      ${lifetime_cost_diff:>10,.0f}")
            
            # Equivalent context
            print(f"\n💡 Context:")
            print(f"   CO₂ savings equivalent to removing {lifetime_emissions_saving/4.6:.0f} cars")
            print(f"   from the road for one year")
            
            # ROI calculation
            if cost_diff < 0:
                payback_years = "Immediate savings"
            else:
                if annual_cost_diff > 0:
                    payback_years = f"Never (higher operating cost)"
                else:
                    payback_years = "N/A"
            
            print(f"   Payback Period:         {payback_years}")
        
        print("\n" + "="*70 + "\n")
    
    def plot_sensitivity_analysis(self, base_results, parameter_name='fuel_price'):
        """Simple sensitivity analysis visualization"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # This is a placeholder for more advanced sensitivity analysis
        # You could vary fuel prices, operating hours, etc.
        
        systems = [r['propulsion_system'] for r in base_results]
        base_costs = [r['total_voyage_cost'] for r in base_results]
        
        # Simulate +/- 20% fuel price variation
        variations = [-0.2, -0.1, 0, 0.1, 0.2]
        
        for i, system in enumerate(systems):
            base_cost = base_costs[i]
            varied_costs = [base_cost * (1 + v * 0.5) for v in variations]  # Simplified
            ax.plot([v*100 for v in variations], varied_costs, 
                   marker='o', label=system, linewidth=2)
        
        ax.set_xlabel('Fuel Price Variation (%)', fontsize=12)
        ax.set_ylabel('Total Voyage Cost ($)', fontsize=12)
        ax.set_title('Sensitivity to Fuel Price Changes', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        return fig