from setuptools import setup, find_packages

setup(
    name='haintsec',
    version='1.0.0',
    packages=find_packages(),  # Include all packages (e.g., utils)
    py_modules=['haintsec'],  # Main script
    entry_points={
        'console_scripts': [
            'haintsec = haintsec:main',  # Links the `haintsec` command to the `main()` function
        ],
    },
    install_requires=[
        'colorama',
        'requests',
        'beautifulsoup4',
        'python-nmap',
        'python-docx',
        'pdfkit',
        'argparse',
        'urllib3',
    ],
    author="Yassine Selmi",
    author_email="yassineselmi629@gmail.com",  # Add your email if you want
    description="A web vulnerability testing tool for scanning and reporting website weaknesses.",
    long_description=open('README.md').read(),  # Ensure README.md exists
    long_description_content_type="text/markdown",
    url="https://github.com/Y518221/HaintSec",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
