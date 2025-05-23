# Time Converter Microservice

**This microservice** converts between 12-hour and 24-hour time formats. It is stateless and implemented with Python and Flask.

## Base URL

```
http://localhost:5000
```

## Endpoints

### POST /convert

Convert a time string to the desired format (12-hour or 24-hour).

**Request Body**

```json
{
  "input_time": "5:30 PM",
  "target_format": "24"
}
```

**Example**

```bash
curl -X POST http://localhost:5000/convert \
     -H "Content-Type: application/json" \
     -d '{"input_time":"5:30 PM", "target_format":"24"}'
```

**Response**

```json
{
  "input_time": "5:30 PM",
  "converted_time": "17:30",
  "format": "24"
}
```

### Alternate Example: Convert to 12-hour format

```bash
curl -X POST http://localhost:5000/convert \
     -H "Content-Type: application/json" \
     -d '{"input_time":"14:30", "target_format":"12"}'
```

**Response**

```json
{
  "input_time": "14:30",
  "converted_time": "02:30 PM",
  "format": "12"
}
```

## How to Receive Data

Responses will contain the original input, converted time string, and the resulting format. All data is JSON.

## Notes

* Acceptable values for `target_format`: "12" or "24"
* The microservice auto-detects whether input is 12-hour or 24-hour formatted.
* If the input is malformed, the service returns a 400 with a descriptive error.
