import requests
import os
import json

from flask import Flask, Response, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('base.html')

@app.route('/api', methods=["GET"])
def api():
    request.args['tables'] = [
        table for table in\
        request.args.get('tables', request.args.get('table')).split('+')
    ]
    pg_cursor.execute(
        """ SELECT {columns}
            FROM {tables}
            {min_date_clause}
            {max_date_clause}
            ORDER BY a.DATE ASC;
        """, {
            'columns': ,
            'tables': '{} base'.format(request.args['tables'][0]) +\
                reduce(
                    lambda table_list, table: table_list + table,
                    [
                        '\nLEFT JOIN {table} ON base.DATE = {table}.DATE'.format(table=table)\
                        for table in request.args['tables'][1:]
                    ]
                ),
            'min_date_clause': 'WHERE a.DATE => {min_date_clause}'.format(
                request.args['min_date'] if request.args.get('min_date') else ''
            ),
            'max_date_clause': (
                'AND ' if request.args.get('min_date') else 'WHERE '\
                + 'a.DATE <= {max_date}'.format(
                    request.args['max_date']
                )
            ) if request.args.get('max_date') else ''
        }
    )
    response_content = json.dumps({})
    return Response(response_content,  mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)
