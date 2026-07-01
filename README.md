# HydroForecast — Production Forecasting Platform

Oil & gas production forecasting and reservoir simulation platform with decline curve analysis, water breakthrough detection, and real-time monitoring.

## Quick Start

```bash
docker compose up -d
```

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Features

- **Reservoir Management** — Store and manage reservoir properties (pressure, porosity, permeability, OOIP)
- **Decline Curve Analysis** — Automatic decline type classification (exponential, harmonic, hyperbolic)
- **Water Breakthrough Detection** — Real-time monitoring of water cut and water production rates
- **Production Forecasting** — Multi-well production data with interactive Recharts visualization
- **Recovery Estimation** — Calculate recovery factors and remaining reserves
- **Real-Time Alerts** — WebSocket-powered live alert feed for production anomalies
- **JWT Authentication** — Secure user registration and login

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), PostgreSQL, JWT, WebSockets
- **Frontend**: React 18, TypeScript, Vite, Recharts, Zustand
- **Infrastructure**: Docker, Docker Compose, Nginx

## Project Structure

```
backend/
  app/
    core/         — Config, security, database, deps
    models/       — User, Reservoir, ProductionForecast, Alert
    schemas/      — Pydantic models
    services/     — Business logic
    agents/       — Forecast engine (decline curve, recovery, water breakthrough)
    api/          — REST endpoints + WebSocket
frontend/
  src/
    store/        — Zustand stores (auth, hydro, websocket)
    components/   — StatsCards, ReservoirForm, ReservoirList, ForecastChart, AlertFeed
    pages/        — Login, Register, Dashboard
    hooks/        — useWebSocket
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login |
| GET | /api/reservoirs | List reservoirs |
| POST | /api/reservoirs | Create reservoir |
| GET | /api/reservoirs/stats | Reservoir stats |
| GET | /api/forecasts | List forecasts |
| POST | /api/forecasts | Create forecast entry |
| GET | /api/alerts | List alerts |
| PUT | /api/alerts/{id} | Update alert status |
| WS | /ws/forecast/{id} | Real-time forecast analysis |

## License

MIT
