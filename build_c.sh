gcc -c -Wall -Werror -fpic lib/waypoint.c -o lib/build/waypoint.o
gcc -shared -o lib/build/libwaypoint.so lib/build/waypoint.o

g++ -c -Wall -Werror -fpic lib/waypoint.cpp -o lib/build/waypoint_cpp.o
g++ -shared -o lib/build/libwaypoint_cpp.so lib/build/waypoint_cpp.o