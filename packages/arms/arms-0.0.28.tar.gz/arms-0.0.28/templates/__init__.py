level_list = [
    'back-java',
    'back-nginx',
    'back-node',
    'back-python',
    'front-build',
    'front-react',
]


def out_levels():
    return list(set(x.split('-', 1)[0] for x in level_list))


def inner_levels(prefix):
    return list(set(x.split('-', 1)[-1] for x in level_list if x.startswith(prefix + '-')))
