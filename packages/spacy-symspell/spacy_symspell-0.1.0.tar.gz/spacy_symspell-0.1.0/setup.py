from pathlib import Path
from setuptools import setup, find_packages


def setup_package():
    package_name = 'spacy_symspell'
    root = Path(__file__).parent.resolve()

    # Read in package meta from about.py
    about_path = root / package_name / 'about.py'
    with about_path.open('r', encoding='utf8') as f:
        about = {}
        exec(f.read(), about)

    # Get readme
    readme_path = root / 'README.md'
    with readme_path.open('r', encoding='utf8') as f:
        readme = f.read()

    setup(
        name=package_name,
        description=about['__summary__'],
        long_description=readme,
        author=about['__author__'],
        author_email=about['__email__'],
        url=about['__url__'],
        version=about['__version__'],
        license=about['__license__'],
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'spacy>=2.0.0,<3.0.0',
            'symspellpy>=6.3.8'],
        python_requires=">=3.5",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7"
        ],
    )


if __name__ == '__main__':
    setup_package()