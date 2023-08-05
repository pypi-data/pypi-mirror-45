from distutils.core import setup

setup(
    name='affirm-pay',
    packages=['affirm'],
    version='0.1',
    license='MIT',
    description='Python Client for Affirm',
    author='Anshul Sharma',
    author_email='anshul.jmi@gmail.com',
    url='https://github.com/raun/affirm-python-sdk',  # Provide either the link to your github or to your website
    download_url='https://github.com/raun/affirm-python-sdk/archive/v_01.tar.gz',  # I explain this later on
    keywords=['AFFIRM', 'SDK', 'CLIENT', 'INTEGRATION'],  # Keywords that define your package best
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
)
