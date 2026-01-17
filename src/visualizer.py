import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class SimulationVisualizer:
    """Create professional visualizations for propulsion system comparison"""
    
    def __init__(self, style='whitegrid'):
        sns.set_style(style)
        sns.set_context("talk")  # Larger fonts for presentation
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
        
    def plot_comparison_dashboard(self, results, save_path=None):
        """Create comprehensive 2x2 comparison dashboard"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Propulsion System Comparison - Short-Sea Tanker', 
                     fontsize=18, fontweight='bold', y=0.995)
        
        configs = [r['configuration'] for r in results]
        
        # 1. Annual Fuel Consumption
        fuel_data = [r['total_fuel_tonnes'] for r in results]
        bars1 = axes[0, 0].bar(configs, fuel_data, color=self.colors, edgecolor='black', linewidth=1.5)
        axes[0, 0].set_title('Annual Fuel/Energy Consumption', fontweight='bold', fontsize=14)
        axes[0, 0].set_ylabel('Fuel Consumption (tonnes/year)', fontsize=12)
        axes[0, 0].tick_params(axis='x', rotation=15)
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars1, fuel_data):
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{val:.0f}t', ha='center', va='bottom', 
                           fontweight='bold', fontsize=11)
        
        # 2. Annual CO₂ Emissions
        co2_data = [r['total_co2_tonnes'] for r in results]
        bars2 = axes[0, 1].bar(configs, co2_data, color=self.colors, edgecolor='black', linewidth=1.5)
        axes[0, 1].set_title('Annual CO₂ Emissions', fontweight='bold', fontsize=14)
        axes[0, 1].set_ylabel('CO₂ Emissions (tonnes/year)', fontsize=12)
        axes[0, 1].tick_params(axis='x', rotation=15)
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars2, co2_data):
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{val:.0f}t', ha='center', va='bottom', 
                           fontweight='bold', fontsize=11)
        
        # 3. Total Annual Cost
        cost_data = [r['total_annual_cost_usd'] / 1e6 for r in results]  # In millions
        bars3 = axes[1, 0].bar(configs, cost_data, color=self.colors, edgecolor='black', linewidth=1.5)
        axes[1, 0].set_title('Total Annual Operating Cost', fontweight='bold', fontsize=14)
        axes[1, 0].set_ylabel('Annual Cost (Million USD)', fontsize=12)
        axes[1, 0].tick_params(axis='x', rotation=15)
        axes[1, 0].grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars3, cost_data):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'${val:.2f}M', ha='center', va='bottom', 
                           fontweight='bold', fontsize=11)
        
        # 4. Fuel Breakdown by Operational Mode (stacked bar)
        sailing_fuel = [r['breakdown']['sailing']['fuel_kg']/1000 for r in results]
        maneuvering_fuel = [r['breakdown']['maneuvering']['fuel_kg']/1000 for r in results]
        port_fuel = [r['breakdown']['port']['fuel_kg']/1000 for r in results]
        
        x = np.arange(len(configs))
        width = 0.6
        
        p1 = axes[1, 1].bar(x, sailing_fuel, width, label='Sailing (65%)', 
                           color='#4CAF50', edgecolor='black', linewidth=1.5)
        p2 = axes[1, 1].bar(x, maneuvering_fuel, width, bottom=sailing_fuel,
                           label='Maneuvering (5%)', color='#FFC107', 
                           edgecolor='black', linewidth=1.5)
        p3 = axes[1, 1].bar(x, port_fuel, width, 
                           bottom=[s+m for s,m in zip(sailing_fuel, maneuvering_fuel)],
                           label='Port (30%)', color='#F44336', 
                           edgecolor='black', linewidth=1.5)
        
        axes[1, 1].set_title('Fuel Consumption by Operational Mode', fontweight='bold', fontsize=14)
        axes[1, 1].set_ylabel('Fuel Consumption (tonnes)', fontsize=12)
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(configs, rotation=15)
        axes[1, 1].legend(loc='upper right', fontsize=10)
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        
        return fig
    
    def plot_emissions_reduction(self, results, baseline_idx=0, save_path=None):
        """Plot CO₂ emissions reduction vs baseline"""
        fig, ax = plt.subplots(figsize=(10, 7))
        
        configs = [r['configuration'] for r in results]
        co2_reductions = [r['vs_baseline']['co2_reduction_pct'] for r in results]
        
        bars = ax.bar(configs, co2_reductions, color=self.colors, 
                     edgecolor='black', linewidth=2)
        
        # Color baseline differently
        bars[baseline_idx].set_color('#cccccc')
        bars[baseline_idx].set_edgecolor('black')
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
        ax.set_title('CO₂ Emissions Reduction vs Baseline\n(Conventional Diesel-Mechanical)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('CO₂ Reduction (%)', fontsize=13)
        ax.tick_params(axis='x', rotation=15)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, co2_reductions)):
            height = bar.get_height()
            if i == baseline_idx:
                label = 'Baseline'
            else:
                label = f'{val:.1f}%'
            
            y_pos = height + (3 if height >= 0 else -6)
            ax.text(bar.get_x() + bar.get_width()/2., y_pos, label,
                   ha='center', va='bottom' if height >= 0 else 'top', 
                   fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        
        return fig
    
    def plot_cost_breakdown(self, results, save_path=None):
        """Plot cost breakdown: fuel vs capital"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        configs = [r['configuration'] for r in results]
        fuel_costs = [r['fuel_cost_usd'] / 1e6 for r in results]
        capital_costs = [r['capital_cost_annual_usd'] / 1e6 for r in results]
        
        x = np.arange(len(configs))
        width = 0.6
        
        p1 = ax.bar(x, fuel_costs, width, label='Fuel Cost', 
                   color='#FF6B6B', edgecolor='black', linewidth=1.5)
        p2 = ax.bar(x, capital_costs, width, bottom=fuel_costs,
                   label='Amortized Capital Cost', color='#4ECDC4', 
                   edgecolor='black', linewidth=1.5)
        
        ax.set_title('Annual Cost Breakdown', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Annual Cost (Million USD)', fontsize=13)
        ax.set_xticks(x)
        ax.set_xticklabels(configs, rotation=15)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        # Add total labels on top
        for i, (fc, cc) in enumerate(zip(fuel_costs, capital_costs)):
            total = fc + cc
            ax.text(i, total + 0.05, f'${total:.2f}M', 
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        
        return fig
    
    def create_value_proposition_summary(self, results, baseline_idx=0):
        """Generate text-based value proposition summary"""
        baseline = results[baseline_idx]
        
        print("\n" + "="*80)
        print("VALUE PROPOSITION SUMMARY".center(80))
        print("="*80)
        print(f"\nVessel Type: Short-Sea Tanker")
        print(f"Annual Operating Hours: 8,760 hours")
        print(f"Baseline: {baseline['configuration']}")
        print(f"  - Annual Fuel: {baseline['total_fuel_tonnes']:,.0f} tonnes")
        print(f"  - Annual CO₂: {baseline['total_co2_tonnes']:,.0f} tonnes")
        print(f"  - Annual Cost: ${baseline['total_annual_cost_usd']:,.0f}")
        
        for i, result in enumerate(results):
            if i == baseline_idx:
                continue
            
            print(f"\n{'─'*80}")
            print(f"Configuration: {result['configuration']}")
            print(f"{'─'*80}")
            
            # Calculate differences
            fuel_saving_tonnes = baseline['total_fuel_tonnes'] - result['total_fuel_tonnes']
            fuel_saving_pct = result['vs_baseline']['fuel_reduction_pct']
            
            co2_saving_tonnes = baseline['total_co2_tonnes'] - result['total_co2_tonnes']
            co2_saving_pct = result['vs_baseline']['co2_reduction_pct']
            
            cost_diff = result['total_annual_cost_usd'] - baseline['total_annual_cost_usd']
            cost_diff_pct = result['vs_baseline']['cost_difference_pct']
            
            print(f"\n📊 Annual Performance:")
            print(f"   Fuel Consumption:     {result['total_fuel_tonnes']:>8,.0f} tonnes  ({fuel_saving_pct:>+6.1f}%)")
            print(f"   CO₂ Emissions:        {result['total_co2_tonnes']:>8,.0f} tonnes  ({co2_saving_pct:>+6.1f}%)")
            print(f"   Total Annual Cost:    ${result['total_annual_cost_usd']:>8,.0f}  ({cost_diff_pct:>+6.1f}%)")
            
            print(f"\n💰 Economic Impact:")
            print(f"   Additional Capital Cost:  ${cost_diff:>10,.0f} per year")
            print(f"   Fuel Cost Savings:        ${baseline['fuel_cost_usd'] - result['fuel_cost_usd']:>10,.0f} per year")
            
            print(f"\n🌍 Environmental Impact (20-year lifecycle):")
            print(f"   Total CO₂ Avoided:        {co2_saving_tonnes * 20:>10,.0f} tonnes")
            print(f"   Equivalent to removing    {co2_saving_tonnes * 20 / 4.6:>10,.0f} cars from road for 1 year")
            
            # ROI analysis
            capital_diff = result['capital_cost_annual_usd'] - baseline['capital_cost_annual_usd']
            fuel_savings = baseline['fuel_cost_usd'] - result['fuel_cost_usd']
            net_annual_impact = fuel_savings - capital_diff
            
            if net_annual_impact > 0:
                print(f"\n✅ Net Annual Savings:     ${net_annual_impact:>10,.0f}")
            else:
                print(f"\n⚠️  Net Annual Cost:       ${abs(net_annual_impact):>10,.0f}")
        
        print("\n" + "="*80 + "\n")
    
    def export_summary_table(self, results):
        """Create summary table for presentation"""
        print("\n" + "="*100)
        print("SUMMARY COMPARISON TABLE")
        print("="*100)
        print(f"{'Configuration':<30} {'Fuel (t/y)':<12} {'CO₂ (t/y)':<12} {'Cost ($/y)':<15} {'vs Baseline':<20}")
        print("-"*100)
        
        for i, r in enumerate(results):
            baseline_str = "BASELINE" if r['vs_baseline']['is_baseline'] else f"CO₂: {r['vs_baseline']['co2_reduction_pct']:+.1f}%"
            
            print(f"{r['configuration']:<30} "
                  f"{r['total_fuel_tonnes']:<12,.0f} "
                  f"{r['total_co2_tonnes']:<12,.0f} "
                  f"${r['total_annual_cost_usd']:<14,.0f} "
                  f"{baseline_str:<20}")
        
        print("="*100 + "\n")


if __name__ == "__main__":
    # Test visualization with mock data
    print("Testing visualization module...")
    
    # Mock results for testing
    mock_results = [
        {
            'configuration': 'Diesel-Mechanical',
            'total_fuel_tonnes': 1200,
            'total_co2_tonnes': 3850,
            'total_annual_cost_usd': 2500000,
            'fuel_cost_usd': 780000,
            'capital_cost_annual_usd': 1720000,
            'breakdown': {
                'sailing': {'fuel_kg': 900000},
                'maneuvering': {'fuel_kg': 200000},
                'port': {'fuel_kg': 100000}
            },
            'vs_baseline': {'co2_reduction_pct': 0, 'is_baseline': True}
        },
        {
            'configuration': 'Dual-Fuel LNG',
            'total_fuel_tonnes': 1050,
            'total_co2_tonnes': 2900,
            'total_annual_cost_usd': 2800000,
            'fuel_cost_usd': 420000,
            'capital_cost_annual_usd': 2380000,
            'breakdown': {
                'sailing': {'fuel_kg': 800000},
                'maneuvering': {'fuel_kg': 180000},
                'port': {'fuel_kg': 70000}
            },
            'vs_baseline': {'co2_reduction_pct': 24.7, 'is_baseline': False}
        }
    ]
    
    viz = SimulationVisualizer()
    viz.export_summary_table(mock_results)
    print("✓ Visualization module ready")