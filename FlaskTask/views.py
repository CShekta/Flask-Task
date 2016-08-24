from FlaskTask import app
from flask import (abort,
                   make_response,
                   redirect,
                   render_template,
                   request,
                  )
import time
import random

CHARSETS = ['ISO-8859-1', 'ISO-8859-2', 'windows-1256', 'windows-1257', 'windows-1258', 'UTF-7', 'shift_jis']

EXAMPLE_STATUS_CODES = [200, 201, 202, 303, 304, 305, 306, 307,
                        308, 400, 401, 402, 403, 404, 405, 406,
                        421, 422, 423, 424, 428, 444, 500, 501,
                        521, 522, 523, 524, 525, 526] + random.sample(xrange(200, 999), 10)


@app.route('/')
@app.route('/index')
def index():
    domain = request.headers['Host']
    return render_template('index.html',
                           title='Home',
                           charset_list=CHARSETS,
                           domain=domain,
                           status_list=EXAMPLE_STATUS_CODES)


@app.route('/headers/timeout_truncated')
def truncated():
    response = make_response(render_template('/headers/truncated.html'))
    response.headers['Content-Length'] = 1000
    return response


@app.route('/status_codes/<code>')
def status_codes(code):
    return render_template('status_code.html',
                           title='Status Codes',
                           ), code


@app.route('/encoding/<charset>')
def encoding(charset):
    response = make_response(render_template('/encoding/encoding.html',
                             title='Encoding',
                             charset=charset).encode(charset))
    response.headers['Content-Type'] = 'text/html; charset=' + str(charset)
    return response


@app.route('/xrobots/<tag>')
def xrobots(tag):
    response = make_response(render_template('/robots/xrobots.html',
                             title='XRobot Tags',
                             tag=tag))
    response.headers['X-Robots-Tag'] = tag
    return response


@app.route('/robots/<tag>')
def robots(tag):
    return render_template('/robots/robots.html',
                           title="Robot Tags",
                           tag=tag)


@app.route('/links/<issue>')
def links(issue):
    return render_template('/links/' + str(issue) + '.html')


@app.route('/head/<issue>')
def head(issue):
    return render_template('/head/' + str(issue) + '.html')


@app.route('/redirects/missing_location')
def missing_location():
    return redirect("", code=301)


@app.route('/redirects/relative')
def relative_redirects():
    response = make_response(render_template('/empty.html'))
    response.status_code = 301
    response.headers['Location'] = '/redirects/rel-redirect-target'
    return response


@app.route('/redirects/rel-redirect-target')
def rel_redirect_target():
    return render_template('/redirects/rel-redirect-target.html')


@app.route('/encoding_type/<encoding_type>')
def compression(encoding_type):
    response = make_response(render_template('/encoding/compression.html',
                                             title=encoding_type))
    response.headers['Content-Encoding'] = encoding_type
    return response


@app.route('/headers/refresh')
def refresh():
    response = make_response(render_template('/headers/refresh.html',
                                             title='refresh'))
    response.headers['Refresh:'] = '0; url=http://www.example.org/fresh-as-a-summer-breeze'
    return response


@app.route('/delay/<delay>')
def delay_response(delay):
    delay = min(float(delay), 90)

    time.sleep(delay)

    return render_template('/delay.html',
                           title="Delayed")


@app.route('/empty')
def empty():
    return render_template('/empty.html')


### really large crawls
@app.route('/site/infinite')
@app.route('/site/infinite/<int:page_number>')
def infinite_site(page_number=0):
    """Return a page from an infinitely large site that has just one outlink."""
    next_page = page_number + 1
    return render_template('/sites/infinite.html',
                           title='Infinite {}'.format(next_page),
                           next_page=next_page)

@app.route('/site/infinite_degree')
@app.route('/site/infinite_degree/<int:page_number>')
@app.route('/site/infinite_degree/<int:outdegree>/<int:page_number>')
def infinite_degree(page_number=0, outdegree=10):
    """Return a page from a site where each page has a specific degree."""
    if outdegree == 0:
        abort(404)
    next_pages = range(page_number + 1, page_number + outdegree + 1)
    return render_template(
        '/sites/infinite_degree.html',
        title='Infinite {} with degree {}'.format(page_number, outdegree),
        degree=outdegree,
        next_pages=next_pages
    )
