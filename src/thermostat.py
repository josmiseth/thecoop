
from gpiozero import Button

button = Button(21)

print(button.when_pressed)
print(button.when_released)

exit()
