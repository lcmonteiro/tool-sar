# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from flask        import Flask, render_template, request, jsonify
from SarParser    import SarParser
from SarSearch    import SarSearch
from SarFilter    import SarFilter
from SarTransform import SarTransform
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
            data.filtered = SarFilter()(data.parsed)
        # split
        if not hasattr(data, 'nodes'):
            data.nodes = SarTransform.split(data.filtered)
        # json
        return jsonify(data.nodes)
    #
    # startting point
    #
    app.run(debug=False, host='0.0.0.0', port=8080)
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------