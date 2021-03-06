from setuptools import setup, find_packages

version = '1.0'

setup(
    name='tn.bulletino',
    version=version,
    description='',
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='TN Tecnologia e Negocios',
    author_email='ed@tecnologiaenegocios.com.br',
    url='http://www.tecnologiaenegocios.com.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['tn'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.autopermission',
        'five.globalrequest',
        'Plone',
        'plone.app.z3cform',
        'plone.api',
        'plone.directives.form',
        'tn.plonebehavior.template',
        'tn.plonehtmlimagecache',
        'tn.plonehtmlpage',
        'tn.plonemailing',
        'tn.plonestyledpage',
    ],
    extras_require={
        'test': [
            'stubydoo',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
