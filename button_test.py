from shields import button_buzzer_shield

b = button_buzzer_shield.Button_Buzzer_Shield()

count = 0

while True:
    if b.button1_pressed():
        count -= 1
    if b.button2_pressed():
        count += 1
    print(count)