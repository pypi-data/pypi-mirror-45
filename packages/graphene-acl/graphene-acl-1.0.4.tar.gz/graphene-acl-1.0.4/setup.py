# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['graphene_acl', 'graphene_acl.tests', 'graphene_acl.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1,<3.0']

setup_kwargs = {
    'name': 'graphene-acl',
    'version': '1.0.4',
    'description': 'Graphene Field ACL',
    'long_description': "# graphene-acl\n\nThe motivation for this library is to simplify access control protection for Graphene Fields. A common approach to ACL protection is through the use of a reusable permissions validation decorator. The problem is this is cumbersome for Graphene Fields that use the standard resolver. You are forced to write an unnecessary resolver function just to annotate it with your permissions validator. The second cumbersome problem this library addresses is ACL role based resolvers. Depending on the users role you might want to perform different business logic in order to retrieve the data they requested for a Graphene Field.\n\n## Installation\n\n```bash\n$ pip install graphene-acl\n```\n\n## Usage\n\n### acl_classifier\n\nThe purpose of the classifier is to return a route key that will be used to determine which resolver function is used for resolving the field. The classifier function has access to all the arguments from the field resolver.\n\n### acl_validator\n\nThe purpose of the validator is to authorize access to the field. This validation will occurr before classification routing happens. If authorization validation is different per classification route then you should not use this validator to enforce authorization access. Instead you should authorize at the specific classifier resolver definition.\n\n### Example\n\n```python\nfrom graphene_acl import AclField\nimport graphene\n\ndef classifier(root, info, *args, **kwargs):\n    if 'admin' in info.context.jwt.permissions:\n        return 'admin'\n    return None\n\ndef has_permissions(permissions):\n    def validator(root, info, *args, **kwars):\n        if (any([permission in info.context.jwt.permissions for permission in permissions])):\n            return True\n        raise AuthorizationError(f'Not authorized to query field {info.field_name}')\n\n    return validator\n\nclass Foo(graphene.ObjectType):\n    private_name = AclField(graphene.String, acl_classifier=classifier)\n    restricted_name = AclField(graphene.String, acl_validator=has_permissions(['foo:name:read', 'admin']))\n\n@Foo.private_name.resolve('admin')\ndef resolve_private_name__admin(root, info, *args, **kwargs):\n    pass\n\n@Foo.private_name.resolve()\ndef resolve_private_name__default(root, info):\n    # Alternatively, authorization handling could be done by an acl_validator\n    raise Error('Not Authorized')\n```\n\nACL Connection Fields\n\n```python\nfrom graphene_django.filter import DjangoFilterConnectionField\nfrom graphene_acl import acl_field_type\n\nBarConnectionField = acl_field_type('BarConnectionField', DjangoFilterConnectionField)\n\nclass Foo(graphene.ObjectType):\n    bar = BarConnectionField(MyNode, acl_permissions=has_permission('FOO'))\n\n```\n\n## Development\n\n### First time setup\n\n-   Install Precommit hooks\n-   `brew install pre-commit && pre-commit install && pre-commit install --install-hooks`\n-   Install poetry: https://github.com/sdispater/poetry#installation\n-   `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`\n-   Install dependencies\n-   `poetry install`\n",
    'author': 'Nick Harris',
    'author_email': 'nick.harris@cybergrx.com',
    'url': 'https://github.com/CyberGRX/graphene-acl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
