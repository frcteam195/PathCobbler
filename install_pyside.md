1. Install the apt dependencies:
```bash
sudo apt install -y \
  build-essential \
  cmake \
  curl \
  git \
  clang \
  libclang-dev \
  libfontconfig-dev \
  libfreetype-dev \
  libglib2.0-dev \
  libgl-dev \
  libgl1-mesa-dev \
  libice-dev \
  libsm-dev \
  libssl-dev \
  libx11-dev \
  libx11-xcb-dev \
  libxcb1-dev \
  libxcb-glx0-dev \
  libxcb-icccm4-dev \
  libxcb-image0-dev \
  libxcb-xinput-dev \
  libxcb-keysyms1-dev \
  libxcb-randr0-dev \
  libxcb-render-util0-dev \
  libxcb-render0-dev \
  libxcb-shape0-dev \
  libxcb-shm0-dev \
  libxcb-sync-dev \
  libxcb-util-dev \
  libxcb-xfixes0-dev \
  libxcb-xinerama0-dev \
  libxcb-xinput-dev \
  libxcb-xkb-dev \
  libxext-dev \
  libxfixes-dev \
  libxi-dev \
  libxkbcommon-dev \
  libxkbcommon-x11-dev \
  libxrender-dev \
  ninja-build
```

2. (Optional) Install a custom Python version
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9-dev python3.9-venv
```

3. Download and unzip Qt source code
```bash
cd ~
curl -O -L https://download.qt.io/archive/qt/6.4/6.4.0/single/qt-everywhere-src-6.4.0.tar.xz
tar -xf qt-everywhere-src-6.4.0.tar.xz
```

4. Setup Qt build directory
```bash
cd qt-everywhere-src-6.4.0/
mkdir qt6-build
cd qt6-build/
```

5. Configure and build Qt
```bash
../configure
cmake --build . --parallel 4
```

6. Install Qt
```bash
sudo cmake --install .
```

7. Setup a `venv` for doing the PySide build and install. Make sure to use the Python version installed in step 2.
```bash
cd ~
python3.9 -m venv pyside-venv
source pyside-venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

8. Get the PySide source code
```bash
git clone https://code.qt.io/pyside/pyside-setup
```

9. Checkout the tag matching the version of the installed Qt
```bash
cd pyside-setup
git checkout 6.4
```

10. Build PySide
```bash
python -m pip install -r requirements.txt
python setup.py build \
  --qtpaths=/usr/local/Qt-6.4.0/bin/qtpaths \
  --ignore-git \
  --parallel 4 \
  --standalone 
```

11. (Optional) Build the wheels and place in `pyside-setup/dist_new/`
```bash
ln -s build/pyside-venv/ build/pyside-venva
python create_wheels.py
```

12. (Optional) Install PySide to the current venv
```bash
python setup.py install \
  --qtpaths=/usr/local/Qt-6.4.0/bin/qtpaths \
  --ignore-git \
  --parallel 4 \
  --standalone \
  --reuse-build
```