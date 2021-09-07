import json

'''
todo: 
1. make settings files import.
2. function to generate new settings

future?:
- generate key list to an easily-read, exportable format
- gui with visible plugboard / rotors
- lose to the Allies
'''

rot1 = ("m", "p", "y", "u", "s", "e", "l", "c", "n", " ", "w", "z", "r", "k", "i", "t", "j", "d", "o", "b", "h", "x", "f", "q", "g", ".", "a", "v")
rot2 = ("i", "b", "r", "g", ".", "f", "w", "x", "q", "n", "z", "o", "u", "e", "d", "t", "p", "a", " ", "k", "c", "s", "h", "v", "j", "m", "y", "l")
rot3 = ("t", "c", " ", "a", "d", "h", "y", "o", "e", "k", "b", "p", "f", "m", "j", "u", "r", "v", "z", "w", ".", "s", "i", "q", "n", "l", "g", "x")

#our alphabet table used as a reference
refe = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".")

reflector = ["abcdefghijklmn", "opqrstuvwxyz ."]

def sanitise(s):
    return "".join([i for i in s.lower() if i in refe])

def ord97(letter):
    #return ord(letter) - 97
    return refe.index(letter)

def chr97(number):
    #return chr(number + 97)
    return refe[number]

def shift_rotor(rotorset, shift): #garbage function for garbage people
    LEN_OF_ROT = 28 # will change according to alphabet that we use.
    rotorshift = []
    #make this For-looped for infinite rotoring
    rotorshift.append(shift % LEN_OF_ROT)
    rotorshift.append((shift // LEN_OF_ROT) % LEN_OF_ROT)
    rotorshift.append(((shift // LEN_OF_ROT) // LEN_OF_ROT) % LEN_OF_ROT) #weird

    live_rotor1 = rotorset[0][rotorshift[0]:] + rotorset[0][:rotorshift[0]]
    live_rotor2 = rotorset[1][rotorshift[1]:] + rotorset[1][:rotorshift[1]]
    live_rotor3 = rotorset[2][rotorshift[2]:] + rotorset[2][:rotorshift[2]]
    
    return (live_rotor1, live_rotor2, live_rotor3)

''' The following 2 functions are similar, but represent 2
very different features of the military enigma.'''
def reflect(char):
    for i, o in enumerate(reflector):
        if char in o:
            return reflector[not i][o.index(char)]

def plugswap(settings, char):
    for i, swap in enumerate(settings):
        if char in swap:
            return settings[i][not swap.index(char)]
    return char #allows for optional plugs

def enigmize_char(char, rotorset):
    letter_index = ord97(char)

    rotor_letter1 = rotorset[0][letter_index]
    rotor_letter2 = rotorset[1][ord97(rotor_letter1)]
    rotor_letter3 = rotorset[2][ord97(rotor_letter2)]

    reflection = reflect(rotor_letter3)

    rotor_index3 = rotorset[2].index(reflection)
    rotor_index2 = rotorset[1].index(chr97(rotor_index3))
    rotor_index1 = rotorset[0].index(chr97(rotor_index2))

    return chr97(rotor_index1)

def encrypt(message, rotorset, plugsetting, rotorstart):
    encoded_message = ""
    for i, char in enumerate(message):
        prerotor_swap = plugswap(plugsetting, char)
        postrotor_swap = plugswap(plugsetting, enigmize_char(prerotor_swap, shift_rotor(rotorset, i + rotorstart)))
        encoded_message += postrotor_swap
    return encoded_message

plugsetting = ("ab", "cd", "ef", "gh", "ij", "kl", "mn", "op", "qr", "st", "uv", "wx", "yz", " .")
print(encrypt(sanitise(input()), (rot1, rot2, rot3), plugsetting, 0))