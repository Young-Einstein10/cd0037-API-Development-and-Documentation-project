import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from settings import TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            TEST_DB_USER, TEST_DB_PASSWORD, "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # ================= CATEGORIES ================= #
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(isinstance(data["current_category"], str))
        self.assertTrue(data["total_questions"])

    # ================= CATEGORIES ================= #

    # ================= QUESTIONS ================= #

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_questions"])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(isinstance(data["total_questions"], int))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_unavailable_question(self):
        res = self.client().delete("/questions/300")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 3).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        new_questions = {
            'question': 'What year was Messi born?',
            'answer': '2000',
            'category': '5',
            'difficulty': 4,
        }
        res = self.client().post("/questions", json=new_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_search_questions(self):
        search_term = {
            'searchTerm': 'title'
        }
        res = self.client().post("/search-questions", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_play_quiz(self):
        payload = {
            'previous_questions': [2, 6],
            'quiz_category': {
                'id': 5,
                'type': 'Entertainment'
            }
        }

        res = self.client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    # ================= QUESTIONS ================= #


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
