"""I wrote a fully automated Vigenere Cipher cracker
submitted 1 year ago by Ouro130Ros
You can find the python code at pastebin
This class allows you to encrypt, decrypt and crack the Vigenere cipher.
To Encrypt simply instantiate the class and call .Encrypt(plainText, key)
To Decrypt simply call .Decrypt(cipherText, key)
To Crack call .Crack(cipherText, pathToEnglishDictionaryFile, candidateCount, passPercentage)
I used this for a dictionary but any in the same format will work.
The Candidate count is the number of passwords to test at each key length.
The passPercentage is the percentage of english words in the plaintext needed to consider the crack a success.
I use a combination of Kasiki analysis to guess key lengths along with Turing's 'Bans' frequency analysis to find the most likely keys of a given length. I hope you enjoy!
P.S. sorry for the lazy code.

https://www.reddit.com/r/codes/comments/3apt0l/i_wrote_a_fully_automated_vigenere_cipher_cracker/
"""

from math import log
import re
import os


class VCipher:
    def __init__(self):
        self.Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.Frequencies = {
            'A': 84, 'B': 23, 'C': 21, 'D': 46, 'E': 116, 'F': 20, 'G': 25, 'H': 49, 'I': 76,
            'J': 2, 'K': 5, 'L': 38, 'M': 34, 'N': 66, 'O': 66, 'P': 15, 'Q': 2, 'R': 64,
            'S': 73, 'T': 81, 'U': 19, 'V': 11, 'W': 21, 'X': 2, 'Y': 24, 'Z': 3
        }

        for k in self.Frequencies.keys():
            self.Frequencies[k] = self.Frequencies[k] / 1000.0

        self.Bans = {}
        for a in self.Alphabet:
            x = (25 * self.Frequencies[a]) / (1 - self.Frequencies[a])
            x = log(x) / log(10)
            self.Bans[ord(a) - ord('A')] = x

    def TuringCheck(self, cipherText, keyLength, resultCount):
        ByLetter = {}
        for a in self.Alphabet:
            ByLetter[a] = []
            ordVal = ord(a) - ord('A')
            for col in range(0, keyLength):
                i = col
                Evidence = 0
                while i < len(cipherText):
                    cipherVal = ord(cipherText[i]) - ord('A')
                    diff = (cipherVal - ordVal) % 26
                    Evidence += self.Bans[diff]
                    i += keyLength
                ByLetter[a].append(Evidence)
        Result = []
        for i in range(0, keyLength):
            Column = {}
            for l in self.Alphabet:
                Column[l] = ByLetter[l][i]
            Result.append(Column)
        return self._GetLikelyPasswords(Result, resultCount)

    def Encrypt(self, plainText, key):
        CipherText = ''
        KeyPos = 0
        for l in plainText:
            if l in self.Alphabet:
                lV = ord(l) - ord('A')
                kV = ord(key[KeyPos].upper()) - ord('A')
                val = (lV + kV) % 26
                CipherText += chr(val + ord('A'))
                KeyPos = (KeyPos + 1) % len(key)
            elif l.upper() in self.Alphabet:
                lV = ord(l) - ord('a')
                kV = ord(key[KeyPos].lower()) - ord('a')
                val = (lV + kV) % 26
                CipherText += chr(val + ord('a'))
                KeyPos = (KeyPos + 1) % len(key)
            else:
                CipherText += l
        return CipherText

    def Decrypt(self, cipherText, key):
        PlainText = ''
        KeyPos = 0
        for l in cipherText:
            if l in self.Alphabet:
                lV = ord(l) - ord('A')
                kV = ord(key[KeyPos].upper()) - ord('A')
                val = (lV - kV) % 26
                PlainText += chr(val + ord('A'))
                KeyPos = (KeyPos + 1) % len(key)
            elif l.upper() in self.Alphabet:
                lV = ord(l) - ord('a')
                kV = ord(key[KeyPos].lower()) - ord('a')
                val = (lV - kV) % 26
                PlainText += chr(val + ord('a'))
                KeyPos = (KeyPos + 1) % len(key)
            else:
                PlainText += l
        return PlainText

    def _Factor(self, n):
        return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))

    def _FindRepeatedSubstrings(self, cipherText, subLength):
        Subs = {}
        for i in range(0, len(cipherText) - subLength):
            Substring = cipherText[i:i + subLength]
            if cipherText.count(Substring) > 1 and not Substring in Subs.keys():
                Subs[Substring] = [m.start() for m in re.finditer(Substring, cipherText)]

        return Subs

    def _AddToCountDict(self, d, v):
        if not v in d.keys():
            d[v] = 1
        else:
            d[v] += 1

    def Crack(self, cipherText, pathToEnglishDict, candidateCount, passPercentage):
        print
        "Cracking...\n{0}".format(cipherText)
        with open(pathToEnglishDict) as f:
            Dictionary = [x.strip('\n') for x in f.readlines()]
        Trimmed = self.Trim(cipherText)
        KeyLengthsDict = self.GetLikelyKeyLengths(Trimmed)
        KeyLengths = sorted(KeyLengthsDict, key=KeyLengthsDict.__getitem__, reverse=True)
        print
        "Found {0} candidate key lengths".format(len(KeyLengths))
        for length in KeyLengths:
            print
            "Testing Length: {0}".format(length)
            Keys = self.TuringCheck(Trimmed, length, candidateCount)
            for key in Keys:
                print
                "     Testing Key: {0}".format(key)
                PlainText = self.TrimWithSpaces(self.Decrypt(cipherText, key))
                Words = PlainText.split()
                EnglishWordCount = 0
                for word in Words:
                    if word in Dictionary: EnglishWordCount += 1
                Percentage = float(EnglishWordCount) / len(Words)
                print
                "          Percentage of english words in sample: %{0}".format(Percentage * 100)
                if Percentage >= (passPercentage / 100.0):
                    print
                    "-------------"
                    print
                    "Cracked!"
                    print
                    "Key = {0}".format(key)
                    print
                    self.Decrypt(cipherText, key)
                    return
        print
        "No key found... try other cyphers"

    def GetLikelyKeyLengths(self, cyphertext):
        Substrings = self._FindRepeatedSubstrings(cyphertext, 3)
        Diffs = []
        for substring in Substrings.keys():
            for i in range(0, len(Substrings[substring]) - 1):
                Diffs.append(Substrings[substring][i + 1] - Substrings[substring][i])
        FactorCounts = {}

        for d in Diffs:
            Factors = self._Factor(d)
            for f in Factors:
                self._AddToCountDict(FactorCounts, f)
        return FactorCounts

    def _GetLikelyPasswords(self, columns, count):
        ColumnLetters = []
        Counts = []
        for ranks in columns:
            ColumnLetters.append(sorted(ranks, key=ranks.__getitem__, reverse=True))
            Counts.append(0)

        Results = []
        ResultCount = 0
        while ResultCount < count:
            BestPass = ""
            SmallestDiff = 1000
            SmallestCol = -1
            for i in range(0, len(columns)):
                BestPass += ColumnLetters[i][Counts[i]]
                if Counts[i] < 25:
                    V1 = columns[i][ColumnLetters[i][Counts[i]]]
                    V2 = columns[i][ColumnLetters[i][Counts[i] + 1]]
                    Diff = V1 - V2
                    if Diff < SmallestDiff:
                        SmallestDiff = Diff
                        SmallestCol = i
            Counts[SmallestCol] += 1
            Results.append(BestPass)
            ResultCount += 1
        return Results

    def TrimWithSpaces(self, text):
        result = ''
        for l in text:
            if l.upper() in self.Alphabet or l == ' ':
                result += l.upper()
        return result

    def Trim(self, text):
        result = ''
        for l in text:
            if l.upper() in self.Alphabet:
                result += l.upper()
        return result

