from setuptools import setup, find_packages

setup(
    name='PhishWatcher',
    author='Zack Nagaich',
    version='1.0',
    author_email='zacknagaich@gmail.com',
    description='Applies DNSTwist fuzzing logic to Domain to yield a set of domains that may be used for domain squatting. ',
    license='GPL',
    packages=find_packages('src'),
    package_dir={ '' : 'src' },
    zip_safe=False,
    package_data={
        '' : [ '*.gif', '*.png', '*.conf', '*.mtz', '*.machine' ] # list of resources
    },
    install_requires=[
        'canari'
    ],
    dependency_links=[
        # custom links for the install_requires
    ]
)
