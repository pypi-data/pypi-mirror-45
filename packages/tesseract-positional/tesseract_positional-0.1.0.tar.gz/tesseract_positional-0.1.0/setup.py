from setuptools import setup

setup(
    name='tesseract_positional',
    version='0.1.0',
    description='Tool to save positional OCR data to a text file',
    url='http://github.com/tjkessler/tesseract_positional',
    author='Travis Kessler',
    author_email='travis.j.kessler@gmail.com',
    license='MIT',
    packages=['tesseract_positional'],
    install_requires=['pytesseract', 'Pillow'],
    entry_points={
        'console_scripts': [
            'tesseract_positional=tesseract_positional.cmd_line:main'
        ]
    },
    zip_safe=False
)
