# Display Card Microservice

**This microservice** fetches and returns detailed information about a specific recipe in a structured format, suitable for display in a UI card. It is implemented using Python, Flask, and SQLite.

## Base URL

```
http://localhost:5000
```

## Endpoint

### GET /recipe/\<recipe\_id>

Retrieve a complete display card for a specific recipe by ID.

**Example**

```bash
curl http://localhost:5000/recipe/1
```

**Response**

```json
{
  "id": 1,
  "title": "Spaghetti Bolognese",
  "description": "A classic Italian pasta dish with meat sauce.",
  "difficulty": "Medium",
  "cuisine": "Italian",
  "created_at": "2025-05-22T22:14:30.528Z",
  "ingredients": [
    { "name": "Spaghetti", "quantity": 200, "unit": "grams" },
    { "name": "Ground Beef", "quantity": 150, "unit": "grams" },
    { "name": "Tomato Sauce", "quantity": 100, "unit": "ml" }
  ],
  "steps": [
    { "step_number": 1, "instruction": "Boil spaghetti until al dente." },
    { "step_number": 2, "instruction": "Brown the ground beef in a skillet." },
    { "step_number": 3, "instruction": "Add tomato sauce and simmer for 15 minutes." },
    { "step_number": 4, "instruction": "Combine spaghetti and sauce before serving." }
  ]
}
```

## How to Receive Data

Responses are structured JSON objects containing:

* Top-level metadata about the recipe (title, description, cuisine, etc.)
* A list of ingredients with name, quantity, and units
* An ordered list of preparation steps

## Notes

* Ensure the `recipe_id` passed exists in the database otherwise a 404 error will be returned.
* It will try to make a default recipe, with has id: 1. Delete it if that's not what you wanted.

