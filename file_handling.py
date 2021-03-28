from io import open


def save_password(file_path, password, website=None, mail=None, username=None):
    with open(file_path, 'a') as f:
        border = '#' * 20
        data = ''
        if website is not None and website != '':
            data += f'Website:   {website}\n'

        if mail is not None and mail != '':
            data += f'Mail:      {mail}\n'

        if username is not None and username != '':
            data += f'Username:  {username}\n'

        data += f'Password:  {password}'

        f.write(f'{border}\n\n{data}\n\n{border}\n\n\n')
