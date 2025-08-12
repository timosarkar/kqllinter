git clone https://github.com/capstone-engine/capstone --depth=1
cd capstone
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCAPSTONE_BUILD_SHARED_LIBS=ON
make -j
sudo make install -j
cd ..
nim c --passL:"-L/usr/local/lib -lcapstone -Wl,-rpath,/usr/local/lib" -r example.nim

