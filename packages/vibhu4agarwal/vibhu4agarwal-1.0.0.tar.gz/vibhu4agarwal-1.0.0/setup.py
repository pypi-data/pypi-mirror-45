from setuptools import setup, find_packages
import vibhu4agarwal as vibhu
import pypandoc

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = pypandoc.convert('README.md', 'rst')

setup(
        name=vibhu.__name__,
        version=vibhu.__version__,
        author=vibhu.__author__,
        author_email='vibhu4agarwal@gmail.com',
        url='https://github.com/Vibhu-Agarwal/vibhu4agarwal',
        description='Interactive Resume of Vibhu Agarwal.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'vibhu = vibhu4agarwal.vibhu:main'
            ]
        },
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords='resume portfolio vibhu4agarwal',
        install_requires=requirements,
        zip_safe=False
)
