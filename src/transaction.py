import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init(key="../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json"):
    """
    Initializes firestore
    @return: returns a tuple of collection objects representing the cart, inventory, and transaction collections
    """
    cred = credentials.Certificate(
        key)
    firebase_admin.initialize_app(cred)

    # App is an app object of sorts
    App = firebase_admin.initialize_app(cred, None, 'Cheqout Transaction')
    # Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
    Client = firebase_admin.firestore.client()

    # get a reference to the top level collection
    return Client.collection('carts'), Client.collection('inventory'), Client.collection('transaction')

def get_data(inventory, item):
    """
    Helper function that gets the unit price and tax of an item
    @param inventory: A Colelction object representing the item inventory
    @param item: The id of the item of request
    @return: A tuple containing the unit price of the item with the tax of the item
    """
    for document in inventory.get():
        if document.id == item:
            item_data = document.to_dict()
            return item_data
    return None

def store_transaction(carts, transactions, inventory, cart_id, user_id):
    """
    Processes and records a transaction from a carts' items
    @param carts: A Collection object representing the carts
    @param transactions: A Collection object representing the transactions
    @param inventory: A Colelction object representing the item inventory
    @param cart_id: The desired cart id to process the transaction with
    @param user_id: The id of the user that is making the transaction
    @return: A Boolean representing whether the transaction succeeded or not
    """
    item_array = None
    # First find the item array from the desired cart
    for document in carts.get():
        if document.id == cart_id:
            cart_data = document.to_dict()
            item_array = cart_data['items']
    if item_array is None:
        return False
    # Then start populating data for the transaction
    transaction_data = {"user": user_id, "cart": cart_id, "items": [], "subtotal": 0., "tax": 0., "total": 0.}
    for item in item_array:
        # TODO: handle case where item prace wasn't found
        if get_data(inventory, item['id']) is None:
            print("PRICE NOT FOUND")
        else:
            item_data = get_data(inventory, item['id'])
            transaction_data['subtotal'] += float(item_data['unit_price']) * item['quantity']
            # Add tax if the item is taxable
            if float(item_data['tax']) == 1:
                transaction_data['tax'] += float(item_data['unit_price']) * item['quantity'] * 0.13
            # process the item as a countable item
            if item_data['format'] == "0":
                transaction_data['items'].append(
                    {'id': item['id'], 'name': item_data['name'], 'qty': item['quantity'], 'unit_price':item_data['unit_price']})
            # process the item as a weighted item
            if item_data['format'] == "1":
                transaction_data['items'].append({'id': item['id'], 'name': item_data['name'], 'weight': item['quantity'], 'unit_price':item_data['unit_price']})
    transaction_data['total'] = transaction_data['subtotal'] + transaction_data['tax']
    # Add a timestamp
    transaction_data['timestamp'] = datetime.datetime.utcnow().strftime('%B %d, %Y, %H:%M:%S UTC').lstrip("0").replace(" 0", " ")
    # TODO: find ways to implement this data
    transaction_data['auth_code'] = 'TEST AUTH CODE'
    transaction_data['payment_type'] = -1
    transactions.add(transaction_data)
    print(transaction_data)

if __name__=="__main__":
    car, inv, tra = init()
    store_transaction(car, tra, inv, 'ULtXMhOuqcRHPpa2aKy1',
                      'womvkAsNMvAIdKpnW2h3')
