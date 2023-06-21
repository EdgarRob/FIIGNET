# File to run entire pipeline for the user 
# Be sure to fix the directories to where you would like them to go.

import subprocess
import argparse

def main(use_gpu, model, disease):
    raw_data_path = "/home/ugrad/serius/edgarrobitaille/test"
    raw_data_enhanced_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/raw_image_enhanced"
    resized_data_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/unprocessed/resized"
    yolo_weights = "/home/ugrad/serius/edgarrobitaille/FIIGNET/preprocessing/yolo_tracking/YOLO/runs/detect/yolov8n_results2/weights/best.pt"
    cropped_data_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/unprocessed/segmented"
    cropped_data_enhanced_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/crop_enhanced"
    esrgan_output_path_raw = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/ESRGAN_output/raw"
    esrgan_output_path_enhanced = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/ESRGAN_output/enhanced"
    square_resized_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/square_resize"

    height = 512
    width = 512

    commands = [
        f"make enhance input_dir={raw_data_path} output_dir={raw_data_enhanced_path}",
        f"make resize input_path={raw_data_enhanced_path} output_path={resized_data_path}",
        f"make segment input_path={resized_data_path} weights={yolo_weights} height={height} width={width} output_path={cropped_data_path}",
        f"make enhance input_dir={cropped_data_path} output_dir={cropped_data_enhanced_path}",
        f"make esrgan input_dir={cropped_data_enhanced_path} output_dir={esrgan_output_path_raw}",
        f"make enhance input_dir={esrgan_output_path_raw} output_dir={esrgan_output_path_enhanced}",
        f"make resize input_path={esrgan_output_path_enhanced} output_path={square_resized_path} height={height} width={width}"
    ]

    # Run each command in sequence
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  # wait for the process to terminate

        if process.returncode != 0:
            print(f"Command '{command}' failed with return code: {process.returncode}")
            break

    if use_gpu:
        pass
    else:
        print("A high-performance GPU is needed to train the GAN, such as a NVIDIA Tesla P100 GPU or better. Please refer to the instructions in the README.md file for more information. ")

    if model == 'gan' and use_gpu:
        print("Running GAN code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
       
    elif model == 'stable_diffusion' and use_gpu:
        print("Running Stable Diffusion code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
        
    elif model == 'cvae' and use_gpu:
        print("Running CVAE code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
       
    elif model == 'fiignet' and use_gpu:
        print("Running FIIGNET code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass

    print("Full pipeline complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--gpu', dest='gpu', action='store_true',
                        help='use GPU for processing')

    # Model group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gan', dest='model', action='store_const', const='gan',
                        help='run GAN model')
    group.add_argument('--stable_diffusion', dest='model', action='store_const', const='stable_diffusion',
                        help='run Stable Diffusion model')
    group.add_argument('--cvae', dest='model', action='store_const', const='cvae',
                        help='run CVAE model')
    group.add_argument('--fiignet', dest='model', action='store_const', const='fiignet',
                        help='run FIIGNET model')

    # Diseases group
    group_diseases = parser.add_mutually_exclusive_group(required=True)
    group_diseases.add_argument('--ich', dest='disease', action='store_const', const='ich',
                        help='run code for ICH')
    group_diseases.add_argument('--red_spot', dest='disease', action='store_const', const='red_spot',
                        help='run code for Red Spot')

    args = parser.parse_args()
    main(args.gpu, args.model, args.disease)




