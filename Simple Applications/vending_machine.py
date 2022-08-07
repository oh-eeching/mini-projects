# Edit Machine Profile
# Please create a txt file and change the name below accordingly when using this app
# Code is still in fine-tuning phase

def editMachineProfile():
    label = ['Slot ID:','Product ID:','Quantity:']  # assume these are the only parameters used in backend vending machines
    while True:
        try:
            machine_id = int(input("Please enter Machine ID: "))
            if machine_id <= 0:
                raise Exception
            break
        except ValueError:
            print("Please enter a valid integer!")
        except:
            print("Please enter a valid ID!")
            
    with open(master,"r") as master_file:
        master_lines = list(x.strip('\n').strip('\t') for x in master_file.readlines())
        s_master_lines = list(a.split(',') for a in master_lines)
        count = len(master_lines[0].split(',')) # check for columns
        all_machine_id = {int(elem[0]) for elem in master_lines} # use set get distinct id                                            
        lines = list(x.split(',') for x in filter(lambda x:str(machine_id) in x[0], master_lines))  # filters only those with correct machine id
        if machine_id in all_machine_id:
            print("Machine ID:",machine_id)
            for each in range(len(lines)):
                for i in range(count-1):      # assuming in the order of master.txt and qty is last column 
                    print(f"{label[i]} {lines[each][i+1]}") # skip machine id repeats
        else:
            print('This is a new machine.')
            menu = """
    Would you like to add a Slot ID and Product ID to the new machine?
    P: Proceed
    L: Quit
    """   
            new_machine_input = input(menu).upper().strip()
            while new_machine_input != 'L':
                if new_machine_input == 'P':
                    try:
                        p_input = int(input("Please enter the new Slot ID: "))
                    except:
                        print("Please enter a valid Slot ID!")
                        continue
                    p_product_input = input(f"Please enter a Product ID for Slot ID {p_input}: ").upper().strip()
                    with open(master,'a') as master_out:
                        master_out.write(f"\n{machine_id},{p_input},{p_product_input}")
                new_machine_input = input(menu).upper().strip()
                      
    menu2 = """
    What would you like to do next?
    A: Add New ID
    B: Edit/Delete ID
    C: Delete Entire Machine Profile
    E: View Current Machine Profile
    F: Quit
    """
    ans = input(menu2).strip().upper()
    while ans != 'F':
        with open(master,"r") as master_file:   # get updated version
            master_lines = list(x.strip('\n').strip('\t') for x in master_file.readlines())
            lines = list(x.split(',') for x in filter(lambda x:str(machine_id) in x[0], master_lines))
            slot_line = {int(lines[i][1]) for i in range(len(lines))}   
                
        if ans == 'A':
            try:
                x_input = int(input("Please enter the new Slot ID: "))
            except:
                print("Please enter a valid Slot ID!")
                continue
            if x_input in slot_line:
                print("This Slot ID already exists! Please select another!")
                continue
            x_product_input = input(f"Please enter a Product ID for Slot ID {x_input}: ").strip().upper()
            with open(master,'a') as master_out:
                master_out.write(f"\n{machine_id},{x_input},{x_product_input}")
            print(f'Slot ID {x_input} and Product ID {x_product_input} has been added to Machine Profile.')
                
        elif ans == 'B':    # can add or delete
            menu3 = f"""      
    What amendments would you like to do for Machine {machine_id}?     
    X: Remove Saved Slots
    Y: Edit Slot ID
    Z: Edit Product ID
    Q: Quit
    """      
            b_input = input(menu3).upper().strip()      # assuming that each slot will always have product
            while b_input != 'Q':
                with open(master,"r") as master_file:   # get updated version of file
                    master_lines = list(x.strip('\n').strip('\t') for x in master_file.readlines())
                    s_master_lines = list(a.split(',') for a in master_lines)   # to get in list form
                    lines = list(x.split(',') for x in filter(lambda x:str(machine_id) in x[0], master_lines))
                    slot_line = {int(lines[i][1]) for i in range(len(lines))}
                    
                if b_input == 'X':
                    try:
                        x_input = int(input("Please enter Slot ID to be removed: "))
                    except:
                        print("Please enter a valid Slot ID!")
                        continue
                    if x_input not in slot_line:
                        print("This Slot ID does not exist! Please select another")
                        continue
                    else:
                        to_retain = list(k for k in s_master_lines if k[1]!= str(x_input))        ##### double check
                        with open(master,'w') as master_out:
                            for i in to_retain:     # format nicely to write
                                j = ','.join(i)+'\n'
                                master_out.write(j)
                        print(f"Slot ID {x_input} has been removed.")
                
                elif b_input == 'Y':
                    try:
                        y_input = int(input("Please enter Slot ID to be edited: "))
                    except:
                        print("Please enter a valid Slot ID!")
                        continue
                    if y_input not in slot_line:
                        print("This Slot ID does not exist! Please select another!")
                        continue
                    try:
                        y_input_change = int(input(f"What should Slot ID {y_input} be changed to? "))   # change to...
                    except:
                        print("Please enter a valid Slot ID!")
                        continue
                    for each in s_master_lines:         # change the value of the element required
                        for i in range(len(each)):
                            if each[i] == str(y_input):
                                each[i] = str(y_input_change)
                    with open(master,'w') as master_out:
                        for i in s_master_lines:     
                            j = ','.join(i)+'\n'
                            master_out.write(j)
                    print(f"Slot ID {y_input} has been changed to {y_input_change}")

                elif b_input == 'Z':
                    try:
                        z_input = int(input("Please enter Slot ID which the desired Product ID is to be edited: "))  ### product line
                    except:
                        print("Please enter a valid Slot ID!")
                        continue
                    if z_input not in slot_line:
                        print("This Slot ID does not exist! Please select another!")
                        continue
                    for each in lines:      # get pos of element to be changed
                        if each[1] == str(z_input):
                            z_id = each[2]
                    z_input_change = input(f"Product ID is {z_id} for Slot ID {z_input}. What should it be changed to? ").strip().upper()
                    for each in s_master_lines:     # iterate and find the correct element to change
                        for i in range(len(each)):
                            if each[i] == str(z_id):
                                each[i] = str(z_input_change)
                    with open(master,'w') as master_out:
                        for i in s_master_lines:             
                            j = ','.join(i)+'\n'
                            master_out.write(j)
                    print(f"Product ID {z_input} has been changed to {z_input_change}")
                with open(master,"r") as master_file:   # get updated version
                    master_lines = list(x.strip('\n').strip('\t') for x in master_file.readlines())
                    s_master_lines = list(a.split(',') for a in master_lines)
                    lines = list(x.split(',') for x in filter(lambda x:str(machine_id) in x[0], master_lines))
                    slot_line = {int(lines[i][1]) for i in range(len(lines))}    
                b_input = input(menu3).upper().strip()
 
        elif ans == 'C':    # will ask before deleting entire profile
            c_input = input(f"Would you like to delete the entire profile of Machine {machine_id}? This is irreversible! [Y/N] ").upper().strip()
            if c_input == "Y":
                opp_lines = list(x.split(',') for x in filter(lambda x:str(machine_id) not in x[0], master_lines))
                with open(master,'w') as master_out:        
                    for i in opp_lines:
                        j = ','.join(i)+'\n'
                        master_out.write(j)
                print(f"Machine Profile for Machine ID {machine_id} has been deleted.")
            elif c_input == "N":
                print("Bringing you back to Menu...")
                pass
            else:
                print("Invalid input!")
                continue
        elif ans == 'E':
            print("Machine ID:",machine_id)
            for each in range(len(lines)):
                for i in range(count-1):      
                    print(f"{label[i]} {lines[each][i+1]}")
        else:
            print("Please provide one of the options above!")
        with open(master,"r") as master_file:   # get updated version of file
            master_lines = list(x.strip('\n').strip('\t') for x in master_file.readlines())
            lines = list(x.split(',') for x in filter(lambda x:str(machine_id) in x[0], master_lines))
            slot_line = {int(lines[i][1]) for i in range(len(lines))}                     
        ans = input(menu2).strip().upper()
    print("Exiting Editing Machine Profile Mode...")
        
if __name__ == "__main__":
    master = "machineProfile.txt"
    editMachineProfile()
