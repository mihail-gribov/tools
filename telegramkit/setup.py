from setuptools import setup, find_packages

setup(
    name='telegramkit',
    version='1.0.0',
    description='A library for asynchronous interaction with Telegram channels and parsing data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ваше Имя',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/telegramkit',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.1',
        'beautifulsoup4>=4.11.1',
        'markdownify>=0.9.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
