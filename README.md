# 3D AR Demo Project

A comprehensive 3D model generation and AR viewing system that integrates MCP (Model Context Protocol) servers, Tripo AI API for 3D generation, and web-based AR viewing capabilities.

## Features

- **3D Model Generation**: Generate high-quality 3D models using Tripo AI API
- **MCP Server Integration**: Model Context Protocol server for AI model interactions
- **AR Viewer**: Web-based AR viewer for 3D model visualization
- **Multi-format Support**: GLB, USDZ, and OBJ format support
- **File Management**: Automated file organization and metadata management
- **Web Interface**: Modern web UI for model generation and viewing

## Architecture

The project consists of several key components:

- **MCP Server**: Handles AI model interactions and tool execution
- **Web Server**: Flask-based web application for user interface
- **API Clients**: External API integrations (Tripo AI)
- **Services**: Business logic for model generation and file management
- **AR Viewer**: Web-based 3D model viewer with AR capabilities

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd 3d-ar-demo
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. **Start the servers**:
   ```bash
   # Start MCP server
   python scripts/start_mcp_server.py
   
   # Start web server (in another terminal)
   python scripts/start_web_server.py
   ```

6. **Access the application**:
   - Web interface: http://localhost:5000
   - MCP server: Configure in your MCP client

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Tripo AI API Configuration
TRIPO_API_KEY=your_tripo_api_key
TRIPO_API_URL=https://api.tripo.ai

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000

# Web Server Configuration
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=5000
DEBUG=True

# File Storage
MODEL_STORAGE_PATH=./data/generated_models
CACHE_PATH=./data/cache
LOG_PATH=./data/logs
```

### API Keys

- **Tripo AI**: Get your API key from [Tripo AI](https://tripo.ai)
- Configure the API key in your `.env` file

## Usage

### Web Interface

1. Open http://localhost:5000 in your browser
2. Enter a text prompt describing the 3D model you want to generate
3. Select generation parameters (format, quality, etc.)
4. Click "Generate Model"
5. View the generated model in the AR viewer

### MCP Server

The MCP server provides tools for:
- 3D model generation
- File management
- Model metadata retrieval
- Format conversion

Configure your MCP client to connect to the server at `localhost:8000`.

### API Endpoints

- `POST /api/generate` - Generate a new 3D model
- `GET /api/models` - List all generated models
- `GET /api/models/<id>` - Get model details
- `GET /api/models/<id>/download` - Download model file
- `POST /api/convert` - Convert model format

## Development

### Project Structure

```
3d-ar-demo/
├── src/                    # Source code
│   ├── mcp_server/        # MCP server components
│   ├── api_clients/       # External API integrations
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic services
│   ├── utils/             # Utility functions
│   └── web/               # Web server components
├── data/                  # Data storage
├── config/                # Configuration files
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
└── deployment/            # Deployment configurations
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

### Code Style

The project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose -f deployment/docker/docker-compose.yml up -d
```

### System Service Deployment

```bash
# Copy service files
sudo cp deployment/systemd/*.service /etc/systemd/system/

# Enable and start services
sudo systemctl enable mcp-server
sudo systemctl enable web-server
sudo systemctl start mcp-server
sudo systemctl start web-server
```

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your Tripo AI API key is correctly configured
2. **Port Conflicts**: Check if ports 5000 and 8000 are available
3. **File Permissions**: Ensure the application has write access to data directories
4. **Dependencies**: Make sure all Python packages are installed correctly

### Logs

Check the following log files for debugging:
- `data/logs/mcp_server.log` - MCP server logs
- `data/logs/web_server.log` - Web server logs
- `data/logs/api_calls.log` - API interaction logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the `docs/` directory
- Review the troubleshooting guide

## Roadmap

- [ ] Enhanced AR viewer with gesture controls
- [ ] Batch model generation
- [ ] Model editing capabilities
- [ ] Integration with additional 3D APIs
- [ ] Mobile app companion
- [ ] Real-time collaboration features 