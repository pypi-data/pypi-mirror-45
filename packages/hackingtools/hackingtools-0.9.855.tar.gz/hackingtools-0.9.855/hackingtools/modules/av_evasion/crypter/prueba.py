import ht_crypter

crypter = ht_crypter.StartModule()
print(crypter.getRandomKeypair(200))
ht_crypter.Logger.saveLog()