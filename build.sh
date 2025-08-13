git clone https://github.com/capstone-engine/capstone --depth=1
cd capstone
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCAPSTONE_BUILD_SHARED_LIBS=ON
make -j
sudo make install -j
cd ../../

git clone https://github.com/keystone-engine/keystone --depth=1
cd keystone
mkdir -p build
cd build
../make-share.sh
#cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON
make -j
sudo make install -j
cd ../..

nim c --passL:"-L/usr/local/lib -lcapstone -lkeystone -Wl,-rpath,/usr/local/lib" -d:nimDebugDlOpen -r main.nim

