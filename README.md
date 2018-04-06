Getting Started
=======================
1. Clone the repository.
2. Install modules (sortedcontainers,PyTrie,pytest,proximityhash,Geohash,geopy,Flask-Cors, Flask)
3. To run the server:
  ```
  $ python runserver.py
  ```
4. To run the client:

  ```
  $ cd client
  $ python -m SimpleHTTPServer
  ```
5. Open http://0.0.0.0:8000 on your browser.

* Note: By default server binds to 0.0.0.0:5000 and the client binds to 0.0.0.0:8000/ . In case you wish to change the address and/or port of the server you will need to update "map.js" which is in the "client" directory.
