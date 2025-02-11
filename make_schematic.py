import mcschematic
import cv2
import os
import numpy as np
import argparse
from tqdm import tqdm

def create_schematic_from_frame(frame_path, output_folder, schematic_name, x_sep, y_sep, layer_sep):

    image = cv2.imread(frame_path)
    if image is None:
        print(f"Error: Could not read image at {frame_path}")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_4bit = image_rgb // 16
    schem = mcschematic.MCSchematic()
    
    height, width = image_4bit.shape[:2]
    offset = ( 1, 0, 1)
    
    for y in range(height):
        for x in range(width):
            
            inverted_y = height - y - 1
            r, g, b = image_4bit[y, x]
            
            schem.setBlock(
                (x * x_sep + offset[0], inverted_y * y_sep + offset[1], 0 * layer_sep + offset[2]),
                mcschematic.BlockDataDB.BARREL._barrelSS[r]
            )
            
            schem.setBlock(
                (x * x_sep + offset[0], inverted_y * y_sep + offset[1], -1 * layer_sep + offset[2]),
                mcschematic.BlockDataDB.BARREL._barrelSS[g]
            )
            
            schem.setBlock(
                (x * x_sep + offset[0], inverted_y * y_sep + offset[1], -2 * layer_sep + offset[2]),
                mcschematic.BlockDataDB.BARREL._barrelSS[b]
            )
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    schem.save(output_folder, schematic_name, mcschematic.Version.JE_1_19_2)
    print(f"Created schematic: {schematic_name}")

def process_frames_folder(frames_folder, output_folder, x_sep, y_sep, layer_sep):
    if not os.path.exists(frames_folder):
        print(f"Error: Frames folder {frames_folder} does not exist")
        return
    
    for filename in tqdm(sorted(os.listdir(frames_folder))):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            frame_index = int(filename.split('_')[-1].split('.')[0])
            frame_path = os.path.join(frames_folder, filename)
            schematic_name = f"frame_{frame_index:04d}"
            create_schematic_from_frame(frame_path, output_folder, schematic_name, x_sep, y_sep, layer_sep)

def main():
    parser = argparse.ArgumentParser(description='Convert video frames to Minecraft schematics using barrels')
    parser.add_argument('--input', '-i', required=True,
                      help='Input folder containing the frames')
    parser.add_argument('--output', '-o', required=True,
                      help='Output folder for schematics')
    parser.add_argument('--x-separation', '-x', type=int, default=1,
                      help='Horizontal separation between pixels (default: 1)')
    parser.add_argument('--y-separation', '-y', type=int, default=1,
                      help='Vertical separation between pixels (default: 1)')
    parser.add_argument('--layer-separation', '-l', type=int, default=2,
                      help='Z-axis separation between RGB layers (default: 2)')
    
    args = parser.parse_args()
    process_frames_folder(args.input, args.output, 
                        args.x_separation, args.y_separation, args.layer_separation)

if __name__ == "__main__":
    main()