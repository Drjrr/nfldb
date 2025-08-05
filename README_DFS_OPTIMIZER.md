# NFL DFS Optimizer

A comprehensive Daily Fantasy Sports optimizer for NFL contests, built with Python and featuring advanced optimization algorithms, data collection from multiple sources, and a modern web interface.

## Features

### 🎯 Core Optimization
- **Linear Programming Optimization**: Uses PuLP library for optimal lineup generation
- **Multiple Optimization Types**: Standard, leverage-based, and correlation-based optimization
- **DraftKings NFL Rules**: Full compliance with DraftKings NFL contest rules
- **Salary Cap Management**: Automatic salary cap enforcement ($50,000)
- **Position Constraints**: Enforces position requirements (QB: 1, RB: 2-3, WR: 3-4, TE: 1-2, DST: 1)
- **Team Stacking Limits**: Configurable team stacking constraints

### 📊 Data Collection
- **DraftKings Integration**: Direct data collection from DraftKings API
- **Player Props**: Integration with sportsbook APIs for player props
- **Projections**: Support for multiple projection sources
- **Historical Data**: Leverages existing NFL database for historical analysis

### 🌐 Web Interface
- **Modern UI**: Beautiful, responsive web interface built with Bootstrap 5
- **Real-time Optimization**: Live lineup generation and validation
- **Data Visualization**: Statistics and player analysis
- **Export Functionality**: Export lineups to CSV format
- **Mobile Responsive**: Works seamlessly on all devices

### 🔧 Advanced Features
- **Leverage Optimization**: Considers ownership projections for contrarian plays
- **Correlation Analysis**: Player correlation matrix for advanced optimization
- **Exposure Management**: Control player exposure across multiple lineups
- **Lineup Validation**: Automatic validation against site rules
- **Performance Analytics**: Detailed statistics and analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nfl-dfs-optimizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   Open your browser and navigate to `http://localhost:5000`

### Environment Variables

You can configure the application using environment variables:

```bash
export HOST=0.0.0.0          # Server host (default: 0.0.0.0)
export PORT=5000             # Server port (default: 5000)
export DEBUG=False           # Debug mode (default: False)
```

## Usage

### Web Interface

1. **Data Collection**
   - Select the NFL week and season
   - Configure DraftKings contest parameters
   - Click "Collect Data" to fetch player information

2. **Optimization Settings**
   - Choose number of lineups to generate
   - Set maximum player exposure
   - Select optimization type (Standard/Leverage/Correlation)
   - Configure leverage weight if using leverage optimization

3. **Generate Lineups**
   - Click "Optimize Lineups" to generate optimal lineups
   - Review generated lineups with projected points and salary information
   - Export lineups to CSV if needed

### API Endpoints

The application provides RESTful API endpoints:

- `POST /api/collect-data` - Collect player data
- `POST /api/optimize` - Generate optimized lineups
- `GET /api/players` - Get player data with filters
- `GET /api/stats` - Get optimization statistics
- `GET /api/health` - Health check endpoint

### Command Line Usage

You can also use the optimizer programmatically:

```python
from dfs_optimizer.data_collector import DataCollector
from dfs_optimizer.optimizer import AdvancedOptimizer

# Collect data
collector = DataCollector()
data = collector.collect_all_data(week=1, season=2024)

# Optimize lineups
optimizer = AdvancedOptimizer()
optimizer.set_players(data['draftkings'])
optimizer.set_constraints({'salary_cap': 50000})

lineups = optimizer.optimize_lineup(num_lineups=5)
```

## Configuration

### DraftKings Settings

The application is pre-configured for DraftKings NFL contests:

- **Contest Type ID**: 21 (NFL)
- **Draft Group ID**: 131064 (Week 1, 2024)
- **Salary Cap**: $50,000
- **Total Players**: 9
- **Position Limits**: QB: 1, RB: 2-3, WR: 3-4, TE: 1-2, DST: 1

### Optimization Parameters

- **Standard Optimization**: Maximizes projected points within constraints
- **Leverage Optimization**: Considers ownership projections for contrarian plays
- **Correlation Optimization**: Uses player correlation matrix for advanced optimization

## Data Sources

### Current Integration
- **DraftKings**: Player salaries and contest information
- **NFL Database**: Historical player performance data

### Planned Integration
- **Sportsbook APIs**: Player props and betting lines
- **Projection Services**: Multiple projection sources
- **Ownership Data**: Contest ownership projections

## Architecture

```
dfs_optimizer/
├── __init__.py              # Package initialization
├── data_collector.py        # Data collection from various sources
├── optimizer.py             # Linear programming optimization engine
├── web_app.py              # Flask web application
└── templates/
    └── index.html          # Main web interface

app.py                      # Application entry point
requirements.txt            # Python dependencies
```

## Optimization Algorithm

The optimizer uses linear programming to solve the following problem:

**Objective Function**: Maximize total projected points
```
Maximize: Σ(player_i × projected_points_i)
```

**Constraints**:
- Salary cap: Σ(player_i × salary_i) ≤ $50,000
- Position requirements: QB=1, RB=2-3, WR=3-4, TE=1-2, DST=1
- Team stacking: Σ(players_from_team_j) ≤ 4
- Total players: Σ(player_i) = 9

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and entertainment purposes only. Please ensure compliance with all applicable laws and terms of service when using DFS optimization tools. The authors are not responsible for any financial losses incurred through the use of this software.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the code comments
- Review the API endpoints for integration help

## Roadmap

### Phase 1 (Current)
- ✅ Basic optimization engine
- ✅ DraftKings data integration
- ✅ Web interface
- ✅ Lineup validation

### Phase 2 (Planned)
- 🔄 Multiple projection sources
- 🔄 Advanced correlation analysis
- 🔄 Ownership projections
- 🔄 Contest-specific optimization

### Phase 3 (Future)
- 📋 Multi-site support (FanDuel, Yahoo)
- 📋 Machine learning projections
- 📋 Real-time optimization
- 📋 Mobile application

## Acknowledgments

- Built with Flask, Pandas, and PuLP
- Inspired by professional DFS optimization tools
- Uses existing NFL database for historical data