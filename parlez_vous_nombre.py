import json
import re


def get_json():
    with open('parlez_vous_nombre.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def decoupe(nombre):
    words = []
    word = ""
    for i, lettre in enumerate(nombre):
        if lettre == " " or lettre == "-":
            words.append(word)
            word = ""
        else:
            word += lettre
        if i+1 == len(nombre):
            words.append(word)
    return words


def convert_words_nombre(words):
    nombre = []
    a = 0
    for word in words:
        d = data['mot-arabe']
        for index in range(len(d)):
            find = re.findall(d[index]['autochtone'], word)
            if find:
                nombre.append(d[index]['arabe'])
                if len(str(d[index]['arabe'])) > 3 and a != 0:
                    nombre.pop(a-1)
                    a = 0
                    nombre.append('+')
                elif len(str(d[index]['arabe'])) > 2 and a == 0:
                    nombre.append('+')
                    a = len(nombre)
    print(nombre)
    return nombre


def cas_special(f, s):
    '''
    Gère les cas des 80-24-21...
    '''
    if s == 20:
        return f*s
    else:
        return f+s


def separe(nombre):
    tab = []
    result = []
    j = 0
    for i in nombre:
        if i != '+':
            tab.append(i)
        elif i == '+' and j != 0:
            result.append(tab)
            tab = []
            j = 0
        j += 1
    result.append(tab)
    return result


def convert_total(nombres):
    end = 0
    result = 0
    for tab in nombres:
        try:
            while len(tab) > 0:
                first = tab.pop(0)
                sec = tab.pop(0)
                try:
                    n = tab.pop(0)
                    if n == 20:
                        sec *= n
                    else:
                        tab.insert(0, n)
                except:
                    pass
                if len(str(first)) > 2 and len(str(sec)) < 3:
                    result = first + sec
                elif len(str(sec)) > 2:
                    result = first * sec
                else:
                    result = cas_special(first, sec)
                tab.insert(0, result)
        except:
            end += first
    return end


def formate(nombre):
    str_nb = str(nombre)[::-1]
    nb = ""
    for i in range(len(str_nb)):
        nb += str_nb[i]
        if i % 3 == 2:
            nb += " "
    return nb[::-1]


def romain(nombre):
    result = 0
    d = data['romain-arabe']
    for i in range(len(d)):
        result += nombre.count(d[i]['autochtone']) * d[i]['arabe']
    return result


def check_lg(text):
    if len(re.findall(r'^[M]*[D]*[C]*[L]*[X]*[V]*[I]*', text)[0]):
        return 0
    return 1


def main(text):
    if check_lg(text):
        a = decoupe(text)
        b = convert_words_nombre(a)
        c = separe(b)
        end = convert_total(c)
    else:
        end = romain(text)
    format_end = formate(end)
    print("{} = {}".format(text, format_end))


if __name__ == '__main__':
    data = get_json()
    main(input('Insérez un nombre écrit en toutes lettres :'))
