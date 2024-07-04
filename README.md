# Vending Machine 

## Setup

### Prerequisites
- Docker

### Building the Docker Image
```bash
docker run -it vending_machine_app_v1
```

## Design

### Data

* products.csv: product info
-   product_id: Unique identifier for each product
-   product_name: Name of the product
-   price: Price of the product
-   stock: Number of units available
-   last_time_stock: Last time the product was stocked
* vending_machines.csv: info on vending machine
-   machine_id: Unique identifier for each vending machine
-   location: Location of the vending machine
-   last_maintenance_date: Last date the vending machine was maintained.
* inventory.csv: keep track of current product inventory
-   product_id: Unique identifier for each product
-   machine_id: Unique identifier for each vending machine
-   stock: Number of units available for each product
* sales.csv: keep track of sales
-   sale_id: Unique identifier for each sale
-   product_id: Unique identifier for the product sold
-   machine_id: Unique identifier for the vending machine for every sale
-   timestamp: Date and time of the sale
-   amount_paid: Amount of money paid by the user
-   change_notes: Cash notes available for repayment
* cash_reserve.csv: keep track of cash notes available in vending machine
-   note: Denomination of the note
-   count: Number of notes available
