gcc -c -Wall -Werror -fpic lib/waypoint.c -o lib/build/waypoint.o -I /opt/homebrew/Caskroom/miniconda/base/envs/pygui/bin/python
gcc -shared -o lib/build/libwaypoint.so lib/build/waypoint.o

g++ -c -Wall -Werror -fpic lib/waypoint.cpp -o lib/build/waypoint_cpp.o -I /opt/homebrew/Caskroom/miniconda/base/envs/pygui/bin/python
g++ -shared -o lib/build/libwaypoint_cpp.so lib/build/waypoint_cpp.o