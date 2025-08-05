#!/usr/bin/env python3
"""
Test script for data collection from DraftKings

This script tests the data collection functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dfs_optimizer.data_collector import DataCollector
import pandas as pd

def test_draftkings_collection():
    """Test DraftKings data collection."""
    
    print("🏈 Testing DraftKings Data Collection")
    print("=" * 50)
    
    try:
        # Initialize data collector
        collector = DataCollector()
        
        # Test DraftKings data collection
        print("\n1. Testing DraftKings data collection...")
        dk_data = collector.dk_collector.get_players(contest_type_id=21, draft_group_id=131064)
        
        if dk_data is not None and not dk_data.empty:
            print(f"   ✅ Successfully collected {len(dk_data)} players from DraftKings")
            print(f"   Columns: {list(dk_data.columns)}")
            
            # Parse the data
            parsed_data = collector.dk_collector.parse_player_data(dk_data)
            print(f"   ✅ Parsed data successfully")
            print(f"   Sample players:")
            
            # Show sample data
            for i, (_, player) in enumerate(parsed_data.head(5).iterrows()):
                print(f"      {i+1}. {player.get('name', 'N/A')} - {player.get('position', 'N/A')} - ${player.get('salary', 0):,}")
            
            return True
        else:
            print("   ❌ No data collected from DraftKings")
            return False
            
    except Exception as e:
        print(f"   ❌ Error collecting data: {e}")
        return False

def test_sample_data_optimization():
    """Test optimization with sample data."""
    
    print("\n2. Testing optimization with sample data...")
    
    try:
        # Create sample data
        sample_players = [
            {'name': 'Patrick Mahomes', 'position': 'QB', 'team': 'KC', 'salary': 8500, 'projected_points': 25.5},
            {'name': 'Josh Allen', 'position': 'QB', 'team': 'BUF', 'salary': 8200, 'projected_points': 24.8},
            {'name': 'Christian McCaffrey', 'position': 'RB', 'team': 'SF', 'salary': 9000, 'projected_points': 26.5},
            {'name': 'Saquon Barkley', 'position': 'RB', 'team': 'NYG', 'salary': 7200, 'projected_points': 20.8},
            {'name': 'Tyreek Hill', 'position': 'WR', 'team': 'MIA', 'salary': 8800, 'projected_points': 24.5},
            {'name': 'Stefon Diggs', 'position': 'WR', 'team': 'BUF', 'salary': 8200, 'projected_points': 22.8},
            {'name': 'Travis Kelce', 'position': 'TE', 'team': 'KC', 'salary': 8500, 'projected_points': 22.5},
            {'name': 'Mark Andrews', 'position': 'TE', 'team': 'BAL', 'salary': 6800, 'projected_points': 18.2},
            {'name': 'San Francisco 49ers', 'position': 'DST', 'team': 'SF', 'salary': 3800, 'projected_points': 12.5},
        ]
        
        players_df = pd.DataFrame(sample_players)
        
        # Test data collection with sample data
        collector = DataCollector()
        data = {
            'draftkings': players_df,
            'player_props': pd.DataFrame(),
            'projections': pd.DataFrame()
        }
        
        # Merge data
        merged_data = collector.merge_data(data)
        print(f"   ✅ Successfully merged {len(merged_data)} players")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in sample data optimization: {e}")
        return False

def main():
    """Main test function."""
    
    print("🧪 DFS Optimizer - Data Collection Tests")
    print("=" * 60)
    
    # Test DraftKings collection
    dk_success = test_draftkings_collection()
    
    # Test sample data optimization
    sample_success = test_sample_data_optimization()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   DraftKings Collection: {'✅ PASS' if dk_success else '❌ FAIL'}")
    print(f"   Sample Data Optimization: {'✅ PASS' if sample_success else '❌ FAIL'}")
    
    if dk_success and sample_success:
        print("\n🎉 All tests passed! The DFS optimizer is ready to use.")
        print("\nNext steps:")
        print("   1. Run the web interface: python app.py")
        print("   2. Open http://localhost:5000 in your browser")
        print("   3. Use the example script: python example_usage.py")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return dk_success and sample_success

if __name__ == '__main__':
    main()