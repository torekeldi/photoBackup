vk_auth = (
    'https://oauth.vk.com/authorize'
    '?client_id=51878226&'
    'redirect_uri=http://oauth.vk.com&'
    'display=page&'
    'scope=photos&'
    'response_type=token&'
    'v=5.199'
)

print(vk_auth)

# запустите код, перейдите по ссылке, которая появится ниже, авторизуйтесь в ВК
# появиться страница, из адресной ссылки скопируйте access_token в файл my_tokens.py