"""
DFS Optimization Engine

Uses linear programming to find optimal lineups based on projections and constraints.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from pulp import *
import logging

logger = logging.getLogger(__name__)


class DFSOptimizer:
    """Main DFS optimization engine using linear programming."""
    
    def __init__(self):
        self.players_df = None
        self.constraints = {}
        self.lineup_rules = {}
        
    def set_players(self, players_df: pd.DataFrame):
        """Set the players DataFrame for optimization."""
        self.players_df = players_df.copy()
        logger.info(f"Set {len(players_df)} players for optimization")
    
    def set_constraints(self, constraints: Dict):
        """Set optimization constraints."""
        self.constraints = constraints
        logger.info(f"Set constraints: {constraints}")
    
    def set_lineup_rules(self, rules: Dict):
        """Set lineup construction rules."""
        self.lineup_rules = rules
        logger.info(f"Set lineup rules: {rules}")
    
    def optimize_lineup(self, num_lineups: int = 1, max_exposure: float = 1.0) -> List[Dict]:
        """
        Optimize lineups using linear programming.
        
        Args:
            num_lineups: Number of lineups to generate
            max_exposure: Maximum exposure per player (0.0 to 1.0)
            
        Returns:
            List of optimized lineups
        """
        if self.players_df is None or self.players_df.empty:
            raise ValueError("No players data available for optimization")
        
        lineups = []
        
        for i in range(num_lineups):
            logger.info(f"Generating lineup {i+1}/{num_lineups}")
            
            # Create optimization problem
            prob = LpProblem(f"DFS_Lineup_{i+1}", LpMaximize)
            
            # Create binary variables for each player
            player_vars = LpVariable.dicts("Player",
                                         self.players_df.index,
                                         cat='Binary')
            
            # Objective function: maximize projected points
            prob += lpSum([player_vars[i] * self.players_df.iloc[i]['projected_points'] 
                          for i in self.players_df.index])
            
            # Add constraints
            self._add_constraints(prob, player_vars, i, max_exposure)
            
            # Solve the problem
            prob.solve(PULP_CBC_CMD(msg=False))
            
            if prob.status == LpStatusOptimal:
                lineup = self._extract_lineup(prob, player_vars)
                lineups.append(lineup)
                logger.info(f"Lineup {i+1} optimized successfully")
            else:
                logger.warning(f"Could not optimize lineup {i+1}")
        
        return lineups
    
    def _add_constraints(self, prob: LpProblem, player_vars: Dict, lineup_num: int, max_exposure: float):
        """Add all optimization constraints."""
        
        # Salary cap constraint
        salary_cap = self.constraints.get('salary_cap', 50000)
        prob += lpSum([player_vars[i] * self.players_df.iloc[i]['salary'] 
                      for i in self.players_df.index]) <= salary_cap
        
        # Position constraints
        self._add_position_constraints(prob, player_vars)
        
        # Team stacking constraints
        self._add_team_constraints(prob, player_vars)
        
        # Exposure constraints for multiple lineups
        if lineup_num > 0 and max_exposure < 1.0:
            self._add_exposure_constraints(prob, player_vars, lineup_num, max_exposure)
    
    def _add_position_constraints(self, prob: LpProblem, player_vars: Dict):
        """Add position-specific constraints."""
        
        # Default DraftKings NFL rules
        position_limits = {
            'QB': (1, 1),
            'RB': (2, 3),
            'WR': (3, 4),
            'TE': (1, 2),
            'FLEX': (0, 1),
            'DST': (1, 1)
        }
        
        for pos, (min_players, max_players) in position_limits.items():
            pos_players = self.players_df[self.players_df['position'] == pos].index
            
            if len(pos_players) > 0:
                # Minimum players constraint
                if min_players > 0:
                    prob += lpSum([player_vars[i] for i in pos_players]) >= min_players
                
                # Maximum players constraint
                prob += lpSum([player_vars[i] for i in pos_players]) <= max_players
        
        # Total players constraint (9 for DraftKings NFL)
        total_players = self.constraints.get('total_players', 9)
        prob += lpSum([player_vars[i] for i in self.players_df.index]) == total_players
    
    def _add_team_constraints(self, prob: LpProblem, player_vars: Dict):
        """Add team stacking constraints."""
        
        # Maximum players per team
        max_team_players = self.constraints.get('max_team_players', 4)
        
        for team in self.players_df['team'].unique():
            if pd.notna(team):
                team_players = self.players_df[self.players_df['team'] == team].index
                if len(team_players) > 0:
                    prob += lpSum([player_vars[i] for i in team_players]) <= max_team_players
    
    def _add_exposure_constraints(self, prob: LpProblem, player_vars: Dict, lineup_num: int, max_exposure: float):
        """Add exposure constraints for multiple lineups."""
        
        # This would track previous lineups and limit exposure
        # For now, just a placeholder
        pass
    
    def _extract_lineup(self, prob: LpProblem, player_vars: Dict) -> Dict:
        """Extract the optimized lineup from the solved problem."""
        
        selected_players = []
        total_salary = 0
        total_projected_points = 0
        
        for i in self.players_df.index:
            if player_vars[i].value() == 1:
                player = self.players_df.iloc[i]
                selected_players.append({
                    'name': player['name'],
                    'position': player['position'],
                    'team': player['team'],
                    'salary': player['salary'],
                    'projected_points': player['projected_points']
                })
                total_salary += player['salary']
                total_projected_points += player['projected_points']
        
        return {
            'players': selected_players,
            'total_salary': total_salary,
            'total_projected_points': total_projected_points,
            'salary_remaining': self.constraints.get('salary_cap', 50000) - total_salary
        }


class AdvancedOptimizer(DFSOptimizer):
    """Advanced optimizer with additional features."""
    
    def __init__(self):
        super().__init__()
        self.correlation_matrix = None
        self.ownership_projections = None
    
    def set_correlation_matrix(self, correlation_matrix: pd.DataFrame):
        """Set player correlation matrix for advanced optimization."""
        self.correlation_matrix = correlation_matrix
    
    def set_ownership_projections(self, ownership_df: pd.DataFrame):
        """Set ownership projections for leverage optimization."""
        self.ownership_projections = ownership_df
    
    def optimize_with_leverage(self, num_lineups: int = 1, leverage_weight: float = 0.3) -> List[Dict]:
        """
        Optimize lineups considering ownership leverage.
        
        Args:
            num_lineups: Number of lineups to generate
            leverage_weight: Weight for ownership leverage in optimization
            
        Returns:
            List of optimized lineups
        """
        if self.ownership_projections is None:
            logger.warning("No ownership projections available, using standard optimization")
            return self.optimize_lineup(num_lineups)
        
        # Merge ownership data
        merged_df = self.players_df.merge(
            self.ownership_projections[['player_name', 'ownership']], 
            left_on='name', 
            right_on='player_name',
            how='left'
        )
        merged_df['ownership'] = merged_df['ownership'].fillna(0.05)  # Default 5%
        
        # Calculate leverage score
        merged_df['leverage_score'] = merged_df['projected_points'] * (1 - merged_df['ownership'] * leverage_weight)
        
        # Use leverage score for optimization
        self.players_df = merged_df
        return self.optimize_lineup(num_lineups)
    
    def optimize_with_correlation(self, num_lineups: int = 1, correlation_threshold: float = 0.7) -> List[Dict]:
        """
        Optimize lineups considering player correlations.
        
        Args:
            num_lineups: Number of lineups to generate
            correlation_threshold: Threshold for positive correlation penalty
            
        Returns:
            List of optimized lineups
        """
        if self.correlation_matrix is None:
            logger.warning("No correlation matrix available, using standard optimization")
            return self.optimize_lineup(num_lineups)
        
        # This would implement correlation-based optimization
        # For now, return standard optimization
        return self.optimize_lineup(num_lineups)


class LineupValidator:
    """Validates lineups against site rules."""
    
    @staticmethod
    def validate_draftkings_nfl(lineup: Dict) -> Tuple[bool, List[str]]:
        """
        Validate lineup against DraftKings NFL rules.
        
        Args:
            lineup: Lineup dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        players = lineup['players']
        
        # Check total players
        if len(players) != 9:
            errors.append(f"Lineup must have exactly 9 players, got {len(players)}")
        
        # Check salary cap
        if lineup['total_salary'] > 50000:
            errors.append(f"Salary cap exceeded: ${lineup['total_salary']} > $50,000")
        
        # Check position requirements
        positions = [p['position'] for p in players]
        position_counts = pd.Series(positions).value_counts()
        
        # QB: exactly 1
        if position_counts.get('QB', 0) != 1:
            errors.append("Lineup must have exactly 1 QB")
        
        # RB: 2-3
        rb_count = position_counts.get('RB', 0)
        if rb_count < 2 or rb_count > 3:
            errors.append(f"Lineup must have 2-3 RBs, got {rb_count}")
        
        # WR: 3-4
        wr_count = position_counts.get('WR', 0)
        if wr_count < 3 or wr_count > 4:
            errors.append(f"Lineup must have 3-4 WRs, got {wr_count}")
        
        # TE: 1-2
        te_count = position_counts.get('TE', 0)
        if te_count < 1 or te_count > 2:
            errors.append(f"Lineup must have 1-2 TEs, got {te_count}")
        
        # DST: exactly 1
        if position_counts.get('DST', 0) != 1:
            errors.append("Lineup must have exactly 1 DST")
        
        # Check team stacking
        teams = [p['team'] for p in players if pd.notna(p['team'])]
        team_counts = pd.Series(teams).value_counts()
        if team_counts.max() > 4:
            errors.append("Maximum 4 players per team allowed")
        
        return len(errors) == 0, errors