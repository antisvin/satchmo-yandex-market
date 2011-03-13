from setuptools import setup, find_packages

setup(
    name='satchmo-yandex-market',
    version=__import__('yandexmarket').VERSION,
    description=('An application that lets you export data from Satchmo '
                 'internet shop to Yandex Market format.'),
    author='Stas Shtin',
    author_email='antisvin@gmail.com',
    url='http://code.google.com/p/satchmo-yandex-market/',
    license = 'MIT License',
    platforms = ['any'],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)

