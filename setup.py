from setuptools import setup, find_packages

setup(
    name='zanim_tools',
    version='1.0.0',
    description='Game character animation tools for Blender',
    long_description=open('README.md').read(),
    author='Gary Tierney',
    author_email='gary.tierney@fastmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    packages=find_packages(),
    keywords='blender',
    install_requires=[],
    package_data={'': ['VERSION']},
    include_package_data=True
)