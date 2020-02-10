def replace_text(text):
    list1 = []
    for i in text.lower():
        if 97 <= ord(i) <= 122 or 65 <= ord(i) <= 90:
            list1.append(i)
        else:
            list1.append('-')
    a = '-'.join((''.join(list1)).split('-')).replace('--', '-')
    return a