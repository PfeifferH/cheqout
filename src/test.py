import client

if __name__=="__main__":
    cart = client.init('2f3648db-8d1e-43ea-af2d-b8726fbd6bcf')
    client.activate(cart)
    client.deactivate(cart)
