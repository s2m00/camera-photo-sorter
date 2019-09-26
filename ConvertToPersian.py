dic = {
    '0' : '۰',
    '1' : '۱',
    '2' : '۲',
    '3' : '۳',
    '4' : '۴',
    '5' : '۵',
    '6' : '۶',
    '7' : '۷',
    '8' : '۸',
    '9' : '۹',

    'A' : 'آ',
    'a' : 'ا',
    'B' : 'ب',
    'C' : 'س',
    'D' : 'د',
    'E' : 'ی',
    'F' : 'ف',
    'G' : 'گ',
    'H' : 'ه',

    '-' : '-',
    '/' : '-',
    ':' : '-',
    ' ' : '-'

}

def getPer(s_input):
    global out_d
    out_d = ""
    for c in s_input:
        out_d = out_d + dic.get(c)

    return out_d



