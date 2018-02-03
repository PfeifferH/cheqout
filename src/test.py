import client

if __name__=="__main__":
    # client api tests
    cart = client.init('2f3648db-8d1e-43ea-af2d-b8726fbd6bcf')
    client.activate(cart)
    client.add_item(cart, 'test_item')
    client.remove_item(cart, 'test_item')
    print(client.get_items(cart))
    client.deactivate(cart)