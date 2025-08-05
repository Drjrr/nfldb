# NFL DFS Optimizer - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd /workspace
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv dfs_env
   source dfs_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Quick Start

### Option 1: Web Interface (Recommended)

1. **Start the web application**
   ```bash
   source dfs_env/bin/activate
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Use the interface**
   - Select NFL week and season
   - Click "Collect Data" to fetch player information
   - Configure optimization settings
   - Click "Optimize Lineups" to generate optimal lineups

### Option 2: Command Line

1. **Run the example script**
   ```bash
   source dfs_env/bin/activate
   python example_usage.py
   ```

2. **Test data collection**
   ```bash
   source dfs_env/bin/activate
   python test_data_collection.py
   ```

## 📊 Features

### ✅ What's Working Now
- **DraftKings Data Collection**: Fetches real player data from DraftKings
- **Linear Programming Optimization**: Generates optimal lineups using PuLP
- **DraftKings NFL Rules**: Full compliance with contest rules
- **Web Interface**: Modern, responsive UI
- **Lineup Validation**: Automatic validation against site rules
- **Multiple Lineup Generation**: Generate up to 150 lineups
- **Exposure Management**: Control player exposure across lineups

### 🔄 Coming Soon
- **Player Props Integration**: Sportsbook APIs for player props
- **Projection Sources**: Multiple projection services
- **Ownership Data**: Contest ownership projections
- **Advanced Correlation**: Player correlation analysis
- **Export Functionality**: CSV export for lineups

## 🎯 Example Output

```
🏈 NFL DFS Optimizer - Example Usage
==================================================

1. Creating sample player data...
   Created 35 sample players

2. Initializing optimizer...
   Set constraints: {'salary_cap': 50000, 'total_players': 9, 'max_team_players': 4}

3. Generating single optimal lineup...
   Generated lineup with 135.1 projected points
   Total salary: $50,000
   Salary remaining: $0
   Lineup valid: True

   Selected Players:
   --------------------------------------------------------------------------------
   QB | Justin Herbert            | LAC | $ 7,600 |  22.8 pts
   RB | Joe Mixon                 | CIN | $ 6,200 |  16.5 pts
   RB | Rhamondre Stevenson       | NE  | $ 5,800 |  15.2 pts
   WR | Tee Higgins               | CIN | $ 6,400 |  16.8 pts
   WR | Chris Olave               | NO  | $ 5,800 |  14.5 pts
   WR | Drake London              | ATL | $ 5,400 |  13.8 pts
   TE | T.J. Hockenson            | MIN | $ 5,200 |  13.8 pts
   TE | Kyle Pitts                | ATL | $ 4,800 |  12.5 pts
   DST | New England Patriots      | NE  | $ 2,800 |   9.2 pts
```

## 🔧 Configuration

### DraftKings Settings
- **Contest Type ID**: 21 (NFL)
- **Draft Group ID**: 131064 (Week 1, 2024)
- **Salary Cap**: $50,000
- **Total Players**: 9
- **Position Limits**: QB: 1, RB: 2-3, WR: 3-4, TE: 1-2, DST: 1

### Optimization Types
- **Standard**: Maximizes projected points within constraints
- **Leverage**: Considers ownership projections for contrarian plays
- **Correlation**: Uses player correlation matrix for advanced optimization

## 📁 Project Structure

```
dfs_optimizer/
├── __init__.py              # Package initialization
├── data_collector.py        # Data collection from various sources
├── optimizer.py             # Linear programming optimization engine
├── web_app.py              # Flask web application
└── templates/
    └── index.html          # Main web interface

app.py                      # Application entry point
example_usage.py            # Example script
test_data_collection.py     # Test script
requirements.txt            # Python dependencies
README_DFS_OPTIMIZER.md     # Full documentation
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure virtual environment is activated
   source dfs_env/bin/activate
   ```

2. **Port Already in Use**
   ```bash
   # Change port in app.py or set environment variable
   export PORT=5001
   python app.py
   ```

3. **Data Collection Fails**
   - Check internet connection
   - Verify DraftKings contest is active
   - Try different contest type ID or draft group ID

### Getting Help

- Check the full documentation in `README_DFS_OPTIMIZER.md`
- Review the example scripts
- Check the logs in `dfs_optimizer.log`

## 🎉 Success!

You now have a fully functional NFL DFS optimizer that can:
- Collect real player data from DraftKings
- Generate optimal lineups using advanced algorithms
- Provide a beautiful web interface
- Validate lineups against contest rules

Happy optimizing! 🏈💰