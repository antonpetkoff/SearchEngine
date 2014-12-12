from flask import Flask
from flask import request
from flask import render_template
from local_settings import debug_mode
from search_engine import SearchEngine

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def do_something():
    query = request.args.get('query', '')
    se = SearchEngine()
    results = se.make_query(query)

    return render_template('result.html', data=results)


if __name__ == '__main__':
    app.run(debug=debug_mode)
