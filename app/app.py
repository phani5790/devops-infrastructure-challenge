import os

from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Challenge Application",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/db")
def database_health():
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "devopsdb"),
            user=os.getenv("POSTGRES_USER", "devops"),
            password=os.getenv("POSTGRES_PASSWORD", "devopspassword")
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result and result[0] == 1:
            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200

        return jsonify({
            "status": "unhealthy",
            "database": "query failed"
        }), 503

    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "database": "connection failed",
            "error": str(error)
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
