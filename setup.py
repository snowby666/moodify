from setuptools import setup, find_packages
from pathlib import Path

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text(encoding='utf-8')

VERSION = '1.0.0'
DESCRIPTION = 'A simple, lightweight and efficient Spotify playlist creator that generates custom playlists based on your mood 🎶'
LONG_DESCRIPTION = '🎧 A music recommendation system that generates Spotify music playlist based on your mood and preferences 🦄'

setup(
    name="moodify",
    version=VERSION,
    author="snowby666",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=['requests', 'six', 'loguru', 'requests_html', 'bs4', 'ytmusicapi'],
    keywords=['spotify', 'music', 'mood', 'music recommendation', 'playlist', 'emotion', 'api'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent"
    ],
    url="https://github.com/snowby666/moodify",
)