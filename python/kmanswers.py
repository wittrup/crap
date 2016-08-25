"""This file contains my found solutions.
For spoiler purposes the answers are base64 encoded.
Scrambled list contains a tuple with answer first and comment second.
Importing this file will load list answers"""

from base64 import b64decode as decode


scrambled =[('cm90KCRpbnB1dCwgNykg', 'IG9yZCgnSScpIC0gb3JkKCdCJyk='),
            ('cm90KCRpbnB1dCwgLTExKSA=', 'IG9yZCgnSScpIC0gb3JkKCdUJyk='),
            ('cm90KCRpbnB1dCwgMylbOjotMV0g', 'IGJydXRlZm9yY2U='),
            ('', ''),
            ('', ''),
            ('YjY0ZGVjb2RlKCRpbnB1dCk=', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', ''),
            ('', '')]

answers = [decode(answer).decode('ascii') for answer, comment in scrambled]

if __name__ == '__main__':
    for answer, comment in [(decode(answer).decode('ascii'), decode(comment).decode('ascii')) for answer, comment in scrambled]:
        print(answer, "#" * (len(comment) > 0) + comment, sep="")
