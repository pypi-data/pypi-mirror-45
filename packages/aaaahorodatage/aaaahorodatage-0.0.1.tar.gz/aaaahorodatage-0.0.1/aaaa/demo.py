#!/usr/bin/env python3
# -*-coding:Utf-8 -*

#############################################
# As compliant as possible with the PEP8    #
# https://www.python.org/dev/peps/pep-0008/ #
#############################################

localusage = False
# localusage = True

if localusage:
    from ahordat import AaaaHorodatageTools
else:
    from aaaa.ahordat import AaaaHorodatageTools

# chemin = p.dirname(p.abspath(__file__)) + "/"


def input_entier(annonce=""):
    """Vérifie si une entrée est entière"""
    ok = False
    while not ok:
        try:
            entier = int(input(annonce))
            ok = True
            return entier
        except ValueError:
            print("An integer, please: ", end="")
            ok = False


def demo():

    print("+------+\n| DEMO |\n+------+\n")

    myDT = AaaaHorodatageTools()
    print("UTC local offset (seconds): ", myDT.get_utc_local_offset())
    print("UTC local offset (string):  ", myDT.get_utc_local_offset("string"))
    date_test = [2001, 1, 1, 1, 5, 0]
    print("Date test: ", date_test)
    myDT.encode(date_test)
    print("Encode date test (local tz):    ", myDT)
    print("Decode date test (string):      ", myDT.decode("string"))
    print("Decode date test (list):        ", myDT.decode("list"))
    print("Decode date test (dictionary):  ", myDT.decode("dictionary"))
    print("UTC timestamp offset (string):  ",
          myDT.get_utc_local_offset("string"))
    myDTutc = myDT.copy()
    myDTutc.tz2utc()
    print("Convert date test to UTC:       ", myDTutc, " = ", myDTutc.decode())
    myDTutc08 = myDTutc.copy()
    myDTutc08.utc2tz("+08:00")
    print("Now convert to UTC +08:00:      ", myDTutc08, " = ",
          myDTutc08.decode())

    rep = True
    while rep:
        print("+-----------------------------+")
        rep = input("| Press Enter to continue ... |")
        rep = False
    print("+-----------------------------+")

    # del myDTutc
    myDTutc = myDT.copy()
    myDTutc.encode(date_test, True)
    print("Encode date test (direct to UTC):      ", myDTutc)
    print("Decode date test (direct to UTC):      ",
          myDTutc.decode())
    myKb = AaaaHorodatageTools()
    myKb.encode()
    print("Here's the timestamp of your input:    ", myKb)
    print("Using self.ts of your input to decode: ", myKb.decode())
    print("I can also decode an other timestamp, with the same instance")
    print("without modify its self.ts:")
    print("Decode an other timestamp:          ", myDT, " = ",
          myKb.decode("string", myDT.get_ts()))
    print("Re-decode your input with self.ts:  ", myKb, " = ", myKb.decode())

    rep = True
    while rep:
        print("+-----------------------------+")
        rep = input("| Press Enter to continue ... |")
        rep = False
    print("+-----------------------------+")

    print("And now, let's see about the difference between 2 dates.")
    myDT.tz2utc()
    myDT.utc2tz("+08:00")
    myDT.convert2epoch(1900)
    print("I have encoded:                ", myDT.get_ts(), " - ",
          myDTutc08.decode())
    print("You have encoded:              ", myKb.get_ts(), " - ",
          myKb.decode())
    myKb.set_ts_same_epoch_offset(myDT)
    print("First, convert mine to +02:00  ", myDT.get_ts(), " - ",
          myDT.decode())
    print("And now, you minus me:         ",
          myDT.diffDays("string", myKb.get_ts()))
    print("Me minus you:                  ", myDT - myKb)
    myKbAdd = myKb.copy()
    print("Addition:                      ", myKbAdd.decode(), " + 1T01:10:20")
    myKbAdd + myKbAdd.dhms2seconds(1, 1, 10, 20)
    print("                             = ", myKbAdd.decode())
    myKbSub = myKb.copy()
    print("And substraction:              ", myKbSub.decode(), " - 1T01:10:20")
    myKbSub - myKbSub.dhms2seconds(1, 1, 10, 20)
    print("                             = ", myKbSub.decode())
    print("\nPlay attention to epoch ...")

    rep = True
    while rep:
        print("+-----------------------------+")
        rep = input("| Press Enter to continue ... |")
        rep = False
    print("+-----------------------------+")

    print("Get local epoch:                         ", myKb.get_epoch())
    myKb.set_epoch(1900)
    print("Set local epoch to 1900:                 ", myKb.get_epoch())
    print("Remember date test, epoch 2000:          ", myDT.get_ts(), " = ",
          myDT.decode())
    myDT1900 = AaaaHorodatageTools()
    myDT1900.encode(date_test)
    print("Encoding with epoch 1900:                ", myDT1900.get_ts(),
          " = ", myDT1900.decode())
    myDT1900.set_epoch(2000)
    print("Reset epoch to 2000:                     ", myDT1900.get_epoch())
    print("Get current embedded epoch of date test: ", myDT1900.get_ts_epoch())
    myDT2000 = myDT1900.copy()
    myDT2000.convert2epoch(2000)
    print("Re-convert date test to epoch 2000:      ", myDT2000.get_ts(),
          " = ", myDT2000.decode())

    rep = True
    while rep:
        print("+-----------------------------+")
        rep = input("| Press Enter to continue ... |")
        rep = False
    print("+-----------------------------+")

    print("Comparison operators")
    print(myDT.decode(), " == ", myKb.decode(), ": ", myDT == myKb)
    print(myDT.decode(), " != ", myKb.decode(), ": ", myDT != myKb)
    print(myDT.decode(), " <  ", myKb.decode(), ": ", myDT < myKb)
    print(myDT.decode(), " <= ", myKb.decode(), ": ", myDT <= myKb)
    print(myDT.decode(), " >  ", myKb.decode(), ": ", myDT > myKb)
    print(myDT.decode(), " >= ", myKb.decode(), ": ", myDT >= myKb)
    print("(", myDT.decode(), " + 10T01:10:20) >  ", myKb.decode(), ": ",
          (myDT + myDT.dhms2seconds(10, 1, 10, 20)) > myKb)

    rep = True
    while rep:
        print("+-----------------------------+")
        rep = input("| Press Enter to continue ... |")
        rep = False
    print("+-----------------------------+")

    print("Conversion Aaaa timestamps <> Posix timestamp")
    myDT1900.convert2epoch(1900)
    myDT1900.tz2utc()
    print("Remember date test set above to tz UTC and")
    print("                        ", myDT1900, " = ",
          myDT1900.decode())
    print("I can convert it to a posix timestamp, because it's UTC")
    myPosix = myDT1900.convert_aaaa2posix()
    print("Its posix timestamp is: ", str(myPosix))
    print("You can verify it on http://www.unixtime.fr/, choosing UTC time.")
    print("My date is unchanged:   ", myDT1900, " = ",
          myDT1900.decode())
    myDT1900.convert_posix2aaaa(myPosix)
    print("And now, I reconvert    ", str(myPosix), " to a Aaaa timestamp ")
    print("with epoch unix = 1970  ", myDT1900, " = ", myDT1900.decode())

    print()
    s = AaaaHorodatageTools("server")
    print("NB: you can get UTC local time with <new> =\
 AaaaHorodatageTools('server')")
    print("Example:                ", s.get_ts(), " = ", s.decode())

    print("\n+-------------+\n| Goodbye ... |\n+-------------+\n")


if __name__ == '__main__':
    demo()
    pass
