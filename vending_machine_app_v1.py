# latest version v2 - last check at 11pm 20240709

import csv
from datetime import datetime

# file paths, please check your file paths, assuming its in same dir
products_file = 'products.csv'
vending_machines_file = 'vending_machines.csv'
inventory_file = 'inventory.csv'
sales_file = 'sales.csv'
cash_reserve_file = 'cash_reserve.csv'

# initialise values for products
def initialize_products():
    products = {}
    with open(products_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products[row['product_name'].lower().replace('_',' ')] = {
                'product_id': row['product_id'],
                'price': row['price'],
                'last_time_stock': row['last_time_stock']
            }
    # print(products)
    return products

# initialise values for the inventory
def initialize_inventory():
    inventory = {}
    with open(inventory_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory[row['product_id']] = {
                'machine_id': row['machine_id'],
                'stock': int(row['stock'])
            }
    return inventory

# update inventory, writes the updated inventory into the csv
def save_inventory(inventory):
    with open(inventory_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['product_id', 'machine_id', 'stock'])
        for product_id, details in inventory.items():
            writer.writerow([product_id, details['machine_id'], details['stock']])

# initialise values for the cash reserve
def initialize_cash_reserve():
    cash_reserve = {}
    with open(cash_reserve_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cash_reserve[int(row['note'])] = int(row['count'])
    return cash_reserve

# update cash reserve, writes the updated cash reserve into the csv
def save_cash_reserve(cash_reserve):
    with open(cash_reserve_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['note', 'count'])
        for note, count in cash_reserve.items():
            writer.writerow([note, count])

# sales logging, writes the log into the csv
def log_sale(product_id, amount_paid, change_notes):
    with open(sales_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([len(open(sales_file).readlines()), product_id, 'VM001', datetime.now(), amount_paid, change_notes])

# calculate change and check if cash reserve is enough
def calculate_change(amount_paid, item_price, cash_reserve):
    notes = [100, 50, 20, 10, 5, 1]
    change = amount_paid - item_price
    change_notes = {}
    ori_change = change # keep track of original change to be paid before calculation starts
    # calculation to repay user based on correct notes
    for note in notes:
        if change == 0: # break loop if amount is enough
            break
        if cash_reserve[note] > 0: # check if cash reserve is above 0, if not skip to the next note
            count, remainder = divmod(change, note)
            if count > 0:
                if cash_reserve[note] >= count:
                    change_notes[note] = count # number of notes used
                    cash_reserve[note] -= count # get remainder change to be paid
                    change = remainder
                else: #
                    change_notes[note] = cash_reserve[note]
                    change -= (count - cash_reserve[note]) * note # get any amount in reserve to repay, get remainder change to be paid
                    cash_reserve[note] = 0 
        else:
            pass # skip because no cash reserve
    
    # last check, making sure the repayment is correct
    total_change_given = sum(note * count for note, count in change_notes.items())
    if total_change_given != ori_change:
        return None, cash_reserve

    return change_notes, cash_reserve


# validate the item, return true if its item is valid and within the product dict keys
def check_item(product_name,products):
    product_name = product_name
    if product_name not in products.keys(): # check if its in the keys in products dict
        return False
    else:
        return True
        
# check if the cash notes user inserted is valid, it must be a multiple of the ringgit notes
def check_cash_notes(amount_paid): # return true if its okay
    if amount_paid not in [1,5,10,20,50,100]: # check if its a multiple within the list
        print('Machine can only accept RM1, RM5, RM20, RM50, RM100 notes')
        return False
    else:
        return True

# function to process transaction
def transaction_process(product_name, amount_paid, products, inventory, cash_reserve):
    # initialise the variables 
    product_name = product_name.lower().replace('_',' ').strip() # standardise the string so that can be looked up
    product = products[product_name]
    product_id = product['product_id']
    item_price = int(product['price'])
    inventory_item = inventory[product_id]

    change_notes, updated_cash_reserve = calculate_change(amount_paid, item_price, cash_reserve)
    if change_notes is None:
        return "Not enough change available, your cash is returned"

    # update stock
    inventory_item['stock'] -= 1
    save_inventory(inventory)

    # update cash reserve
    if amount_paid in updated_cash_reserve:
        updated_cash_reserve[amount_paid] += 1
    else:
        updated_cash_reserve[amount_paid] = 1
    save_cash_reserve(updated_cash_reserve)

    # Log the sale
    log_sale(product_id, amount_paid, change_notes)
    dispensed_change_notes = ', '.join([f'RM{note} x {count}' for note, count in change_notes.items()])
    return f"Dispensed {product_name.upper()}.\n Change: {dispensed_change_notes} \n Thank you, come again :) \n.....\n.....\n....."

# to display the items by product name, price, how much is in stock
def display_items(products, inventory):
    display = ""
    counter=0
    for product_name, details in products.items():
        product_id = details['product_id']
        stock = inventory[product_id]['stock']
        display += f"| {product_name.upper()} RM{details['price']} [{stock}] | " # append strings to display item and price
        if counter ==4: # limit only to 4 columns of string
            display += f"\n"
        counter+=1
    return display

# controlling main functions 
def vending_machine():
    print('Machine starting... \n*ctrl+C to quit the machine*\n......\n......\n......')
    while True:
        products = initialize_products() 
        inventory = initialize_inventory()
        cash_reserve = initialize_cash_reserve()
        print(display_items(products, inventory))
        
        # name check, loop until valid product available
        while True:
            product_name = input("Select an item: ").lower().replace('_',' ').strip()
            if check_item(product_name,products): # check if item is valid and get the amount
                product = products[product_name]
                product_id = product['product_id']
                item_price = int(product['price'])
                inventory_item = inventory[product_id]
                if inventory_item['stock'] <= 0: # check for stock for the item
                    print("Item out of stock, please choose again") # loop again if product not in stock
                else:
                    break
            else:
                print('Invalid product name, please try again')
                
        # payment note validatiion, loop until cash is enough
        amount_paid = 0
        while True: # loop the cash insert from user until it exceed the amount they need to pay
            try:
                inserted_cash = int(input("Insert amount (in RM): ").strip())
            except ValueError:
                 print("'Machine can only accept money (integer value)'") # if input is non int value
            if check_cash_notes(inserted_cash): # call the function that returns true if the cash is valid for checking purposes
                amount_paid += inserted_cash # user can insert cash until its enough
                print(f"Total inserted: RM{amount_paid}")
                if amount_paid < item_price:
                    print('Insert more cash')
                else:
                    break
        
        result = transaction_process(product_name, amount_paid, products, inventory, cash_reserve)
        print(result)

# running the app
if __name__ == "__main__":
    vending_machine()
