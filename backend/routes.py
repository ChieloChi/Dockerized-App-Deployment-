from flask import Blueprint, request, jsonify
from db import get_connection

routes = Blueprint('routes', __name__)

# --- Health Check Route ---
@routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is running"}), 200


# --- Get all todos ---
@routes.route('/todos', methods=['GET'])
def get_todos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        conn.close()
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Add a new todo ---
@routes.route('/todos', methods=['POST'])
def add_todo():
    try:
        data = request.get_json()
        title = data.get('title')

        if not title:
            return jsonify({"error": "Title is required"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (title) VALUES (%s)", (title,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Todo added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Update a todo (mark completed, etc.) ---
@routes.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    try:
        data = request.get_json()
        completed = data.get('completed')

        if completed is None:
            return jsonify({"error": "Completed field is required"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET completed = %s WHERE id = %s", (completed, id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Todo updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Delete a todo ---
@routes.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Todo deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
