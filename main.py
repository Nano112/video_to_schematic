import cv2
import os
import numpy as np
import argparse
from typing import Tuple, Optional

class VideoProcessor:
    def __init__(self, input_path: str, output_base_dir: str = "processed"):
        
        self.input_path = input_path
        self.output_base_dir = output_base_dir
        self.frames_dir = os.path.join(output_base_dir, "frames")
        self.quantized_dir = os.path.join(output_base_dir, "quantized")
        
        for directory in [self.output_base_dir, self.frames_dir, self.quantized_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def calculate_new_dimensions(self, target_width: int, target_height: int, 
                               original_width: int, original_height: int, 
                               keep_aspect_ratio: bool) -> Tuple[int, int]:
        if not keep_aspect_ratio:
            return target_width, target_height
        
        original_aspect = original_width / original_height
        target_aspect = target_width / target_height
        
        if original_aspect > target_aspect:
            # Width is the limiting factor
            new_width = target_width
            new_height = int(target_width / original_aspect)
        else:
            # Height is the limiting factor
            new_height = target_height
            new_width = int(target_height * original_aspect)
            
        return new_width, new_height

    def downscale(self, target_width: int, target_height: int, 
                  target_fps: Optional[int] = None, keep_aspect_ratio: bool = False) -> None:
        
        video = cv2.VideoCapture(self.input_path)
        original_fps = video.get(cv2.CAP_PROP_FPS)
        original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        frame_interval = 1
        if target_fps and target_fps < original_fps:
            frame_interval = int(original_fps / target_fps)
        
        new_width, new_height = self.calculate_new_dimensions(
            target_width, target_height,
            original_width, original_height,
            keep_aspect_ratio
        )
        
        frame_count = 0
        frame_index = 0
        
        while True:
            success, frame = video.read()
            if not success:
                break
            
            if frame_index % frame_interval != 0:
                frame_index += 1
                continue
            
            resized_frame = cv2.resize(frame, (new_width, new_height))
            
            output_path = os.path.join(self.frames_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(output_path, resized_frame)
            
            frame_count += 1
            frame_index += 1
            
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")
        
        video.release()
        print(f"Extracted {frame_count} frames at {new_width}x{new_height}")

    def quantize(self, bits_per_channel: int = 4) -> None:

        levels = 2 ** bits_per_channel
        divider = 256 // levels
        
        frame_count = 0
        for filename in sorted(os.listdir(self.frames_dir)):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.frames_dir, filename)
                frame = cv2.imread(image_path)
                
                quantized_frame = (frame // divider) * divider
                
                output_path = os.path.join(self.quantized_dir, f"quantized_{filename}")
                cv2.imwrite(output_path, quantized_frame)
                
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"Quantized {frame_count} frames...")
        
        print(f"Quantized {frame_count} frames to {bits_per_channel} bits per channel")

def main():
    parser = argparse.ArgumentParser(description='Process video with downscaling and color quantization')
    parser.add_argument('input_video', help='Path to input video file')
    parser.add_argument('--width', type=int, default=64, help='Target width')
    parser.add_argument('--height', type=int, default=64, help='Target height')
    parser.add_argument('--fps', type=int, help='Target FPS (optional)')
    parser.add_argument('--keep-aspect-ratio', action='store_true', help='Maintain aspect ratio')
    parser.add_argument('--bits', type=int, default=4, help='Bits per color channel for quantization')
    parser.add_argument('--output-dir', default='processed', help='Base output directory')
    
    args = parser.parse_args()
    
    processor = VideoProcessor(args.input_video, args.output_dir)
    
    print("Starting frame extraction and resizing...")
    processor.downscale(args.width, args.height, args.fps, args.keep_aspect_ratio)
    
    print("\nStarting color quantization...")
    processor.quantize(args.bits)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()