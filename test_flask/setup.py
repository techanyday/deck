from setuptools import setup, find_packages

setup(
    name="powerpoint-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask==1.1.4',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-Login==0.6.2',
        'Flask-CORS==3.0.10',
        'Werkzeug==1.0.1',
        'MarkupSafe==2.0.1',
        'Jinja2==2.11.3',
        'itsdangerous==1.1.0',
        'SQLAlchemy==1.4.23'
    ]
)
