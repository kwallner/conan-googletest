# Info

This repository is forked from https://github.com/lasote/conan-gtest. 

It is mainly for testing and evaluation purposes. If you need a tested and maintained release please switch to https://github.com/lasote/conan-gtest. 

# conan-gtest

[Conan.io](https://conan.io) package for Google test library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/gtest/1.8.0/kwallner/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ conan create . kwallner/stable

## Upload packages to server

    $ conan upload gtest/1.8.1@kwallner/stable --all

## Reuse the packages

### Basic setup

    $ conan install gtest/1.8.1@kwallner/stable

### Project setup

If you handle multiple dependencies in your project, it would be better to add a *conanfile.txt*

    [requires]
    gtest/1.8.1@kwallner/stable

    [options]


    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files `conanbuildinfo.txt` and `conanbuildinfo.cmake` with all the necessary paths and variables
needed to link with the other dependencies.

