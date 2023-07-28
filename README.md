# API

GET /products - fetch product list
GET /products/{id} - retrive single product
GET /products/upload_products/ - fetch from file, parse and upload to DB
POST /products/{id}/sold/ - mark product as sold by ID
DELETE /products/{id} - delete product

## Process

Products are parsed in chunks and insertion to the database uses transaction to speedup upload and parsing. 
There are 10000 items in the product list and import happens immediately. With the millions of products there is a sence to increase chunk size.
Key is `client_id` so even with lots of imports products will be updated if `client_id` is in list.
