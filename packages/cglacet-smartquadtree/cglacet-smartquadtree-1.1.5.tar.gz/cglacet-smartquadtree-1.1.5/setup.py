from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize, build_ext

extensions = [
    Extension(
        "smartquadtree",
        ["smartquadtree.pyx", "quadtree.cpp", "neighbour.cpp"],
        extra_compile_args=["-std=c++11"],
        language="c++"
    )
]

def get_long_description():
    import codecs
    with codecs.open('tutorial.rst', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(
    name="cglacet-smartquadtree",
    version="1.1.5",
    author="Xavier Olive",
    author_email="xavier@xoolive.org",
    description="Implementation of quadtrees for moving objects",
    long_description=get_long_description(),
    license="MIT",
    url="https://github.com/cglacet/quadtree",
    packages = find_packages(),
    ext_modules=cythonize(extensions),
    data_files=[('.', ['tutorial.rst', ])],
    include_package_data=True,
    cmdclass = {
        "build_ext": build_ext
    }
)

# Producing long description
# ipython nbconvert tutorial.ipynb --to rst
# Then manually edit paths to images to point to github

# Windows compilation (mingw)
# edit smartquadtree.cpp
# add #include <cmath> at the top of the file before #include "pyconfig.h"
