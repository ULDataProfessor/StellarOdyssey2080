StellarOdyssey2080 Web (Flask + PWA)
================================

Run (dev)
---------

1. `python run.py`
2. Visit `http://localhost:5002`

PWA
---

- Manifest: `/manifest.json`
- Service Worker: `/service-worker.js` (cache-first static, network-first API)
- Offline page: `/offline.html`
- Install button in header appears when eligible

Fonts
-----

- Google Fonts: Orbitron, Share Tech Mono

Directory
---------

- `templates/index.html` is served by Flask
- `css/`, `js/`, `icons/`, and PWA assets live under `/web`

# StellarOdyssey2080 Web Edition (Flask)

A modern web interface for the StellarOdyssey2080 space trading game built with Flask.

## 🚀 Quick Start

### Development Setup

Use Python 3.10 or newer for the pinned web and development dependencies.
These security updates are verified on Python 3.12.

1. **Install Dependencies**
   ```bash
   cd web/
   pip install -r requirements-web.txt
   ```

2. **Run Development Server**
   ```bash
   python app.py
   # or
   python run.py
   ```

3. **Access the Game**
   - Open: http://localhost:5000
   - API: http://localhost:5000/api/

### Production Deployment

#### Using Docker (Recommended)

1. **Build and Run**
   ```bash
   docker-compose up -d
   ```

2. **Environment Variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DEBUG=false
   ```

#### Manual Deployment

1. **Install Production Server**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 🎮 Features

### Core Game Features
- **Real-time Gameplay**: Full space trading simulation
- **Dynamic Markets**: Market prices based on supply/demand
- **Procedural Galaxy**: Infinite sectors with unique content
- **Enhanced Combat**: Tactical ship-to-ship combat
- **Mission System**: Quests and storylines
- **Skill Progression**: Character development
- **Save/Load**: Persistent game state

### Web-Specific Features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live game state synchronization
- **Modern UI**: Space-themed interface with animations
- **REST API**: Full API for external integrations
- **Session Management**: Secure player data handling

## 🛠️ API Endpoints

### Game State
- `GET /api/status` - Get current game state
- `POST /api/save` - Save game
- `POST /api/load` - Load game

### Navigation
- `POST /api/travel` - Travel to sector
- `GET /api/galaxy` - Get galaxy map

### Trading
- `GET /api/market` - Get market prices
- `POST /api/trade` - Execute trade

### Combat & Missions
- `POST /api/combat` - Combat actions
- `GET /api/missions` - Get available missions

### Debug (Development Only)
- `GET /api/debug/info` - System information
- `GET /api/debug/reset` - Reset game state

## 🏗️ Architecture

```
web/
├── app.py              # Main Flask application
├── run.py              # Production runner
├── config.py           # Configuration management
├── requirements-web.txt # Python dependencies
├── Dockerfile          # Container definition
├── docker-compose.yml  # Container orchestration
├── templates/          # HTML templates
│   └── index.html      # Main game interface
├── css/               # Stylesheets
│   ├── style.css      # Main styles
│   └── terminal.css   # Terminal styles
└── js/                # JavaScript
    └── game.js        # Game client logic
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session key | `dev-secret` |
| `DEBUG` | Enable debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |

### Game Settings
- **Max Sectors**: 1000 procedural sectors
- **Auto-save**: Every 5 minutes
- **Session Timeout**: Browser session (no server timeout)

## 🚀 Deployment Options

### 1. Local Development
```bash
python app.py
```

### 2. Production Server
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 3. Docker Container
```bash
docker build -t logdtw2002-web .
docker run -p 5000:5000 logdtw2002-web
```

### 4. Cloud Platforms

#### Heroku
```bash
# Add Procfile: web: gunicorn app:app
git push heroku main
```

#### Railway/Render
- Connect GitHub repository
- Set build command: `pip install -r requirements-web.txt`
- Set start command: `python run.py`

#### AWS/GCP/Azure
- Use provided Dockerfile
- Deploy as container service

## 🔒 Security

### Production Checklist
- [ ] Set strong `SECRET_KEY`
- [ ] Disable debug mode (`DEBUG=False`)
- [ ] Use HTTPS in production
- [ ] Set up proper logging
- [ ] Configure session timeouts
- [ ] Enable CSRF protection
- [ ] Set up rate limiting

## 📊 Monitoring

### Health Checks
- Endpoint: `/api/status`
- Docker: Built-in healthcheck
- Expected response: `{"success": true, ...}`

### Logs
- Application logs: Console output
- Access logs: Gunicorn/server logs
- Error tracking: Flask error handlers

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest

# Test API endpoints
curl http://localhost:5000/api/status
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: Create GitHub issue
- **Documentation**: Check main README.md
- **API**: Use `/api/debug/info` for system status

---

**Ready to explore the galaxy? 🚀**

Start your space trading adventure at http://localhost:5000!
