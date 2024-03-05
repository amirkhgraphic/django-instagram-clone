import uuid


def category_path(instance, filename):
    app = instance.__class__.__module__.split('.')[1]
    return f'{app}/category/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'


def avatar_path(instance, filename):
    return f'user/avatar/user-{instance.id}-{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'


def get_default_thumbnail():
    return 'default/default.png'


default_preview = ('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus laborum autem, '
                   'dolores inventore, beatae nam.')
