if [[ $1 == clean ]]; then
    rm -Rf lib/build
    exit 0
fi

mkdir -p lib/build
cd lib/build

if [ ! -f "Makefile" ]; then
    cmake ..
fi

make
