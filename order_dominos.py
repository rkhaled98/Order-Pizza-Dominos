from pizzapi import *
from collections import defaultdict

def FSM():
    state = defaultdict(lambda: defaultdict())
    state['begin'] = {'proceed': 'customer', 'exit': 'exit'}
    state['customer'] = {'redo':'customer','exit':'exit','proceed':'address_store'}
    state['address_store'] = {'redo':'address_store','exit':'exit','proceed':'items'}
    state['items']={'redo':'items','proceed':'card','alreadycard':'order','exit':'exit'}
    state['card']={'redo':'card','proceed':'order','exit':'exit'}
    state['order']={'nogooditems':'items','proceed':'placedorder','exit':'exit', 'card':'card'}
    state['placedorder']={}
    firstnamelastname,email,phone,addressline1,region,state_loc,zipcode=[""]*7
    card_number,card_exp,card_zip,card_pin = [""]*4
    customer,address,store,menu,order=[None]*5
    items_for_order = []
    
    current_state = 'begin'
    while current_state!='exit' and current_state!='placedorder':
        if current_state=='begin':
            userin = input("would you like to place a Domino's order? enter:{}".format(state[current_state].keys()))
            next_state = state[current_state][userin]
            print(next_state)
        if current_state == 'customer':
            firstnamelastname = input("what's your first name and last name?").split(" ")
            email = input("what's your email?")
            phone = input("what's your phone number?")
            userin = input("you have entered\nname:{}\nemail:{}\nphone:{}\n{}"\
                          .format(firstnamelastname,email,phone,state[current_state].keys()))
            if userin == 'proceed':
                customer = Customer(firstnamelastname[0],firstnamelastname[1],email,phone)
            next_state = state[current_state][userin]
        if current_state == 'address_store':
            addressline1 = input("enter address line 1")
            region = input("enter region")
            state_loc = input("enter state")
            zipcode = input("enter zipcode")
            address = Address(addressline1,region,state_loc,zipcode)
            store = address.closest_store()
            menu = store.get_menu()
            order = Order(store,customer,address)
            # The below line checks to see which state the user would like to go to after confirming information
            # possible states: redo info, go on to enter items, or exit
            userin = input("you have entered\naddress line 1:{}\nregion:{}\nstate:{}\nzipcode:{}\nstore:{}\n{}"\
                          .format(addressline1,region,state_loc,zipcode,store.get_details()['AddressDescription'],state[current_state].keys()))
            next_state = state[current_state][userin]
        if current_state == "items":
            state_items = defaultdict(lambda: defaultdict)
            current_state_items = 'search'
            state_items['search'] = {'add': 'add', 'exit':'exit','search':'search','remove':'remove', 'proceed':'card'}
            state_items['add'] = {'add': 'add', 'exit':'exit', 'search':'search', 'remove':'remove','proceed':'card'}
            state_items['remove'] = {'add': 'add', 'exit':'exit', 'search':'search', 'remove':'remove','proceed':'card'}
            while current_state_items != 'exit' and current_state_items != 'card':
                if current_state_items == 'search':
                    search_term = input("please enter a term to search the menu at this Domino's.")
                    menu.search(Name=search_term)
                    userin = input("make note of the ID of desired item.\n{}".format(state_items[current_state_items].keys()))
                    next_state_items = state_items[current_state_items][userin]
                if current_state_items == 'add':
                    add_key = input("please enter an ID to add, or type search to go back to search")
                    if add_key == "search":
                        next_state_items = 'search'
                    else:
                        try:
                            order.add_item(add_key)
                            userin = input("item successfully added.\
                             your current items are:\n{}.\n\
                             type add to add another or proceed\
                             to continue to payment info\n{}"\
                                           .format([x['Name'] for x in order.data['Products']],state_items[current_state_items].keys()))
                            next_state_items = state_items[current_state_items][userin]
                        except KeyError:
                            userin = input("error. type add to try again\n{}".format(state_items[current_state_items].keys()))
                            next_state_items = state_items[current_state_items][userin]
                if current_state_items == 'remove':
                    # do code here
                    pass
                current_state_items = next_state_items
            # if we have exited out of the items search/add/remove DFA with card, then we go to card.
            # if exit, then exit
            if current_state_items == 'card':
                next_state = 'card'
            elif current_state_items == 'exit':
                next_state = 'exit'
        if current_state == 'card':
            card_number = str(input("enter card number."))
            card_exp = str(input("enter card expiration date. format: MMYY"))
            card_pin = str(input("enter card security code."))
            card_zip = str(input("enter card zip code."))
            userin = input("you have entered\n\
            card number:{}\ncard exp:{}\ncard pin:{}\ncard zip:{}\n{}"\
                          .format(card_number,card_exp,card_pin,card_zip,state[current_state].keys()))
            next_state = state[current_state][userin]
        if current_state == 'order':
            userin = input("would you like to place your order?{}".format(state[current_state].keys()))
            if userin == "proceed":
                card_info = PaymentObject(card_number,card_exp,card_pin,card_zip)
                try:
                    order.pay_with(card_info)
                except Exception as e:
                    userin = input("there was an error{}\n{}".format(e,state[current_state].keys()))
            next_state = state[current_state][userin]
        if current_state == 'placedorder':
            print("congratulations. your order has been placed")
            next_state = 'exit'
                 
        current_state = next_state
    
    print("\nthank you")
        
def main():
    FSM()

if __name__ == "__main__":
    main()