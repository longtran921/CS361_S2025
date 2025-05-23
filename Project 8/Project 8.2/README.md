# Countdown Timer Microservice

**This microservice** allows users to start and track a countdown timer based on predefined durations. It is implemented using Python, Flask, and SQLite.

## Base URL

```
http://localhost:5000
```

## Endpoints

### GET /durations

List all available timer durations.

**Example**

```bash
curl http://localhost:5000/durations
```

**Response**

```json
[
  { "id": 1, "label": "Pomodoro", "seconds": 1500 },
  { "id": 2, "label": "Short Break", "seconds": 300 }
]
```

### POST /start

Start a countdown timer for a selected duration.

**Request Body**

```json
{
  "duration_id": 1
}
```

**Example**

```bash
curl -X POST http://localhost:5000/start \
     -H "Content-Type: application/json" \
     -d '{"duration_id": 1}'
```

**Response**

```json
{
  "message": "Countdown started",
  "countdown_id": 1,
  "ends_at": "2025-05-22T22:10:00Z"
}
```

### GET /status/\<countdown\_id>

Get the status of a running countdown.

**Example**

```bash
curl http://localhost:5000/status/1
```

**Response**

```json
{
  "countdown_id": 1,
  "remaining_seconds": 1340,
  "is_active": true
}
```

## How to Receive Data

All responses are JSON objects containing countdown status or timer metadata. Clients should parse the `remaining_seconds` field to display time visually.

## Notes

* This service continues counting down in the background using end timestamps.
* No real-time updates are pushed; clients must poll `/status/<id>`.
* All durations must be preconfigured or seeded in the database.
