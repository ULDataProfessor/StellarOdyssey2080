# StellarOdyssey2080

A text-based adventure game that combines RPG elements with space exploration and resource management. Explore the galaxy, trade goods, build your empire, and embark on epic space adventures.

## Features

- **Character Progression**: Level up, gain experience, and improve your skills with enhanced prerequisites system
- **Combat System**: Turn-based combat with various weapons and abilities
- **Space Exploration**: Navigate through different sectors and planets
- **Resource Management**: Manage credits, fuel, and supplies
- **Trading System**: Buy and sell goods between planets with dynamic markets
- **Quest System**: Complete missions and earn rewards
- **Web Interface**: Modern web-based interface with optimized performance
- **ASCII Art**: Beautiful text-based graphics and animations

## Recent Improvements

✅ **Fixed Critical Import Issues**: Web application now starts reliably  
✅ **Enhanced Skill System**: Proper prerequisites checking for skill unlocks  
✅ **Performance Optimizations**: Faster web UI with smooth animations  
✅ **Better Error Handling**: Robust API endpoints with proper validation  
✅ **Security Enhancements**: Input validation and XSS prevention  
✅ **Configuration Management**: Environment-aware settings for dev/production  

See [IMPROVEMENTS.md](docs/IMPROVEMENTS.md) for detailed technical information.

## Installation

1. Clone this repository
2. Use Python 3.10 or newer and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   # Console version
   python main.py
   
   # Web interface
   cd web && python app.py
   # Then visit http://localhost:5002
   ```

## Game Controls

- **Movement**: Use cardinal directions (north, south, east, west) or shortcuts (n, s, e, w)
- **Actions**: Type commands like "look", "inventory", "status", "help"
- **Combat**: Use "attack", "defend", "use [item]", "flee"
- **Trading**: Use "buy", "sell", "trade"
- **Navigation**: Use "travel", "land", "takeoff"

## Game Structure

- `main.py` - Main game entry point
- `game/` - Core game modules
  - `player.py` - Player character and stats
  - `world.py` - Game world and locations
  - `combat.py` - Combat system
  - `trading.py` - Trading and economy system
  - `quests.py` - Quest and mission system
- `data/` - Game data files
- `utils/` - Utility functions and helpers

## Documentation

- [Dynamic Market System](docs/dynamic_market.md)
- [Save System](docs/save_system.md)
- [Mission Generator](docs/mission_generator.md)
- [AI Counselor](docs/ai_counselor.md)

## Contributing

Feel free to contribute by adding new features, fixing bugs, or improving the game mechanics!

## License

MIT License - feel free to use and modify as you wish.
