from setuptools import setup, find_packages

setup(
    name='YourGame',
    version='1.0.0',
    description='A cross-platform game built with Pygame',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pygame-menu',
        'pytmx',
    ],
    entry_points={
        'console_scripts': [
            'yourgame=main:main',
            'compile-game=compile_game:main',  # Add this line for the compile script
        ],
    },
    package_data={
        '': ['gfx/images/*.jpg', 'map/*.tmx'],
    },
    include_package_data=True,
)