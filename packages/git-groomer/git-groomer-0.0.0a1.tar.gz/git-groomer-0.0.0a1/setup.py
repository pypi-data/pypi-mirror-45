from setuptools import setup, find_packages

setup(
    name='git-groomer',
    version='0.0.0a1',
    description='Tool to take good care of your git repository.',
    url='https://github.com/JavierLuna/git-groomer',
    author='Javier Luna Molina',
    author_email='javierlunamolina@gmail.com',
    install_requires=['requests', 'maya'],
    setup_require=['pytest-runner'],
    tests_require=["pytest", "pytest-mock", "pytest-freezegun", "requests-mock"],
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='git repository gitlab git-grooming grooming groom branch commit repo ',
    packages=find_packages(exclude=['tests'])
)
