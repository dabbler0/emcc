#!/usr/bin/env python
import simplejson as json
import urlparse
import os
import auth
import memcache

if __name__ == "__main__":
  # Parse the path
  qwargs = urlparse.parse_qs(os.environ["QUERY_STRING"])

  # Enforce one value per query string argument
  for key in qwargs:
    qwargs[key] = qwargs[key][0]
  
  # Initialize our memcache client
  cache = memcache.Client(["localhost:11211"], debug=0)
  
  # Initialize our database connection
  conn = sqlite3.connect("teams.db")
  c = conn.cursor()

  # Get the teams belonging to this user
  c.execute("UPDATE teams SET name=?, members=? WHERE id=?", (qwargs["name"], qwargs["members"], qwargs["id"]))
  conn.commit()

  # Get the session key for this user
  key = auth.dehexify(cache.get("__SRP_SESSKEY:" + qwargs["uname"]))
  
  print "content-type: application/json"
  print ""
  print auth.encrypt(key, json.dumps({
    "success": True if c.rowcount == 1 else False
  }))
