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

- products.csv: product info
-   product_id: Unique identifier for each product.
-   product_name: Name of the product.
-   price: Price of the product.
-   stock: Number of units available.
-   last_time_stock: Last time the product was stocked.
- vending_machines.csv: info on vending machine
- inventory.csv: keep track of current product inventory
- sales.csv: keep track of sales
- cash_reserve.csv: keep track of cash notes available in vending machine
