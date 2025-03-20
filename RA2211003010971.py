from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

WINDOW_SIZE = 10
TIMEOUT = 0.5  # 500 ms
API_ENDPOINTS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/fibo',
    'r': 'http://20.244.56.144/test/rand'
}

window = []

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except (requests.exceptions.RequestException, ValueError):
        return []


def calculate_average():
    if window:
        return round(sum(window) / len(window), 2)
    return 0.0

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in API_ENDPOINTS:
        return jsonify({"error": "Invalid number ID"}), 400

    
    numbers = fetch_numbers(API_ENDPOINTS[number_id])
    
    unique_numbers = list(set(numbers))  
    global window
    previous_window = window.copy()

    for num in unique_numbers:
        if num not in window:
            window.append(num)
    
    
    if len(window) > WINDOW_SIZE:
        window = window[-WINDOW_SIZE:]

    
    avg = calculate_average()

    response_data = {
        "windowPrevState": previous_window,
        "windowCurrState": window,
        "numbers": numbers,
        "avg": avg
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=9876)
