from setuptools import setup, find_packages
setup(
    name="rockspring",
    version="0.1.2",
    packages=find_packages(),
    scripts=['rockspring/generator.py'],

    install_requires=['jinja2', 'click'],
    include_package_data=True,

    # metadata to display on PyPI
    author="Pawel Burzynski",
    author_email="p.k.burzynski@gmail.com",
    description="Request/Reply service generation package",
    license="MIT",
    entry_points='''
        [console_scripts]
        rsgen=rockspring.generator:generate
    ''',
)