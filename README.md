# Info

This repository is forked from https://github.com/lasote/conan-gtest. 

It is mainly for testing and evaluation purposes. If you need a tested and maintained release please switch to https://github.com/lasote/conan-gtest. 

# conan-gtest

[Conan.io](https://conan.io) package for Google test library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/googletest/1.8.0/kwallner/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ conan create . kwallner/testing

## Upload packages to server

    $ conan upload googletest/1.10.0@kwallner/testing --all

## Reuse the packages

### Basic setup

    $ conan install googletest/1.10.0@kwallner/testing

### Project setup

If you handle multiple dependencies in your project, it would be better to add a *conanfile.txt*

    [requires]
    googletest/1.10.0@kwallner/testing

    [options]


    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files `conanbuildinfo.txt` and `conanbuildinfo.cmake` with all the necessary paths and variables
needed to link with the other dependencies.

