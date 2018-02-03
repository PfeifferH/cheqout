import client

if __name__=="__main__":
    # client api tests
    cart = client.init()
    client.activate(cart)
    client.add_item(cart, 'test_item')
    client.remove_item(cart, 'test_item')
    print(client.get_items(cart))
    client.complete(cart)
    client.deactivate(cart)
