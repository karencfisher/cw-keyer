from keyer.sender.sender import Sender


s = Sender(10)
for c in 'HELLO':
    print(s.reverse_morse[c], end=' ')
print('')
