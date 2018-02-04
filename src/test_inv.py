from src import inventory

if __name__=="__main__":
    # inventory tests
    inv = inventory.init(
        "keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json")
    print(inventory.get_item_data(inv, 'ID I GUESS'))
    inventory.add_item_data(inv, 'another item id', {'name': 'other item I guess'})

    print("+== Type 'HELP' for help ==+")
    while True:
        inp = input("Command: ")
        if inp[:4].lower() == 'help':
            print("QUIT: \t quit application")
            print("ADD \t add item")
        if inp[:4].lower() == 'quit':
            print("exiting...")
            break
        if inp[:3].lower() == 'add':
            item_data = {}
            print("Enter the name of the item: ", end="")
            item_data['name'] = input()
            print("Enter the format of the new item")
            print("0: ITEM")
            print("1: BULK")
            item_data['format'] = input("Format: ")
            print("Enter the unit price of this item: " , end="")
            item_data['unit_price'] = input()
            print("Enter the tax of this item: ", end="")
            item_data['tax'] = input()
            print("Enter the id of the item: ", end="")
            item_id = input()
            inventory.add_item_data(inv, item_id, item_data)
