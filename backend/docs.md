# Trivia API Documentation

#### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with the following properties:
  - success - boolean to state if the request was successful
  - categories - an object in the format of 'id: category_string' representing key: value pairs.
  - total_categories - stating the total number of categories.

- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

### GET /questions

- General:
  - Returns a list of question objects, success value, and total number of questions.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### POST /questions

- General:
  - Creates a new question using the following payload:

    ```
    {
        question: string,
        answer: string,
        category: string,
        difficulty: number
    }
    ```

  - Returns the id of the created question, success value, total questions, and question list like so.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question":"What is the capital of Nigeria", "answer":"Abuja", "category":"5", "difficulty": 5 }'`

```
{
  "success": true,
  "questions": [
    { 
        "question":"What is the capital of Nigeria", "answer":"Abuja", 
        "category":"5", 
        "difficulty": 5 
    },
    ...,
    {
        "question":"When is Christmas", 
        "answer":"December 25", 
        "category":"2", 
        "difficulty": 1 
    }
  ],
  "created": 10,
  "total_questions": 20
}
```

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, and a message to be displayed on the Frontend.
- `curl -X DELETE http://127.0.0.1:5000/questions/12`

```
{
    "success": true,
    "deleted": 12,
    "message": "Question deleted successfully!"
}
```

#### POST /search-questions

- General:
  - Filters through the question list to search for any word that's equal to the `searchTerm` passed in the payload.
  - Returns a list of questions that passes the search filter,  success value and total questions.

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "Title" }'`

```
{
  "success": true,
  "questions": [
    { 
        "question":"What is the title of Nigeria", "answer":"Abuja", 
        "category":"5", 
        "difficulty": 5 
    },
    ...,
    {
        "question":"When Title was he given", 
        "answer":"Chief of Staff", 
        "category":"2", 
        "difficulty": 1 
    },
    {
        "question":"The Family's Title was created in the year?", 
        "answer":"1908", 
        "category":"4", 
        "difficulty": 5 
    },
  ],
  "total_questions": 10
}
```

#### GET /categories/{category_id}/questions

- General:
  - Fetches all questions based on a particular category.
  - Returns a list of question objects, success value, current category, and total number of questions.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```
{
    "success": true,
    "current_category": "Science",
    "total_questions": 19
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 2,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 2,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ]
}
```

### POST /quizzes

- General
  - Fetch random questions to play the quiz. Endpoint accepts a     `quiz_category` object containing the category details and a `previous_questions` list containing the questions id that's been asked previously.
  - Returns a random question and success value.

- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{ "quiz_category": { "type": "Science", id: "2" }, "previous_questions": [11, 19] }'`

```
{
    "success": true,
    "question": {
        "answer": "Lionel Messi", 
        "category": 3, 
        "difficulty": 2, 
        "id": 22, 
        "question": "Who's the best player in the world"
    }
}
```

## Error Handling

Errors are returned in the following json format:

```
{
    'success': false,
    'error': 404,
    'message': 'resource not found'
}
```

The API returns 4 kinds of errors:

- 400: bad request
- 404: not found
- 422: unprocessable
- 500: internal server error
