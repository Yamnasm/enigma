import json

'''
todo:
1. function to generate new settings

future?:
- generate key list to an easily-read, exportable format
- gui with visible plugboard / rotors
- lose to the Allies
'''
def import_machine_settings():
    with open("machine-settings.json", "r") as file:
        data = json.load(file)
        return data
    
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
def reflect(char, reflector):
    for i, o in enumerate(reflector):
        if char in o:
            return reflector[not i][o.index(char)]

def plugswap(settings, char):
    for i, swap in enumerate(settings):
        if char in swap:
            return settings[i][not swap.index(char)]
    return char

def enigmize_char(char, rotorset, reflector):
    letter_index = ord97(char)

    rotor_letter1 = rotorset[0][letter_index]
    rotor_letter2 = rotorset[1][ord97(rotor_letter1)]
    rotor_letter3 = rotorset[2][ord97(rotor_letter2)]

    reflection = reflect(rotor_letter3, reflector)

    rotor_index3 = rotorset[2].index(reflection)
    rotor_index2 = rotorset[1].index(chr97(rotor_index3))
    rotor_index1 = rotorset[0].index(chr97(rotor_index2))

    return chr97(rotor_index1)

def encrypt(message, rotorset, reflector, plugsetting, rotorstart):
    encoded_message = ""
    for i, char in enumerate(message):
        prerotor_swap = plugswap(plugsetting, char)
        #this is messy and i hate it
        postrotor_swap = plugswap(plugsetting, enigmize_char(prerotor_swap, shift_rotor(rotorset, i + rotorstart), reflector))
        encoded_message += postrotor_swap
    return encoded_message

if __name__ == "__main__":
    refe = [chr(i) for i in range(97, 123)] + [" ", "."]
    settings = import_machine_settings()

    rl = settings["rotor_list"]
    ro = settings["rotor_order"]
    rotors = [rl[ro[i]] for i in range(len(ro))]

    re = settings["reflector"]
    reflector = [re[:len(re)//2], re[len(re)//2:]]

    pl = settings["plug_settings"]
    plugsetting = [pl[i:i+2] for i in range(0, len(pl), 2)]

    # example: "abc" which will mean "1 2 3", (first number = last rotor)
    # which is unmodulo'd as 843.
    rs = settings["rotor_start"]
    rotor_start = sum([(28 ** e) * i for e, i in enumerate([ord97(c) + 1 for c in rs[::-1]])])

    print(encrypt(sanitise(input()), rotors, reflector, plugsetting, rotor_start))