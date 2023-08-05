from setuptools import setup


setup(
    name='lime_python',
    packages=['lime_python', 'lime_python.base',
              'lime_python.documents', 'lime_python.utils'],
    version='v1.0.1',
    license='apache-2.0',
    description='This module implements the basic models of the LIME protocol',
    author='Gabriel Rodrigues dos Santos',
    author_email='gabrielr@take.net',
    url='https://github.com/takenet/lime-python',
    download_url='https://github.com/takenet/lime-python/archive/v1.0.1.tar.gz',
    keywords=['lime', 'blip', 'chatbot'],
    setup_requires=["pytest-runner"],
    tests_require=['pytest'],
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
