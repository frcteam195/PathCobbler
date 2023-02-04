# PathCobbler

- [PathCobbler](#pathcobbler)
  - [To run this project on Mac](#to-run-this-project-on-mac)
  - [To run this project on Linux x86\_64 (Ubuntu)](#to-run-this-project-on-linux-x86_64-ubuntu)
  - [To run this project on Windows](#to-run-this-project-on-windows)
  - [To run this project on Linux arm64/aarch64 (Ubuntu)](#to-run-this-project-on-linux-arm64aarch64-ubuntu)

___

## To run this project on Mac

First, ensure that [Homebrew is installed](https://brew.sh/) and that you have installed the Mac command line dev tools (this should happen as part of the brew install).

After installing brew, make sure to add it to your PATH in ~/.zprofile by doing the following in a new terminal:
```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Now that brew is installed and set up, close the terminal and reopen it so that your new PATH variable will take effect.
```
cd PathCobbler
brew install python
brew install cmake
python3 -m ensurepip
pip3 install -r requirements.txt
./build_c.sh
```

Now that you have successfully built the C++ bindings for the project, you can run the main.py to launch it:
```
python3 main.py
```
___

## To run this project on Linux x86_64 (Ubuntu)

Run the following commands in a terminal
```
sudo apt update
sudo apt install build-essential cmake python3 python3-pip
cd PathCobbler
python3 -m ensurepip
pip3 install -r requirements.txt
./build_c.sh
```

Now that you have successfully built the C++ bindings for the project, you can run the main.py to launch it:
```
python3 main.py
```
___

## To run this project on Windows

Download and install [python3](https://www.python.org/downloads/).
Ensure that during the installation, you choose to add python3 to your path.

Open a new administrative Command Prompt window and type the following commands:
```
python3 -m ensurepip
cd PathCobbler
pip3 install -r requirements.txt
```

Download and install [cmake](https://cmake.org/download/)

Download and install [MinGW](https://osdn.net/projects/mingw/)

Open a MinGW shell and navigate to the PathCobbler folder. Now run the following commands:
```
./build_c_win.sh
```
Now close the MinGW shell.

In the Command Prompt, navigate to the PathCobbler folder and run the following command:
```
python3 main.py
```

___

## To run this project on Linux arm64/aarch64 (Ubuntu)

Run the following commands in a terminal
```
sudo apt update
sudo apt install build-essential cmake python3 python3-pip
python3 -m ensurepip
```

Now, follow the instructions for [building the required modules from source](install_pyside.md).

Once these modules have been successfully installed, you can proceed to build the C++ bindings:
```
cd PathCobbler
./build_c.sh
```

Now that you have successfully built the C++ bindings for the project, you can run the main.py to launch it:
```
python3 main.py
```