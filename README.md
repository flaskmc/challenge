Getting Started
=======================
1. Pull the repository.
2. Copy four csv files (`shops.csv`, `products.csv`, `tags.csv` and `taggings.csv`) provided in the original into the "data" directory.
3. To run the server:
  ```
  $ python runserver.py
  ```
4. To run the client:

  ```
  $ cd client
  $ python -m SimpleHTTPServer
  ```

* Note1: By default server binds to 0.0.0.0:5000 and the client binds to 0.0.0.0:8000/ . In case you wish to change the address and/or port of the server you will need to update "map.js" which is in the "client" directory.
