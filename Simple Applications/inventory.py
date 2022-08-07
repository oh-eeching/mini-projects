# Adding items to an inventory
# Inventory app

inventoryList = {}  # use a dictionary to track

def displayInventory(lst):
    if not lst:
        return None
    else:
        return lst

def addNewItemNQty(item,qty):
    global inventoryList
    if item in inventoryList:
        inventoryList['item'] += qty
    else:
        inventoryList.update({item:qty})
    return inventoryList

def removeItemNQty(item_remove,qty_remove):
    global inventoryList
    if item_remove in inventoryList:
        inventoryList[item_remove] -= qty_remove
        return inventoryList
    else: return None

def inventoryMenu():
    menu = '''
            << Inventory Menu>>
         A. Display all inventory
         B. Add new item and qty
         C. Remove item
         D. Exit
    '''
    print(menu)
    choice = input("Please select a choice from the above options: ").upper().strip()
    while choice != 'D':
        if choice == 'A':
            if displayInventory(inventoryList): 
                print('<<Your Inventory>>')
                for item in inventoryList:
                    print(f"{item} x{inventoryList[item]}")
            else:
                print('No items added yet')
                
        elif choice == 'B':
            print('Adding new item and item qty')
            item = input('Please enter item to add: ').strip().lower()
            try:
                qty = int(input('Please enter item qty to add: '))
            except:
                print('Please enter an integer!')
                continue
            addNewItemNQty(item,qty)
            print(f'{item} x {qty} has been added to your inventory.')
            
        elif choice == 'C':
            print('Removing qty for item')
            item_remove = input('Please enter item to remove: ').strip().lower()
            try:
                qty_remove = int(input('Please enter item qty to remove: '))
            except:
                print('Please enter an integer!')
                continue
            if not removeItemNQty(item_remove,qty_remove):
                print(f'{item_remove} does not exist!')
            else:
                print(f'{item} x {qty_remove} has been removed from your inventory.')
            
        else:
            print('Please input a valid option!')
            
        print(menu)
        choice = input("Please select a choice from the above options: ").upper().strip()
    print('Thank you for using inventoryMenu')
    print('Good Bye!')

if __name__ == "__main__":
    inventoryMenu()
