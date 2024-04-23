# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/powers', methods=['GET'])
# def get_powers():
#     limit = request.args.get('limit', default=10, type=int)
#     powers = select_all_powers(limit)
#     return jsonify([power.to_dictionary() for power in powers])

# def select_all_powers(limit):
#     print(DATABASE_FILE)
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     # Get column names from the sales table
#     cur.execute('SELECT * FROM powers LIMIT ?', (limit,))
#     results = cur.fetchall()
#     powers = []
#     for result in results:
#         power = Power(result[1], result[2], result[3], result[0])
#         powers.append(power)
#     return powers

import psycopg2
from flask import Flask, request, jsonify
from controller import connection_string

app = Flask(__name__)

@app.route('/powers', methods=['GET'])
def get_powers():
    limit = request.args.get('limit', default=10, type=int)
    powers = select_all_powers(limit)
    return jsonify([power.to_dictionary() for power in powers])

def select_all_powers(limit):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        cur.execute('SELECT * FROM powers LIMIT %s', (limit,))
        results = cur.fetchall()
        powers = []
        for result in results:
            power = Power(result[1], result[2], result[3], result[0])
            powers.append(power)
        cur.close()
        conn.close()
        return powers
    except psycopg2.Error as e:
        print(f"Error in select_all_powers: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)


