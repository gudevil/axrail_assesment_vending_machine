# Vending Machine 
![sample](/sample_run.PNG)
## Setup

- Adjust the value in inventory.csv (how much products available) & cash_reserve.csv (how much cash available for repayment) accordingly
- Products can be added in products.csv
- Make sure the files are in the same directory
  - Dockerfile
  - requirements.txt
  - vending_machine.py
  - products.csv
  - vending_machines.csv
  - inventory.csv
  - sales.csv
  - cash_reserve.csv
- Run the docker image or setup locally

### Prerequisites
- Docker

### Building the Docker Image
```bash
docker run -it vending_machine_app_v1
```

## Design
### App
Some key consideration when building this:
- User are displayed with the products available, price and unit available
- Making sure the transaction is for validated cash notes and repayment is done correctly
- In the backend, logging must be updated to the csv file for every succesful transactions


### Data
Data will be stored and pulled from csv file. I try to replicate the way I designed for a DB through this format (ideally I wanted to implement DB but didn't had enough time). 
The fields are some data that I think is relevant for a vending machine and would be useful.

  I also put a timestamp so that we can check for seasonality or whether if its possible to apply a time series model.

Below are the fields used:
* products.csv: product info
  * product_id: Unique identifier for each product
  * product_name: Name of the product
  * price: Price of the product
  * stock: Number of units available
  * last_time_stock: Last time the product was stocked
* vending_machines.csv: info on vending machine
  * machine_id: Unique identifier for each vending machine
  * location: Location of the vending machine
  * last_maintenance_date: Last date the vending machine was maintained.
* inventory.csv: keep track of current product inventory
  * product_id: Unique identifier for each product
  * machine_id: Unique identifier for each vending machine
  * stock: Number of units available for each product
* sales.csv: keep track of sales
  * sale_id: Unique identifier for each sale
  * product_id: Unique identifier for the product sold
  * machine_id: Unique identifier for the vending machine for every sale
  * timestamp: Date and time of the sale
  * amount_paid: Amount of money paid by the user
  * change_notes: Cash notes available for repayment
* cash_reserve.csv: keep track of cash notes available in vending machine
  * note: Denomination of the note
  * count: Number of notes available

Some other consideration that I did not get to implement is to include fields like:
- temperature
- time duration every time user try to purchase
- cancelled transaction

Where I believe we can further do EDA and if possible apply other ML models
