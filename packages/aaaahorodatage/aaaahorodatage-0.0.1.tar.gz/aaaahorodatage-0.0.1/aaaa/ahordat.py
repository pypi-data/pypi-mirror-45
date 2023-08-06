#!/usr/bin/env python3
# -*-coding:Utf-8 -*


#########################################
# GNU General Public License, version 3 #
############################################################################
#                                                                          #
#    This program is free software: you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation, either version 3 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#                                                                          #
#    Robert Sebille, Belgium, 2018 -                                       #
#                                                                          #
############################################################################
# As compliant as possible with the PEP8    #
# https://www.python.org/dev/peps/pep-0008/ #
#############################################

import sys
import math
import time
import os.path as p


class AaaaHorodatage:

    """
    Encoding and decoding module for timestamps of AaaaHorodatage class.

    Timestamp format = [0-9]+AAAAZ+/-HH:MM where [0-9]+ = the number of
    seconds from the epoch until the date entered, AAAA = the epoch of
    the timestamp, and Z+/-HH:MM the UTC offset (e.g for CEST,
    summertime: Z+02:00). The timezone and epoch are embedded.

    Class attribute(s)
    - epoch: class reference year of the timestamp (only for encoding).
    Range: 1000 <= epoch <= 9999. Default 2000.

    Several ranges and keyboard input are managed, but not exceptions.
    """

    # année de référence (attribut de classe)
    epoch = 2000
    # Europe/Brussels summertime
    utc_local_offset = 7200

    def __init__(self, ts=""):
        # protected
        # Liste nombre de jours par mois, moins décembre et année non
        # bissextile
        self._ljm = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        self._nb_sec_par_jour = 86400
        # public
        if ts == "":
            self.ts = self.encode((self.get_epoch(), 1, 1, 0, 0, 0))
        if ts == "server":
            self.ts = str(math.trunc(time.time())) + "1970Z+00:00"

    # protected #
    # attributs
    def _get_ljm(self, i):
        return self._ljm[i]

    ljm = property(_get_ljm)

    def _get_nb_sec_par_jour(self):
        return self._nb_sec_par_jour

    get_nb_sec_par_jour = property(_get_nb_sec_par_jour)

    # méthodes
    def _offset_seconds2string(self, offset_seconds=0):
        if offset_seconds < -43200 or offset_seconds > +50400:
            print("Fatal error 2: offset_seconds not in range -43200 ", end="")
            print(">= offset_seconds <= +50400 in ", end="")
            print("_offset_seconds2string(offset_seconds)")
            sys.exit(2)
        chaineoffset = "+"
        if offset_seconds < 0:
            chaineoffset = "-"
        abs_offset_seconds = math.fabs(offset_seconds)
        heures = int(abs_offset_seconds / (60 * 60))
        minutes = int((abs_offset_seconds % 3600) / 60)
        if heures < 10:
            chaineoffset += "0"
        chaineoffset += str(heures) + ":"
        if minutes < 10:
            chaineoffset += "0"
        chaineoffset += str(minutes)
        return chaineoffset

    def _offset_string2seconds(self, offset_string="+00:00"):
        tmp = offset_string.split(":")
        retour = int(tmp[0]) * 3600
        if retour > 0:
            retour += int(tmp[1]) * 60
        else:
            retour -= int(tmp[1]) * 60
        return retour

    def _bissextile(self, an=0):
        b = 0
        if an % 400 == 0 or (an % 4 == 0 and not(an % 100 == 0)):
            b = 1
        return b

    def _input_entier(self, annonce=""):
        """Vérifie si une entrée est entière"""
        ok = False
        while not ok:
            try:
                entier = int(input(annonce))
                ok = True
                return entier
            except ValueError:
                print("I want an integer, please: ", end="")
                ok = False

    def _calcul_encode(self, annee, mois, jour, heures, minutes, secondes,
                       utc):
        """Encode the timestamp."""
        # ts = horodatage
        ts = secondes
        ts += minutes * 60
        ts += heures * 60 * 60

        # calcul du nombre de secondes de l'année en cours et ajout à ts
        i = 0
        tmp = 0
        while i < (mois - 1):
            tmp += self._get_ljm(i)
            if i == 1:
                tmp += self._bissextile(annee)
#           print (i, " ljm ", self._get_ljm(i), " tmp ", tmp)
            i += 1
        tmp += jour - 1
        # print (" tmp ", tmp)
        ts += tmp * self._get_nb_sec_par_jour()

        # calcul des secondes depuis epoch et ajout à ts
        i = self.get_epoch()
        tmp = 0
        while i < (annee):
            tmp += 365 + self._bissextile(i)
#          print (i, " tmp ", tmp, " j ", (365 + self.bissextile(i)))
            i += 1

        ts += tmp * self._get_nb_sec_par_jour()

        # On sauve l'epoch dans les 4 derniers chiffres du ts
        ts = (ts * 10000) + self.get_epoch()

        # On ajoute l'offset UTC (local ou Z) sous forme de chaine
        self.ts = str(ts) + "Z" + self.get_utc_local_offset("string")
        if utc:
            self.tz2utc()

#       print (annee, " bissextile = ", self.bis)
#       print (self.ts, " est l'horodatage pour le ", self.jour, "/", \
#       self.mois, "/", self.annee, \
#       " à ", self.heures, ":", self.minutes, ":", self.secondes, sep = "")

        return self.ts

    def _calcul_decode(self, typ, ts):
        """Decode the timestamp."""
        # Récupération tz, epoch, ts
        offset = ts.split("Z")
        ts = int(offset[0])
        offset = str(offset[1])
        # Récupération de l'époque
        epoch = ts % 10000
        # Récupération du ts en seconde
        ts = int(ts / 10000)

        # On retire les secondes de epoch à annee - 1
        # (on en n'a pas besoin pour calculer mois et jour)
        i = 0
        vrai = 1
        while vrai == 1:
            annee = epoch + i
            compare = (self._get_nb_sec_par_jour() * 365) +\
                      (self._get_nb_sec_par_jour() *
                       self._bissextile(annee))
            # print("t1 ", compare, " ts ", ts, " an ", annee, " v ",
            #      vrai)
            if compare < ts:
                ts -= compare
                i += 1
            else:
                vrai = 0
            # print("t2 ", compare, " ts ", ts, " an ", annee, " v ",
            #      vrai)
        # input("test ")

        # On retrouve secondes, minutes et heures
        secondes = ts % 60
        minutes = int((ts / 60) % 60)
        heures = int((ts / (60 * 60)) % 24)

        # on a retiré les secondes des années précédentes depuis epoch,
        # donc on récupère le n° du jour dans l'année (-1)
        jour = int(ts / self._get_nb_sec_par_jour())
        # on sépare mois et jour
        i = 0
        tmp = self._get_ljm(0)
        mois = 1
        while jour >= tmp:
            jour -= tmp
            i += 1
            tmp = self._get_ljm(i)
            if i == 1:
                tmp += self._bissextile(annee)
            mois += 1
            # print("i " + str(i) + " j " + str(jour) +\
            #       " t " + str(tmp))
        jour += 1

        # on gère le type de retour demandé
        if typ == "string":
            if mois < 10:
                str_mois = "0" + str(mois)
            else:
                str_mois = str(mois)
            if jour < 10:
                str_jour = "0" + str(jour)
            else:
                str_jour = str(jour)
            if heures < 10:
                str_heures = "0" + str(heures)
            else:
                str_heures = str(heures)
            if minutes < 10:
                str_minutes = "0" + str(minutes)
            else:
                str_minutes = str(minutes)
            if secondes < 10:
                str_secondes = "0" + str(secondes)
            else:
                str_secondes = str(secondes)
            retour = str(annee) + "-" + str_mois + "-" + str_jour + "T" +\
                str_heures + ":" + str_minutes + ":" +\
                str_secondes + offset
        if typ == "list":
            retour = list()
            retour.append(annee)
            retour.append(mois)
            retour.append(jour)
            retour.append(heures)
            retour.append(minutes)
            retour.append(secondes)
            retour.append(offset)
        if typ == "dict" or typ == "dictionary":
            retour = dict()
            retour["year"] = annee
            retour["month"] = mois
            retour["day"] = jour
            retour["hour"] = heures
            retour["minutes"] = minutes
            retour["seconds"] = secondes
            retour["UTC"] = offset

        return retour

    # méthodes publiques #
    # classe (cls)
    def get_epoch(cls):
        """Return the current epoch of the AaaaHorodatage class."""
        return cls.epoch

    get_epoch = classmethod(get_epoch)

    def set_epoch(cls, num):
        """Set the epoch of the AaaaHorodatage class.

        Range: 1000 <= epoch <= 9999. Default 2000.
        epoch class attribute is only for encoding.
        For decoding, the timestamps embed their own
        epoch.

        """
        if num >= 1000 and num < 10000:
            cls.epoch = int(num)
        else:
            print("Error: set_epoch(1000 ... 9999) = ", str(num), ". ",
                  "epoch now set to previous: ", cls.epoch, ".", sep="")

    set_epoch = classmethod(set_epoch)

    def set_utc_local_offset(cls, *offset):
        """Set the local UTC offset.

        Avalaible inputs:
        - Number of seconds (-43200 >= *offset <= +50400)
        - String (+/-HH:MM) ("-12:00" >= *offset <= "+14:00")

        update self.utc_local_offset, but !!! NOT self.ts !!!
        To update self.ts with the self.new utc_local_offset,
        you must re-encode the date
        """

        if len(offset) < 1:
            print("Fatal error 4: missing *offset argument in ", end="")
            print("set_utc_local_offset(*offset).")
            sys.exit(4)
        if not isinstance(offset[0], int) and not isinstance(offset[0], str):
            print("Fatal error 5: *offset must be a string ", end="")
            print("or an integer in set_utc_local_offset(*offset).")
            sys.exit(5)
        offset_candidate = offset[0]
        if isinstance(offset[0], str):
            offset_candidate = self._offset_string2seconds(offset[0])
        if offset_candidate < -43200 or offset_candidate > +50400:
            print("Fatal error 6: *offset out of range in ", end="")
            print("set_utc_local_offset(*offset).")
            print(" -43200 >= *offset <= +50400")
            print("or '-12:00' >= *offset <= '+14:00'.")
            sys.exit(6)
        cls.utc_local_offset = offset_candidate

    set_utc_local_offset = classmethod(set_utc_local_offset)

    # instance (self)
    def get_utc_local_offset(self, typ=""):
        """Get the local UTC offset set by the
        set_utc_local_offset method.

        Return:
        - Number of seconds (default)
        - String (+/-HH:MM) if typ = "string"

        """
        retour = self.utc_local_offset
        if typ == "string":
            retour = self._offset_seconds2string(self.utc_local_offset)
        return retour

    def get_ts(self):
        """Return the current timestamp"""
        return self.ts

    def get_ts_epoch(self):
        """Return the epoch of the timestamp

        Don't confuse with the class attribute epoch
        you can get or set with class methods
        get_epoch() and set_epoch(num)
        """
        retour = self.ts.split("Z")
        retour = int(retour[0])
        retour = int(retour % 10000)
        return retour

    def encode(self, d="", utc=False):
        """Request input of seconds, minutes, hour, year, month
            and day and return an AaaaHorodatage class timestamp.

            d =
            - "" or none: keyboard input.
            - list or tuple input, (fixed order): year, month, day,
            hour, minutes, seconds.
            - dict (any order, e.g.):
            seconds: minutes: hour: year: month: day:

            Ranges: seconds, minutes: 0-59. hour: 0-23.
            year: >= epoch, month: 1-12, day: 1-28/29/30/31,
            exact for the month.
            NB: encode year > 9999 with en epoch = 1000
            can causes long calculations.

            self.ts will be updated.

            utc: True, UTC timezone (default) | False, local timezone

        """
        annee = -1
        mois = -1
        jour = -1
        heures = -1
        minutes = -1
        secondes = -1
        utc = utc

        # list or tupples
        if isinstance(d, list) or isinstance(d, tuple):
            annee = d[0]
            mois = d[1]
            jour = d[2]
            heures = d[3]
            minutes = d[4]
            secondes = d[5]

        # dict
        if isinstance(d, dict):
            annee = d["year"]
            mois = d["month"]
            jour = d["day"]
            heures = d["hour"]
            minutes = d["minutes"]
            secondes = d["seconds"]

        # on vérifie les plages des entrées listes, tuples, dictionnaires
        if isinstance(d, list) or isinstance(d, tuple) or isinstance(d, dict):
            erreur = ""
            # if self.annee < self.get_epoch() or self.annee > 9999:
            if annee < self.get_epoch():
                erreur = "Fatal error 3, year = " + str(annee) +\
                         ". It must be [>= " + str(self.get_epoch()) +\
                         ", integer] in encode."
            if mois < 1 or mois > 12:
                erreur = "Fatal error 3, month = " + str(mois) + \
                         ". It must be [1-12, integer] in encode."
            nb_jours = self._get_ljm(mois - 1)
            if mois == 2:
                nb_jours += self._bissextile(annee)
            if jour < 1 or jour > nb_jours:
                erreur = "Fatal error 3, day = " + str(jour) + ". For " +\
                         str(mois) + "/" + str(annee) + ", day must be [1-" +\
                         str(nb_jours) + ", integer] in encode."

            if heures < 0 or heures > 23:
                self.erreur = "Fatal error 3, hour = " + str(heures) + \
                              ". It must be between [0-23, integer] in encode."
            if minutes < 0 or minutes > 59:
                erreur = "Fatal error 3, minutes = " + str(minutes) +\
                         ". It must be between [0-59, integer] in encode."
            if secondes < 0 or secondes > 59:
                erreur = "Fatal error 3, seconds = " + str(secondes)\
                    + ". It must be between [0-59, integer] in encode."

            if erreur != "":
                print(erreur)
                sys.exit(3)

        # keyboard
        if d == "":
            print("Coding a timestamp from the keyboard:")
            annonce = "Year [>= " + str(self.get_epoch()) + ", integer]: "
            # while annee < self.get_epoch() or annee > 9999:
            while annee < self.get_epoch():
                print(annonce, end="")
                annee = self._input_entier()
                # annee = int(input(annonce))
            while (mois < 1 or mois > 12):
                print("Month [1-12, integer]: ", end="")
                mois = self._input_entier()
            nb_jours = self._get_ljm(mois - 1)
            if mois == 2:
                nb_jours += self._bissextile(annee)
            while jour < 1 or jour > nb_jours:
                print("Day [1-" + str(nb_jours) + ", integer]: ", end="")
                jour = self._input_entier()
            while heures < 0 or heures > 23:
                print("Hour [0-23, integer]: ", end="")
                heures = self._input_entier()
            while minutes < 0 or minutes > 59:
                print("Minutes [0-59, integer]: ", end="")
                minutes = self._input_entier()
            while secondes < 0 or secondes > 59:
                print("Seconds [0-59, integer]: ", end="")
                secondes = self._input_entier()

        return self._calcul_encode(annee, mois, jour, heures, minutes,
                                   secondes, utc)

    def decode(self, typ="string", ts=""):
        """Request an AaaaHorodatage class timestamp input and
            return year, month, day, hour, minutes, seconds and
            offset UTC.

            Return typ =
            - "string": return a string (YYYY-MM-DDTHH:MM:SS+HH:MM). Default,
            compliant ISO 8601.
            - "list": return a list (fixed order).
            fixed order: year, month and day, hour, minutes, seconds, UTC.
            - "dict" or "dictionary": return a dict (any order).
            ts = timestamp: I will use ts, self.ts will not be modified.
            ts = none or "": I will use self.ts.

        """
        if ts == "":
            ts = self.ts

        # retour
        return self._calcul_decode(typ, ts)

    def offset_seconds2string(self, offset_seconds=0):
        """Return a string, timezone offset in the form +/-HH:MM

        utc_seconds = number of seconds, integer.
        -43200 >= utc_seconds <= +50400

        """
        return self._offset_seconds2string(offset_seconds)

    def offset_string2seconds(self, offset_string="+00:00"):
        """Return a number of seconds (integer)

        utc_string: timezone offset in the form +/-HH:MM

        """
        return self._offset_string2seconds(offset_string)

    def tz2utc(self):
        """Convert the timestamp ts to an UTC.

        self.ts will be updated.

        """
        ts = self.ts
        # ts_list = self.decode("list", ts)
        # ts_tmp_list[3] = heure, ts_tmp_list[4] = minutes
        tmp = ts.split("Z")
        ts_sec = int(tmp[0])
        epoch = int(ts_sec % 10000)
        ts_sec = int(ts_sec / 10000)
        offset_ts = self._offset_string2seconds(tmp[1])

        ts_sec -= offset_ts
        if ts_sec < 0:
            print("Fatal error 10: timestamp less than epoch in tz2utc(", ts,
                  ").", sep="")
            sys.exit(10)

        self.ts = str(ts_sec) + str(epoch) + "Z+00:00"

        return self.ts

    def utc2tz(self, *new_offset):
        """Convert a timestamp UTC to an other timezone.

        *new_offset:
        - Number of seconds (-43200 >= *new_offset <= +50400)
        - String (+/-HH:MM) ("-12:00" >= *new_offset <= "+14:00")

        self.ts will be updated.

        """
        if len(new_offset) < 1:
            print("Fatal error 7: missing *new_offset argument in ", end="")
            print("utc2tz(*new_offset).")
            sys.exit(7)
        if not isinstance(new_offset[0], int) and \
                not isinstance(new_offset[0], str):
            print("Fatal error 8: *new_offset must be a string ", end="")
            print("or an integer in utc2tz(*new_offset).")
            sys.exit(8)
        offset = new_offset[0]
        if isinstance(new_offset[0], str):
            offset = self._offset_string2seconds(new_offset[0])
        if offset < -43200 or offset > +50400:
            print("Fatal error 9: *new_offset out of range in ", end="")
            print("utc2tz(*new_offset).")
            print(" -43200 >= *new_offset <= +50400")
            print("or '-12:00' >= *new_offset <= '+14:00'.")
            sys.exit(9)

        ts = self.ts
        tmp = ts.split("Z")
        ts_offset = self.offset_string2seconds(tmp[1])
        if ts_offset != 0:
            print("Fatal error 12: I can only convert an UTC timestamp.")
            print("In utc2tz (*new_offset).")
            sys.exit(12)
        ts_sec = int(tmp[0])
        ts_epoch = int(ts_sec % 10000)
        ts_sec = int(ts_sec / 10000)
        ts_sec += offset
        self.ts = str(ts_sec) + str(ts_epoch) + "Z" +\
            self._offset_seconds2string(offset)

        return self.ts


chemin = p.dirname(p.abspath(__file__)) + "/"


class AaaaHorodatageTools(AaaaHorodatage):

    """
    Tools for timestamps of AaaaHorodatage class, Child class of
    AaaaHorodatage.

    Timestamp format = [0-9]+AAAAZ+/-HH:MM where [0-9]+ = the number of
    seconds from the epoch until the date entered, AAAA = the epoch of
    the timestamp, and Z+/-HH:MM the UTC offset (e.g for CEST,
    summertime: Z+02:00).  The timezone and epoch are embedded.

    Class attribute(s)
    - epoch: class reference year of the timestamp (only for encoding).
    Range: 1000 <= epoch <= 9999. Default 2000.

    Several ranges and keyboard input are managed, but not exceptions.
    """

    # For dev start #
    # in AaaaHorodatage:
    # année de référence (attribut de classe)
    #    epoch = 1900
    # private
    # attributs
    #    def _get_ljm(self, i):
    #    ljm = property(_get_ljm)
    # methodes
    #    def _bissextile(self, an = 0):
    #    def _input_entier(self, annonce=""):
    #    def _calcul_encode(self):
    #    def _cal    def _input_entier(self, annonce=""):cul_decode(self, typ):
    # méthodes publiques
    # classe (cls)
    #    def get_epoch(cls):
    #    get_epoch = classmethod(get_epoch)
    #    def set_epoch(cls, num):
    #    set_epoch = classmethod(set_epoch)
    # instance (self)
    #    def encode(self, d=""):
    #    def decode(self, typ="string", t=0):
    # For dev end

    def __init__(self, ts=""):
        AaaaHorodatage.__init__(self, ts)
        # protected
        # douglas = open("aaaa/42", "r")
        # self._Aaaa42 = douglas.read()
        # douglas.close()

    def get_42(self):
        douglas = open(chemin + "42", "r")
        print(douglas.read())
        douglas.close()
        print("Non fatal error 42: existential error 101010.")
        print("System not halted. L'histoire")
        print("                              con")
        print("                                 ti")
        print("                                   n")
        print("                                    u")
        print("                                     e")
        print("                                       .")
        print("                                        .")
        print("                                         .\n")
        print("|101010 101010 101010 101010 101010 101010 101010 101010 101010\
 101010 101010 |\n")

    # get_42 = property(_get_42)

    # protected #
    # attributs

    # Special #
    def copy(self):
        tmp = AaaaHorodatageTools()
        tmp.ts = self.ts
        return tmp

    def __eq__(self, ts_object):
        """== operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix == ts_object_posix

    def __ne__(self, ts_object):
        """!= operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix != ts_object_posix

    def __gt__(self, ts_object):
        """> operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix > ts_object_posix

    def __ge__(self, ts_object):
        """>= operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix >= ts_object_posix

    def __lt__(self, ts_object):
        """< operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix < ts_object_posix

    def __le__(self, ts_object):
        """<= operator"""
        aaaa = self.copy()
        aaaa_posix = aaaa.convert_aaaa2posix()
        ts_object_posix = ts_object.convert_aaaa2posix()
        return aaaa_posix <= ts_object_posix

    def __str__(self):
        """Return the string self.ts"""
        return self.get_ts()

    def __add__(self, seconds=0):
        """new_ts = ts_object + seconds.
        Overload of plus operator.

        self.ts will be updated

        Tips:
        - use dhms2second(d=0, h=0, m=0, s=0) method to
        convert days + hours + minutes + seconds in seconds
        - To add seconds to a new timestamp instance:
        new_ts_object = ts_object.copy()
        new_ts_object + seconds

        """
        tmp = self.ts.split("Z")
        ts_offset = tmp[1]
        tmp = int(tmp[0])
        ts_epoch = int(tmp % 10000)
        ts_seconds = int(tmp / 10000)
        ts_seconds += seconds
        self.ts = str(ts_seconds) + str(ts_epoch) + "Z" + ts_offset
        return self

    def __sub__(self, *nb_seconds_or_ts_object):
        """new_ts = ts_object - *nb_seconds_or_ts_object
        Overload of minus operator.

        if *nb_seconds_or_ts_object is ts_object, call
        self.ts.diffDays("string", *nb_seconds_or_ts_object.get_ts()),
        see this method. self.ts is NOT updated.

        if *nb_seconds_or_ts_object is a nb_seconds integer
        update and return  self.ts - *nb_seconds
        self.ts seconds - seconds must be >= 0 (epoch-01-01)

        Tips:
        - use dhms2second(d=0, h=0, m=0, s=0) utility method
        to convert days + hours + minutes + seconds in seconds
        - To add seconds to a new timestamp instance:
        new_ts_object = ts_object.copy()
        new_ts_object - seconds

        """
        if isinstance(nb_seconds_or_ts_object[0], AaaaHorodatageTools):
            return nb_seconds_or_ts_object[0].diffDays("string", self.get_ts())

        if isinstance(nb_seconds_or_ts_object[0], int):
            seconds = nb_seconds_or_ts_object[0]
            tmp = self.ts.split("Z")
            ts_offset = tmp[1]
            tmp = int(tmp[0])
            ts_epoch = int(tmp % 10000)
            ts_seconds = int(tmp / 10000)
            if ts_seconds >= seconds:
                ts_seconds -= seconds
            else:
                print("Fatal error 53: number of seconds to substract ",
                      end="")
                print("to big in __sub__(seconds=0). Substract < ", end="")
                print(ts_epoch, "-01-01 (epoch of the timestamp)",  sep="")
                print("Program halted.")
                sys.exit(53)
            self.ts = str(ts_seconds) + str(ts_epoch) + "Z" + ts_offset
            return self

    # protected #
    # méthodes
    # méthodes publiques #
    # class (cls)
    # instance (self)
    def diffDays(self, typ="string", ts2=0):
        """Difference between 2 timestamps in days, hours, minutes, seconds.
            ts2 - self.ts1.

            Usage: ts1_object.diffDays(<typ>, <ts2>)
            Offset UTC timestamp 1 must match offset UTC timestamp 2
            and epoch timestamp 1 must match epoch timestamp 2.

            Return typ =
            - "seconds": return the number of seconds.
            - "string": return a string (+/-DDTHH:MM:SS). Default.
            - "list": return a list (fixed order).
            fixed order: sens_difference, day, hour, minutes, seconds.
            - "dict" or "dictionary": return a dict (any order).
            ts2 = 0 or none: keyboard input.
            ts2 eg: ts2_object.get_ts()

        """
        # if keyboard
        if ts2 == 0:
            ts2 = input("Decode timestamp 2: ")
        # if arg
        # to do

        # Récupération des timestamp et test des offset utc
        ts1_split = self.ts.split("Z")
        ts2_split = ts2.split("Z")
        if ts1_split[1] != ts2_split[1]:
            print("Fatal error 51: offset UTC1 " + ts1_split[1] +
                  " does not match offset UTC2 " + ts2_split[1] +
                  "\nProgram halted.")
            print("Consider to standardize the 2 timestamps to Z (+00:00)")
            print(" using <instance>.tz2utc(timestamp1)")
            print(" using <instance>.tz2utc(timestamp2)")
            sys.exit(51)
        # recup ts1, ts2
        ts1 = int(ts1_split[0])
        ts2 = int(ts2_split[0])
        epoch1 = ts1 % 10000
        epoch2 = ts2 % 10000
        ts1 = int(ts1 / 10000)
        ts2 = int(ts2 / 10000)
        # test des epoch
        if epoch1 != epoch2:
            print("Fatal error 52: epoch1 " + str(epoch1) +
                  " does not match epoch2 " + str(epoch2) +
                  "\nProgram halted.")
            print("Consider to standardize the 2 epochs")
            print(" using <instance>.convert2epoch(timestamp1, epoch)")
            print(" using <instance>.convert2epoch(timestamp2, epoch)")
            sys.exit(52)
        # ts2 > ts1 => sens diff = +, sinon -
        sens_diff = "+"
        if ts1 > ts2:
            ts1, ts2 = ts2, ts1
            sens_diff = "-"

        dts = ts2 - ts1
        secondes = dts % 60
        minutes = int((dts / 60) % 60)
        heures = int((dts / (60 * 60)) % 24)
        jours = int(dts / (60 * 60 * 24))

        if typ == "seconds":
            if sens_diff == "-":
                retour = -dts
            else:
                retour = dts

        if typ == "string":
            retour = (sens_diff + str(jours) + "T" + str(heures) + ":" +
                      str(minutes) + ":" + str(secondes))
        if typ == "list":
            retour = list()
            retour.append(sens_diff)
            retour.append(jours)
            retour.append(heures)
            retour.append(minutes)
            retour.append(secondes)

        if typ == "dict" or typ == "dictionary":
            retour = dict()
            retour["sensdiff"] = sens_diff
            retour["days"] = jours
            retour["hours"] = heures
            retour["minutes"] = minutes
            retour["seconds"] = secondes

        return retour

    def convert2epoch(self, epoch):
        """Convert an embedded epoch to an other

        1000 <= epoch <= 9999
        self.ts is updated

        """
        ts_offset = self.ts.split("Z")
        ts_offset = self.offset_string2seconds(ts_offset[1])
        save_offset = self.get_utc_local_offset()
        save_epoch = self.get_epoch()
        ts = self.decode("list", self.ts)
        self.set_epoch(epoch)
        self.set_utc_local_offset(ts_offset)
        ts = self.encode(ts)
        self.set_epoch(save_epoch)
        self.set_utc_local_offset(save_offset)
        self.ts = ts
        return self.ts

    def dhms2seconds(self, d=0, h=0, m=0, s=0):
        """Convert days + hours + minutes + seconds in seconds"""
        return d * self._get_nb_sec_par_jour() + h * 3600 + m * 60 + s

    def convert_aaaa2posix(self):
        """Return a Posix timestamp (UTC) from an Aaaa timestamp"""
        aaaa_ts = self.copy()
        aaaa_ts.convert2epoch(1970)
        aaaa_ts.tz2utc()
        # self.ts = save_local_ts
        tmp = aaaa_ts.get_ts().split("Z")
        ts_sec = int(tmp[0])
        ts_sec = int(ts_sec / 10000)

        return ts_sec

    def convert_posix2aaaa(self, posix_ts):
        """Return an Aaaa timestamp from a Posix timestamp
        self.ts is updated

        posix_ts will be considered at UTC time.

        """
        self.ts = str(posix_ts) + "1970Z+00:00"
        return self.ts

    def set_ts_same_epoch_offset(self, ts_object):
        """Convert ts_object to same epoch and UTC offset
        than self.ts

        ts_object.ts is updated
        """
        ts_epoch = self.get_ts_epoch()
        tmp = self.get_ts()
        tmp = tmp.split("Z")
        ts_offset = tmp[1]
        ts_object.tz2utc()
        ts_object.utc2tz(ts_offset)
        ts_object.convert2epoch(ts_epoch)

        return ts_object


if __name__ == "__main__":
    # at top, # from ahordat import AaaaHorodatage # to test module

    h = AaaaHorodatageTools()
    h.encode((2001, 1, 1, 10, 10, 10))
    print(h.decode())
    h2 = h + h.dhms2seconds(1, 2, 10, 20)
    print(h2.get_ts())
    print(h.decode(), " - ", h2.decode())

    sys.exit()
    k = AaaaHorodatageTools()
    print(k.get_utc_local_offset())
    print(k.get_utc_local_offset("string"))
    myKCEST = k.encode([2001, 2, 20, 20, 15, 30])
    print(myKCEST)
    print(k.decode('string', myKCEST), "\n---")
    print(k.convert2epoch(myKCEST, 1900))
