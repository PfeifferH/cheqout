from client import Client

if __name__=="__main__":
    # cart = client.init()
    cart = Client()
    # client.activate(cart)
    cart.activate()
    # client.add_item(cart, 'test_item')
    cart.add_item('item id')
    # client.remove_item(cart, 'test_item')
    cart.remove_item('item id')
    # print(client.get_items(cart))
    print(cart.get_items())
    # client.complete(cart)
    cart.complete()
    # client.deactivate(cart)
    cart.deactivate()

