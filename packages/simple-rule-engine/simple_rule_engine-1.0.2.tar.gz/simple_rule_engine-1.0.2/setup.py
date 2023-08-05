from setuptools import setup

setup(
    name="simple_rule_engine",
    version="1.0.2",
    description="Lightweight yet flexible Rule Engine Parser that supports declarative specification of complex rules",
    url="https://github.com/jeyabalajis/simple_rule_engine",
    author="Jeyabalaji Subramanian",
    author_email="jeyabalaji.subramanian@gmail.com",
    license="MIT",
    include_package_data=True,
    package_dir={'parser': 'parser'},
    packages=['parser'],
    keywords='simple rule engine',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ]
)
