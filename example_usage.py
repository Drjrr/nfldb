#!/usr/bin/env python3
"""
Example usage of the NFL DFS Optimizer

This script demonstrates how to use the optimizer programmatically
without the web interface.
"""

import pandas as pd
import numpy as np
from dfs_optimizer.data_collector import DataCollector
from dfs_optimizer.optimizer import AdvancedOptimizer, LineupValidator

def create_sample_data():
    """Create sample player data for demonstration."""
    
    # Sample player data that mimics DraftKings format
    sample_players = [
        # QBs
        {'name': 'Patrick Mahomes', 'position': 'QB', 'team': 'KC', 'salary': 8500, 'projected_points': 25.5},
        {'name': 'Josh Allen', 'position': 'QB', 'team': 'BUF', 'salary': 8200, 'projected_points': 24.8},
        {'name': 'Jalen Hurts', 'position': 'QB', 'team': 'PHI', 'salary': 8000, 'projected_points': 24.2},
        {'name': 'Lamar Jackson', 'position': 'QB', 'team': 'BAL', 'salary': 7800, 'projected_points': 23.5},
        {'name': 'Justin Herbert', 'position': 'QB', 'team': 'LAC', 'salary': 7600, 'projected_points': 22.8},
        
        # RBs
        {'name': 'Christian McCaffrey', 'position': 'RB', 'team': 'SF', 'salary': 9000, 'projected_points': 26.5},
        {'name': 'Saquon Barkley', 'position': 'RB', 'team': 'NYG', 'salary': 7200, 'projected_points': 20.8},
        {'name': 'Derrick Henry', 'position': 'RB', 'team': 'TEN', 'salary': 7000, 'projected_points': 19.5},
        {'name': 'Nick Chubb', 'position': 'RB', 'team': 'CLE', 'salary': 6800, 'projected_points': 18.9},
        {'name': 'Alvin Kamara', 'position': 'RB', 'team': 'NO', 'salary': 6500, 'projected_points': 17.8},
        {'name': 'Joe Mixon', 'position': 'RB', 'team': 'CIN', 'salary': 6200, 'projected_points': 16.5},
        {'name': 'Rhamondre Stevenson', 'position': 'RB', 'team': 'NE', 'salary': 5800, 'projected_points': 15.2},
        
        # WRs
        {'name': 'Tyreek Hill', 'position': 'WR', 'team': 'MIA', 'salary': 8800, 'projected_points': 24.5},
        {'name': 'Stefon Diggs', 'position': 'WR', 'team': 'BUF', 'salary': 8200, 'projected_points': 22.8},
        {'name': 'Davante Adams', 'position': 'WR', 'team': 'LV', 'salary': 8000, 'projected_points': 21.5},
        {'name': 'A.J. Brown', 'position': 'WR', 'team': 'PHI', 'salary': 7800, 'projected_points': 20.8},
        {'name': 'CeeDee Lamb', 'position': 'WR', 'team': 'DAL', 'salary': 7600, 'projected_points': 19.9},
        {'name': 'Ja\'Marr Chase', 'position': 'WR', 'team': 'CIN', 'salary': 7400, 'projected_points': 19.2},
        {'name': 'DeVonta Smith', 'position': 'WR', 'team': 'PHI', 'salary': 6800, 'projected_points': 17.5},
        {'name': 'Tee Higgins', 'position': 'WR', 'team': 'CIN', 'salary': 6400, 'projected_points': 16.8},
        {'name': 'Brandon Aiyuk', 'position': 'WR', 'team': 'SF', 'salary': 6000, 'projected_points': 15.2},
        {'name': 'Chris Olave', 'position': 'WR', 'team': 'NO', 'salary': 5800, 'projected_points': 14.5},
        {'name': 'Drake London', 'position': 'WR', 'team': 'ATL', 'salary': 5400, 'projected_points': 13.8},
        
        # TEs
        {'name': 'Travis Kelce', 'position': 'TE', 'team': 'KC', 'salary': 8500, 'projected_points': 22.5},
        {'name': 'Mark Andrews', 'position': 'TE', 'team': 'BAL', 'salary': 6800, 'projected_points': 18.2},
        {'name': 'George Kittle', 'position': 'TE', 'team': 'SF', 'salary': 6200, 'projected_points': 16.5},
        {'name': 'Dallas Goedert', 'position': 'TE', 'team': 'PHI', 'salary': 5400, 'projected_points': 14.2},
        {'name': 'T.J. Hockenson', 'position': 'TE', 'team': 'MIN', 'salary': 5200, 'projected_points': 13.8},
        {'name': 'Kyle Pitts', 'position': 'TE', 'team': 'ATL', 'salary': 4800, 'projected_points': 12.5},
        
        # DSTs
        {'name': 'San Francisco 49ers', 'position': 'DST', 'team': 'SF', 'salary': 3800, 'projected_points': 12.5},
        {'name': 'Buffalo Bills', 'position': 'DST', 'team': 'BUF', 'salary': 3600, 'projected_points': 11.8},
        {'name': 'Dallas Cowboys', 'position': 'DST', 'team': 'DAL', 'salary': 3400, 'projected_points': 11.2},
        {'name': 'Philadelphia Eagles', 'position': 'DST', 'team': 'PHI', 'salary': 3200, 'projected_points': 10.5},
        {'name': 'Baltimore Ravens', 'position': 'DST', 'team': 'BAL', 'salary': 3000, 'projected_points': 9.8},
        {'name': 'New England Patriots', 'position': 'DST', 'team': 'NE', 'salary': 2800, 'projected_points': 9.2},
    ]
    
    return pd.DataFrame(sample_players)

def main():
    """Main example function."""
    
    print("🏈 NFL DFS Optimizer - Example Usage")
    print("=" * 50)
    
    # Create sample data
    print("\n1. Creating sample player data...")
    players_df = create_sample_data()
    print(f"   Created {len(players_df)} sample players")
    
    # Initialize optimizer
    print("\n2. Initializing optimizer...")
    optimizer = AdvancedOptimizer()
    optimizer.set_players(players_df)
    
    # Set constraints
    constraints = {
        'salary_cap': 50000,
        'total_players': 9,
        'max_team_players': 4
    }
    optimizer.set_constraints(constraints)
    print(f"   Set constraints: {constraints}")
    
    # Generate single lineup
    print("\n3. Generating single optimal lineup...")
    lineups = optimizer.optimize_lineup(num_lineups=1)
    
    if lineups:
        lineup = lineups[0]
        print(f"   Generated lineup with {lineup['total_projected_points']:.1f} projected points")
        print(f"   Total salary: ${lineup['total_salary']:,}")
        print(f"   Salary remaining: ${lineup['salary_remaining']:,}")
        
        # Validate lineup
        is_valid, errors = LineupValidator.validate_draftkings_nfl(lineup)
        print(f"   Lineup valid: {is_valid}")
        if errors:
            print(f"   Validation errors: {errors}")
        
        # Display lineup
        print("\n   Selected Players:")
        print("   " + "-" * 80)
        for player in lineup['players']:
            print(f"   {player['position']:2} | {player['name']:25} | {player['team']:3} | "
                  f"${player['salary']:6,} | {player['projected_points']:5.1f} pts")
    
    # Generate multiple lineups
    print("\n4. Generating multiple lineups...")
    multiple_lineups = optimizer.optimize_lineup(num_lineups=3, max_exposure=0.7)
    
    print(f"   Generated {len(multiple_lineups)} lineups")
    for i, lineup in enumerate(multiple_lineups, 1):
        print(f"   Lineup {i}: {lineup['total_projected_points']:.1f} pts, "
              f"${lineup['total_salary']:,} salary")
    
    # Demonstrate leverage optimization
    print("\n5. Demonstrating leverage optimization...")
    
    # Create sample ownership data
    ownership_data = {
        'player_name': ['Patrick Mahomes', 'Josh Allen', 'Christian McCaffrey', 'Tyreek Hill'],
        'ownership': [0.25, 0.20, 0.30, 0.28]
    }
    ownership_df = pd.DataFrame(ownership_data)
    
    optimizer.set_ownership_projections(ownership_df)
    leverage_lineups = optimizer.optimize_with_leverage(num_lineups=1, leverage_weight=0.3)
    
    if leverage_lineups:
        print(f"   Generated leverage lineup with {leverage_lineups[0]['total_projected_points']:.1f} points")
    
    print("\n✅ Example completed successfully!")
    print("\nTo run the web interface, execute: python app.py")

if __name__ == '__main__':
    main()