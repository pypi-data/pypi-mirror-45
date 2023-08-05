from setuptools import setup

setup_kwargs = dict(
    name='sentry_falcon',
    version='0.1.0',
    description='Falcon web framework integration for the Sentry SDK',
    packages=['sentry_falcon'],
    author='Jacob Magnusson',
    author_email='m@jacobian.se',
    url='https://github.com/jmagnusson/sentry-falcon',
    license='BSD',
    platforms='any',
    install_requires=[
        'falcon',
        'sentry_sdk',
    ],
    extras_require={
        'test': {
            'coverage',
            'flake8',
            'isort',
            'pytest',
        },
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

if __name__ == '__main__':
    setup(**setup_kwargs)
