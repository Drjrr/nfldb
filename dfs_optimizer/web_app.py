"""
Web application for DFS Optimizer.

Provides a modern web interface for lineup optimization.
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import logging
from datetime import datetime
import os
from typing import Dict, List

from .data_collector import DataCollector
from .optimizer import DFSOptimizer, AdvancedOptimizer, LineupValidator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
data_collector = DataCollector()
optimizer = AdvancedOptimizer()
current_data = None


@app.route('/')
def index():
    """Main page with optimization interface."""
    return render_template('index.html')


@app.route('/api/collect-data', methods=['POST'])
def collect_data():
    """API endpoint to collect player data."""
    try:
        data = request.get_json()
        week = data.get('week', 1)
        season = data.get('season', 2024)
        contest_type_id = data.get('contest_type_id', 21)
        draft_group_id = data.get('draft_group_id', 131064)
        
        logger.info(f"Collecting data for Week {week}, Season {season}")
        
        # Collect data
        global current_data
        current_data = data_collector.collect_all_data(
            week=week,
            season=season,
            contest_type_id=contest_type_id,
            draft_group_id=draft_group_id
        )
        
        # Merge data for optimization
        merged_data = data_collector.merge_data(current_data)
        
        # Set players in optimizer
        optimizer.set_players(merged_data)
        
        # Set default constraints
        constraints = {
            'salary_cap': 50000,
            'total_players': 9,
            'max_team_players': 4
        }
        optimizer.set_constraints(constraints)
        
        return jsonify({
            'success': True,
            'message': f'Data collected successfully for Week {week}',
            'player_count': len(merged_data),
            'data_preview': merged_data.head(10).to_dict('records')
        })
        
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize', methods=['POST'])
def optimize_lineups():
    """API endpoint to optimize lineups."""
    try:
        data = request.get_json()
        num_lineups = data.get('num_lineups', 1)
        max_exposure = data.get('max_exposure', 1.0)
        optimization_type = data.get('optimization_type', 'standard')
        
        if current_data is None:
            return jsonify({
                'success': False,
                'error': 'No data available. Please collect data first.'
            }), 400
        
        logger.info(f"Optimizing {num_lineups} lineups with {optimization_type} optimization")
        
        # Optimize lineups
        if optimization_type == 'leverage':
            leverage_weight = data.get('leverage_weight', 0.3)
            lineups = optimizer.optimize_with_leverage(num_lineups, leverage_weight)
        elif optimization_type == 'correlation':
            correlation_threshold = data.get('correlation_threshold', 0.7)
            lineups = optimizer.optimize_with_correlation(num_lineups, correlation_threshold)
        else:
            lineups = optimizer.optimize_lineup(num_lineups, max_exposure)
        
        # Validate lineups
        validated_lineups = []
        for i, lineup in enumerate(lineups):
            is_valid, errors = LineupValidator.validate_draftkings_nfl(lineup)
            lineup['lineup_id'] = i + 1
            lineup['is_valid'] = is_valid
            lineup['validation_errors'] = errors
            validated_lineups.append(lineup)
        
        return jsonify({
            'success': True,
            'lineups': validated_lineups,
            'total_lineups': len(validated_lineups)
        })
        
    except Exception as e:
        logger.error(f"Error optimizing lineups: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/players')
def get_players():
    """API endpoint to get current player data."""
    if current_data is None or 'draftkings' not in current_data:
        return jsonify({
            'success': False,
            'error': 'No player data available'
        }), 400
    
    players_df = current_data['draftkings']
    
    # Apply filters if provided
    position_filter = request.args.get('position')
    team_filter = request.args.get('team')
    min_salary = request.args.get('min_salary', type=int)
    max_salary = request.args.get('max_salary', type=int)
    
    filtered_df = players_df.copy()
    
    if position_filter:
        filtered_df = filtered_df[filtered_df['position'] == position_filter]
    
    if team_filter:
        filtered_df = filtered_df[filtered_df['team'] == team_filter]
    
    if min_salary:
        filtered_df = filtered_df[filtered_df['salary'] >= min_salary]
    
    if max_salary:
        filtered_df = filtered_df[filtered_df['salary'] <= max_salary]
    
    return jsonify({
        'success': True,
        'players': filtered_df.to_dict('records'),
        'total_players': len(filtered_df)
    })


@app.route('/api/export-lineup/<int:lineup_id>')
def export_lineup(lineup_id):
    """Export lineup to CSV format."""
    try:
        # This would retrieve the specific lineup
        # For now, return a placeholder
        return jsonify({
            'success': False,
            'error': 'Export functionality not implemented yet'
        }), 501
        
    except Exception as e:
        logger.error(f"Error exporting lineup: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """Get optimization statistics."""
    if current_data is None:
        return jsonify({
            'success': False,
            'error': 'No data available'
        }), 400
    
    players_df = current_data['draftkings']
    
    stats = {
        'total_players': len(players_df),
        'positions': players_df['position'].value_counts().to_dict(),
        'teams': players_df['team'].value_counts().to_dict(),
        'salary_range': {
            'min': int(players_df['salary'].min()),
            'max': int(players_df['salary'].max()),
            'avg': int(players_df['salary'].mean())
        },
        'projected_points_range': {
            'min': float(players_df['projected_points'].min()),
            'max': float(players_df['projected_points'].max()),
            'avg': float(players_df['projected_points'].mean())
        }
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


def create_app():
    """Application factory."""
    return app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)