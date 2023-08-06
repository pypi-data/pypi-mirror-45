import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='docdetect1',
    version='1.0.1',
    author='haotran',
    author_email='hao.cse@gmail.com',
    url='https://github.com/haocse/docdetect-1',
    description='Real-time detection of documents in images.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=[
        'docdetect'
    ],
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    keywords='docdetect document-detection rectangle-detection edge-detection',
    zip_safe=True
)
