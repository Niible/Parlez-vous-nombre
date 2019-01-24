import json
import re
text = "sept cent vingt et un"
test = "cent vingt quatre mille huit cent deux"
ttet = "trois mille milliard deux cent quatre vingt un million cinq cent quarante deux mille neuf cent quatre vingt dix neuf"
tttt = "sept cent quatre vingt dix neuf million cent soixante dix mille huit cent douze"


def get_json():
    '''
    Récupere le fichier Json avec les conversions 'lettres-nombres'
    '''
    with open('dict-conv-chiffres.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def decoupe(nombre):
    '''
    Sépare chaque mot qu'il y ait un espace ou un 'tiret' pour les mettre dans une liste
    '''
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
    '''
    Convertion des mots en chiffre ou nombre
    Plus un algorithme permettant de ranger les nombres qui vont ensemble
    '''
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
    '''
    En fonction de convert_words_nombre et des séparation défini range les valeurs dans des tableaux
    '''
    tab = []
    result = []
    j = 0
    for i in nombre:
        if i != '+':
            tab.append(i)
        elif i == '+' and j != 1:
            result.append(tab)
            tab = []
            j = 0
        j += 1
    result.append(tab)
    return result


def convert_total(nombres):
    '''
    Algorithme donnant le nombre final !!
    '''
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
    '''
    format le nombre en str pour afficher les espaces ex: 1 000 000
    '''
    str_nb = str(nombre)[::-1]
    nb = ""
    for i in range(len(str_nb)):
        nb += str_nb[i]
        if i % 3 == 2:
            nb += " "
    return nb[::-1]


def romain(nombre):
    '''
    Convertion des chiffres romain en arabe
    '''
    result = 0
    d = data['romain-arabe']
    for i in range(len(d)):
        result += nombre.count(d[i]['autochtone']) * d[i]['arabe']
    return result


def check_lg(text):
    '''
    Check si le texte comporte des chiffres romain et renvoie 0 sinon 1 
    '''
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
    main(input('Inséré un nombre écrit en toute lettre :'))