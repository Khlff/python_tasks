import re

sub_str = 'КОШКА'
input_string = "СОБАКА КОШКА ПОПУГАЙ СОБАКА ЯЩЕРИЦА ЖОПА КОШКА КОШКА АНАНАС ЯМАЙКА ЧИЛИ"
if re.findall(r'(.*?) ', input_string).count(sub_str) > 2:
    print('ok')
else:
    print('no')

password = 'jjj23&Aaz'
if len(re.findall(r'[A-Za-z\d]', password)) and len(re.findall(r'[a-z]', password)) and len(
        re.findall(r'\d', password)) and len(re.findall(r'\w', password)):
    print('secure')
else:
    print('not secure')
