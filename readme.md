# Video to Minecraft Schematic Converter

This project converts video files into a sequence of Minecraft schematics, where each frame is represented using colored barrels. The conversion process involves downscaling the video, extracting frames, quantizing colors, and generating Minecraft schematics that can be imported into the game.

## Features

- Video downscaling with customizable resolution
- Frame extraction with target FPS control
- Color quantization (4-bit color depth per channel)
- Automatic schematic generation using colored barrels
- Maintains aspect ratio option
- Configurable pixel spacing in all dimensions

## Prerequisites

- Python 3.8+
- OpenCV (cv2)
- mcschematic
- NumPy
- tqdm

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/video_to_schematic.git
cd video_to_schematic
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

The conversion process happens in two steps:

### 1. Video Processing

First, process your video file using `main.py`:

```bash
python main.py input_video.mp4 --width 64 --height 64 --fps 30 --bits 4 --output-dir output
```

Arguments:
- `input_video`: Path to your input video file
- `--width`: Target frame width (default: 64)
- `--height`: Target frame height (default: 64)
- `--fps`: Target frames per second (optional)
- `--keep-aspect-ratio`: Maintain original aspect ratio
- `--bits`: Bits per color channel for quantization (default: 4)
- `--output-dir`: Output directory (default: 'processed')

### 2. Schematic Creation

Then, convert the processed frames to Minecraft schematics using `make_schematic.py`:

```bash
python make_schematic.py -i output/quantized -o frame_schematics -x 1 -y 1 -l 2
```

Arguments:
- `-i, --input`: Input folder containing the processed frames
- `-o, --output`: Output folder for schematics
- `-x, --x-separation`: Horizontal separation between pixels (default: 1)
- `-y, --y-separation`: Vertical separation between pixels (default: 1)
- `-l, --layer-separation`: Z-axis separation between RGB layers (default: 2)

## Output Structure

```
video_to_schematic/
├── output/
│   ├── frames/        # Extracted video frames
│   └── quantized/     # Color-quantized frames
└── frame_schematics/  # Generated Minecraft schematics
```

## Schematic Structure

Each frame is converted into a Minecraft schematic with the following properties:

- RGB channels are separated into three layers
- Each pixel is represented by three barrels (one for each color channel)
- Colors are quantized to 4 bits (16 levels) per channel
- Barrels are placed with configurable spacing for better visibility

## Minecraft Compatibility

The generated schematics are compatible with Minecraft Java Edition 1.19.2. You'll need a schematic loader mod or WorldEdit to import them into your world.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

[Your chosen license]

## Acknowledgments

- Built using the mcschematic library
- Uses OpenCV for video processing
- Inspired by [any relevant projects or inspirations]