#Dustin Motes, Jeffrey Heckeroth, Carlos Beltran, Abraham Nacianceno
#May 30, 2012
#ITT104
#Mr. Herrin

#Defines the main function
def main():
    gas = 200
    ammo = 5
    print ('Welcome to Battlebots!')
    print ('Battlebot is starting up..')
    command(gas, ammo)

#Defines the command function
def command(gas, ammo):
    import time
    time.sleep (2)
    print ('Press 1 to move the bot')
    print ('Press 2 to fire the weapon')
    print ('Press 3 for status of the bot')
    print ('Press 4 to reboot the bot')
    print ('Press 5 to shutdown the bot')
    cmd = input ('enter your choice now: ')
    if cmd == '1':
        move(gas, ammo)
    elif cmd == '2':
        fire(gas, ammo)
    elif cmd == '3':
        status(gas, ammo)
    elif cmd == '4':
        reboot(gas, ammo)
    elif cmd == '5':
        shutdown(gas, ammo)
    else:
        print ('Please enter a valid command')
        command(gas, ammo)

## this function is to move the battle bot.

def move(gas, ammo):
    obstacle = 0
    if gas == 0:
        print ('I\'m out of gas, reboot for more gas.')
        command(gas, ammo)
    else:
        direction = input ('Type which direction you would like to move: Forward, Left, Backwards, Right: ')
        distance = input ('How far do you want to move?:  ')
        if int(distance) <= gas:
            print ('Enter 1 if an obstacle is in the way:  ')
            print ('Enter 2 if there is no obstacle:  ')
            obstacle = input ('Enter your choice now: ')
            if obstacle == 1:
                odDistance = input ('How far away is the obstacle?: ')
            
                if int(odDistance) >= int(distance):
                    gas = gas - int(distance)
                    print ('I moved', direction, distance)
                    print ('I have this much gas left:  ', gas)

                    command(gas, ammo)
                elif int(odDistance) < int(distance):
                    gas = gas - int(odDistance)
                    print ('I could only move', direction, odDistance)
                    print ('I have this much gas left:  ', gas)

                    command(gas, ammo)
            else:
                gas = gas - int(distance)
                print ('I moved', direction, distance)
                print ('I have this much gas left:  ', gas)
                command(gas, ammo)

        elif int(distance) > gas:
            print ('Error: I can\'t move that far!')
            command(gas, ammo)

    
#Commands for firing the battle bots weapon
def fire(gas, ammo):
    if ammo == 0:
        print ('Get me more ammo!  I\'m out! Reboot for more ammo.')
        command(gas, ammo)
    else:
        target = input ('How far away is the target?: ')
        ammo = ammo - 1
        if int(target) <= 20:
            print ('Target is destroyed!')
            print ('Ammo left', ammo)
            command(gas, ammo)
        elif int(target) <= 40:
            print ('Target is partially disabled')
            print ('Ammo left', ammo)
            command(gas, ammo)
        else:
            print ('You missed the target...:')
            print ('Ammo left', ammo)
            command(gas, ammo)

#Displays the status of the fuel, ammo
def status(gas, ammo):
    print ('Fuel:', gas)
    print ('Ammunition:', ammo)
    command(gas, ammo)
    
#Reboots the battlebot
def reboot(gas, ammo):
    rBoot = input ('Are you sure you want to reboot? Press 1 for yes, Press 2 for no: ')
    if rBoot == '1':
        import time
        print ('I am rebooting now...')
        time.sleep (3)
        main()
    elif rBoot == '2':
        import time
        print ('Aborting reboot..')
        time.sleep (3)
        command(gas, ammo)
        
#shuts down the battlebot
def shutdown(gas, ammo):
    shut = input ('Are you sure you want to shutdown? Press 1 for yes, Press 2 for no: ')
    if shut == '1':
        import time
        print ('I am shutting down now...')
        time.sleep (3)
        print ('Good night world')
        import sys
        sys.exit(1)
    elif shut == '2':
        command(gas, ammo)
    else:
        print ('Invalid command')
        command(gas, ammo)

main()
