import setuptools

setuptools.setup(
    name="AlarmTime",
    version="0.1.3",
    author="Md. Shohanur Rahman",
    author_email="dshohan112@gmail.com",
    url = 'https://github.com/shohan98/alarm_time_claculate',
    description="Detect alarm time from natural sentence and calculate time difference from current time to target time.",
    long_description='For calculating time difference from current time to Target time and can detect a time from our natural language',
    long_description_content_type="text/markdown",
    license = 'MIT',
    install_requires = ['datetime','python-dateutil','regex'],
    packages=setuptools.find_packages(),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
