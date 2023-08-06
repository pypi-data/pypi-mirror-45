from setuptools import setup
from sphinx_materialdesign_theme import __version__

setup(
    name = 'sphinx_materialdesign_theme_nopyc',
    version = __version__,
	download_url="https://github.com/ir-3/sphinx_materialdesign_theme/archive/v1.tar.gz",
    author = 'Masahiko Yasuda',
    author_email= 'myasuda@uchida.co.jp',
    url="https://github.com/myyasuda/sphinx_materialdesign_theme",
    docs_url="http://myyasuda.github.io/sphinx_materialdesign_theme/",
    description='Sphinx Material Design Theme WITHOUT ITS MAJOR FLAW',
    packages = ['sphinx_materialdesign_theme'],
    include_package_data=True,
    license= 'MIT License',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Documentation"
    ],
    entry_points = {
        'sphinx.html_themes': [
            'sphinx_materialdesign_theme = sphinx_materialdesign_theme',
        ]
    }
)

