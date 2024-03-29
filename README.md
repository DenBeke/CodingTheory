GoEnigma
========

[![Build Status](https://magnum.travis-ci.com/DenBeke/CodingTheory.svg?token=55DZWEWREsf4wvhULGzt)](https://magnum.travis-ci.com/DenBeke/CodingTheory)

An enigma machine written in Go


Cloning
-------

### go get

Let Go clone the repo into the correct directory:

    $ go get github.com/DenBeke/CodingTheory

### git clone

You can also Git clone the repo, but then you need to manually set the correct path.  
Repo should be cloned in `$GOPATH/src/github.com/DenBeke/CodingTheory`.


Build
-----

Build:

    $ go build

Run:

    $ ./GoEnigma input.json


Testing
-------

Unit tests depend on [GoConvey](https://github.com/smartystreets/goconvey), so install the dependencies first:

    $ go get github.com/smartystreets/goconvey
    $ go get github.com/smartystreets/assertions

Run the unit tests

    $ go test ./... -v


Formatting code
---------------

Always format the code before you commit/push!

    $ gofmt -l -w .
