from distutils.core import setup

setup(
    name="SendNotificationViaMail",
    version="0.0.0",
    author="prasanth vajja",
    author_email="prasanth@caratred.com",
    packages=["Services"],
    include_package_data=True,
    install_requires=[
    "python-http-client==3.1.0",
    "sendgrid==6.0.4"
    ]
)
