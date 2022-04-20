INCLUDE_DIRECTORIES(${goollie_SOURCE_DIR}/include)

#the following block of code is an example of how to build an executable in
#cmake.  Unmodified, it will add an executable called "MyExe" to the project.
#MyExe will be built using the files MyClass.h and MyClass.cxx, and it will
#be linked to all the libraries you specified above. 
#You can build more than one executable per project
SET(CurrentExe "../GoOllie")
ADD_EXECUTABLE(${CurrentExe} main.cpp)

TARGET_LINK_LIBRARIES(${CurrentExe}
-lpthread
-lz
-lutil
libtuxcap.so.4.0)

SET_TARGET_PROPERTIES(${CurrentExe}
                             PROPERTIES
                             OUTPUT_NAME "../GoOllie"
)
