# Wallpaper Resizer
![Run Tests](https://github.com/slapelachie/wall-resize/workflows/Run%20Tests/badge.svg)

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
```
$ git clone https://github.com/slapelachie/wall-resize
$ cd wall-resize
$ pip install .
```

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
| -w        | Use waifu2x scaling on smaller images (This process takes a long time) |
| --replace | Replaces the inputed file once scaled |
| --progress| Displays the progress of the scaling |


### Examples
To only descale images in the `~/wallpapers/` directory to 1920x1080
```
wall-resize -i ~/wallpapers/
```

To descale and upscale images to 1920x1080 in the `~/wallpapers/` directory and move them once they have done
```
wall-resize --replace -wi ~/wallpapers/
```

To do everything in the last command, use the dimensions of 640x480 and move them to `~/scaled_wallpapers/` once done
```
wall-resize -d 640x480 -wi ~/wallpapers/ -o ~/scaled_wallpapers/
```

## License
Using the [GNU GPLv2](LICENSE) license
