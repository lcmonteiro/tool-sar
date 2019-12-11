# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from flask                 import Flask, render_template, request, jsonify
from toolsar.sar_parser    import SarParser
from toolsar.sar_search    import SarSearch
from toolsar.sar_filter    import SarFilter
from toolsar.sar_transform import SarTransform
# -------------------------------------------------------------------------------------------------
# code
# -------------------------------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(params):
    app = Flask(__name__)
    # page services
    @app.route("/")
    def index():
        return render_template("basic.html")
        #return render_template("test.html")
    # data service
    @app.route("/data")
    def data():
        # parse
        if not hasattr(data, 'parsed'):
            data.parsed = SarParser(params.path)()
        # filter
        if not hasattr(data, 'filtered'):
            data.filtered = SarFilter(params.target, params.filter)(data.parsed)
        # split
        if not hasattr(data, 'nodes'):
            data.nodes = SarTransform.split(data.filtered)
        # json
        return jsonify(data.nodes)
    #
    # startting point
    #
    app.run(debug=True, host='0.0.0.0', port=8080)
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------