import ht_crypter
from colorama import Fore, Back, Style

ht_crypter.Logger.setDebugModule()
crypter = ht_crypter.StartModule()
print(crypter.getRandomKeypair(200))
ht_crypter.Logger.saveLog()
ht_crypter.Logger.printMessage('hola', 'esta es la descripcion del mensaje')
ht_crypter.Logger.printMessage('holaaaaa', 'esta es la descripcion del sddssdsds')
ht_crypter.Logger.printMessage('holdffdfda', 'esta es la descripcion del sddssdsds')