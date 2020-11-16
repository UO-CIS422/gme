"""
Simple Flask web site 
"""

import flask    # The basic framework for http requests, storing cookies, etc

import logging  # For monitoring and debugging

# Our own modules
from db.db_sqlite import write_ratings, read_ratings
import arrow

###
# Globals
###

import CONFIG   # Separate out per-machine configuration 
app = flask.Flask(__name__)   
app.secret_key = CONFIG.COOKIE_KEY
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)



#################
# Pages and request handling:
# We "route" URLs to functions by attaching
# the app.route 'decorator'.
#
# I typically use the same base name for URL, function,
# and html template, but that is just for readability ---
# url "/foo" could call function "bar()" which could
# render page "zot.html". 
#
#################

@app.route("/")
@app.route("/index")
def index():
  return flask.render_template('index.html')

@app.route("/display")
def display():
    flask.g.ratings = read_ratings(flask.session["member"], flask.session["timestamp"])
    app.logger.debug("Database query result: {}".format(flask.g.ratings))
    return flask.render_template('display.html')


#################
# Handle a form
#################

# Step 1: enter teammate names, to populate
# evaluation form
@app.route("/_teammates", methods=['POST'])
def set_teammates():
  app.logger.debug("Teammates list form: |{}|".format(flask.request.form))
  app.logger.debug("teammate field: |{}|".format(
    flask.request.form.getlist('teammate')))
  teammates=flask.request.form.getlist('teammate')
  yourself = flask.request.form.get('yourself')
  repo = flask.request.form.get('repo')
  team =  [ "{} (yourself)".format(yourself)] + list(teammates)
  return flask.render_template("eval-form.html", team=team, repo=repo)

# Step 2: Evaluations per teammate (including self)
#
@app.route("/_gme_form", methods=['POST'])
def evals():
  app.logger.debug("Evaluations: |{}|".format(flask.request.form))
  member = flask.request.form.get("teammate") # Should get first one
  member = member.replace(" (yourself)", "")  # Undo edit in set_teammates
  repo = flask.request.form.get("repo")
  per_member_fields = [ "teammate",
                        "dependable", "comments-dependable",
                        "constructive", "comments-constructive",
                        "engaged", "comments-engaged",
                        "productive", "comments-productive",
                        "asset", "comments-asset" ]

  # First the whole lists ... 
  fields = { }
  for field in per_member_fields:
    fields[field] = flask.request.form.getlist(field)

  # Timestamp identifies the transaction and prevents
  # later access by others
  timestamp = arrow.now().isoformat()

  # Then individual ratings 
  for i in range(len(fields["teammate"])):
    ratings = { "member": member }
    for field in per_member_fields:
      app.logger.debug("Probing instance {} of field {} in {}".format(i,field,fields))
      ratings[field] = fields[field][i]
    write_ratings(timestamp, repo, ratings)
    
  flask.session["member"] = member
  flask.session["timestamp"] = timestamp
  return flask.redirect("/display")


###################
#   Error handlers
#   These are pages we display when something goes wrong
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return flask.render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
  app.logger.warning("++ 500 error: {}".format(e))
  assert app.debug == False  ## Crash me please, so I can debug! 
  return flask.render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return flask.render_template('403.html'), 403


###############
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#   (Currently none, leaving this here as an example)
###############
# @app.route("/_check")
# def _check():
#   tray = request.args.get("tray", "", type=str)
#   pattern = request.args.get("pattern", "XXX", type=str)
#   matches = find.search(WORDS, pattern, tray)
#   ### Matches returns a list of words
#   return jsonify(result={ "words": " ".join(matches) })

#############
# Filters
# These process some text before inserting into a page
#############
@app.template_filter('humanize')
def humanize(date):
    """Humanize an ISO date string"""
    as_arrow = arrow.get(date)
    return as_arrow.humanize()

# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#
if __name__ == "__main__":
    # Running standalone
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    pass


