# Wallpaper Resizer
Simple batch image resizing script that implements upscaling.

This project is aimed at mass converting wallpapers to a specified set of dimensions.
As I have well over 100 wallpapers, this script makes it easier for me to resize the images
to match my screen dimensions.

## Installation
Tested on Arch Linux and nothing else. This probably works on other distros as well.
### Prerequisites
This script used the program waifu2x found at this [GitHub repo](https://github.com/DeadSix27/waifu2x-converter-cpp) and was downloaded using the Arch User Repository

#### Python Modules
Idk what modules are installed by default, I'll get to this one day

### Installing
Run the `create_binary.sh` file while in the directory where this README is.
Move the `wall-resize` binary to a place where it can be executed. For example the `/usr/local/bin/` directory.

### 

## How to use
If you ever forget the syntax used for this script, use wall-resize -h for the entire syntax.

### Syntax
The arguments are the following

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message |
| -i        | The input file |
| -o        | The output directory |
| -d        | The dimensions of the rescaled image. Defaults to: 1920x1080 |
| -v        | Verbose logging |
| -m        | Move used files once they have been scaled|
| -w        | Use waifu2x scaling on smaller images (This process takes a long time) |

### Examples
To only descale images in the `~/wallpapers/` directory to 1920x1080
```
wall-resize -i ~/wallpapers/
```

To descale and upscale images to 1920x1080 in the `~/wallpapers/` directory and move them once they have done
```
wall-resize -wm -i ~/wallpapers/
```

To do everything in the last command, use the dimensions of 640x480 and move them to `~/scaled_wallpapers/` once done
```
wall-resize -wm -d 640x480 -i ~/wallpapers/ -o ~/scaled_wallpapers/
```

## License
TBA