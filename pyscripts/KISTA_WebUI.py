skip_install_system = True
skip_install        = False
webui_version = "v2.5"

import os
os.makedirs('/content', exist_ok=True)
os.makedirs('/content/drive', exist_ok=True)
os.makedirs('/content/drive/MyDrive', exist_ok=True)
os.makedirs('/content/drive/MyDrive/docs', exist_ok=True)
os.makedirs('/content/drive/MyDrive/models', exist_ok=True)
os.makedirs('/content/drive/MyDrive/controlnet', exist_ok=True)
os.makedirs('/content/drive/MyDrive/output', exist_ok=True)
os.makedirs('/content/drive/MyDrive/models', exist_ok=True)

#
# 3/8 : DEFINING PATHS
#
KISTA_DRIVE_PATHS = "/content/drive/MyDrive/docs"
DEFAULT_CHECKPOINTS_FOLDER = '/content/drive/MyDrive/models'
DEFAULT_CONTROLNET_FOLDER  = '/content/drive/MyDrive/controlnet'
WEBUI_ROOT = '/content'
WEBUI_FOLDER = 'stable-diffusion-webui'
WEBUI_PATH = os.path.join(WEBUI_ROOT, WEBUI_FOLDER)
CLONE_ARG = "clone --depth 1"

ext_bulk_controllnet = True
ext_inf_img_browsing = True
ext_bulk_two = False
ext_bulk_one = False
ext_bulk_three = True
ext_cozy_nest = False

hf_read_token = ''
path_cpkt = ''
dir__models = '/content/drive/MyDrive/models'
dir__controlnet = '/content/drive/MyDrive/controlnet'
dir__outdir_samples = '/content/drive/MyDrive/output'
dir__outdir_grids = '/content/drive/MyDrive/output'
task__cache_controlnet = True
task__cache_checkpoints = True
sources__copy_lauras = ''
sources__copy_textual_inversion = ''
dir__extra_loras_search = ''

#
#
#


import tarfile; import os; import shutil; import json;
from pathlib import Path
from ipywidgets import widgets, GridspecLayout, Layout
from configparser import ConfigParser
from IPython.display import display, Markdown, clear_output
from tqdm import tqdm
wget https://raw.githubusercontent.com/L0garithmic/fastcolabcopy/main/fastcopy.py
import fastcopy

#
# 1/8 : DEFINING FUNCTIONS
#
_B=True
_A=False
def return__isValidDir(directory):
    if os.path.isdir(directory):return _B
    else:return _A
def return__isValidFile(file_path):
    if os.path.isfile(file_path):return _B
    else:return _A
def do_we_need_to_download_checkpoint():
    if return__isValidFile(path_cpkt):return _A
    if return__isValidDir(dir__models) and find_checkpoint_file(dir__models)!='':return _A
    return _B
def copy_sources(destination_dir, string_sources):
    sources=[source.strip()for source in string_sources.split(',')]
    for source in sources:
        if os.path.exists(source):
            if os.path.isfile(source):shutil.copy2(source,destination_dir);print(f"Copied file: {source}")
            elif os.path.isdir(source):shutil.copytree(source,os.path.join(destination_dir,os.path.basename(source)), dirs_exist_ok=True);print(f"Copied directory: {source}")
            else:print(f"Ignored invalid source: {source}")
        else:print(f"Ignored non-existent source: {source}")
def copy_files__directory(source_dir, destination_dir):
    file_names = os.listdir(source_dir)
    for file_name in file_names:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        shutil.copy2(source_path, destination_path)
        print(f"Copied file: {file_name}")
def find_checkpoint_file(directory):
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".ckpt") or filename.endswith(".safetensors"):
                return os.path.join(directory, filename)
    return ""
def createFile__ifNotExist(directory, filename_to_look_for, file_contents):
    env_file_path = os.path.join(directory, filename_to_look_for)
    if not os.path.isfile(env_file_path):
        with open(env_file_path, 'w') as env_file:
            env_file.write(file_contents)
            print(f"Created {filename_to_look_for} in {directory}")
def calculate_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size
def return__bytesToMb(size_in_bytes):
    size_in_mb = size_in_bytes / 1024 / 1024
    return f'{int(size_in_mb)} MB'
def display__dirTotalSize(directory):
    print(f'Total: {return__bytesToMb(calculate_directory_size(directory))} for dir {directory}')
def do_dir_contain_controlnet_models(directory):
    if not return__isValidDir(directory):return _A
    if calculate_directory_size(directory)>10000000000:return _B
    else:return _A
def strtobool (val):
    val=val.lower()
    if val in('y','yes','t','true','on','1'):return _B
    elif val in('','n','no','f','false','off','0'):return _A
    else:raise ValueError('invalid truth value %r'%(val,))
def getValue (savedconf, key, type):
    try:val=savedconf[key]
    except KeyError:val=''
    if type=='bool':return strtobool(val)
    else:return val
def openReplaceStringMatch(file_path, match, replace):
    if not os.path.isfile( file_path ):
        print(f'Error opening file: {file_path}')
    else:
        modified_lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if match in line:
                    line = line.replace(match, replace)
                modified_lines.append(line)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(modified_lines))
def commentOutLinesStartingWith(file_path, matches, comment_str='# '):
    if not os.path.isfile( file_path ):
        print(f'Error opening file: {file_path}')
    else:
        modified_lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line
                uncomment = False
                for match in matches:
                    if line.strip().startswith(match):
                        print(f'Match: {match}')
                        uncomment = True
                if uncomment:
                    line = comment_str + line.strip() + "\n"
                modified_lines.append(line)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(modified_lines))
def create_empty_file(file_path):
    with open(file_path, 'a'):
        print(f"File created: {file_path}")
def move_single_file(source_file, destination_file, copyOnly=False):
    file_size = os.path.getsize(source_file)

    with open(source_file, "rb") as src_file, \
         open(destination_file, "wb") as dest_file, \
         tqdm(total=file_size, unit="B", unit_scale=True, desc="Moving file", ncols=80) as progress:

        chunk_size = 1024 * 1024  # 1 MB
        bytes_copied = 0

        while True:
            chunk = src_file.read(chunk_size)

            if not chunk:
                break

            dest_file.write(chunk)
            bytes_copied += len(chunk)
            progress.update(len(chunk))

    if not copyOnly:
        os.remove(source_file)
        print(f"File '{source_file}' moved to '{destination_file}'.")
    else:
        print(f"File '{source_file}' copied to '{destination_file}'.")


# make sure dir exists, boolean return
def dir_is_ok(directory):
    if directory and os.path.isdir(directory):
        return True
    elif directory:
        try:
            os.makedirs(directory)
            return True
        except OSError as e:
            print(f"Error creating directory: {e}")
            return False
    else:
        return False




# Download all ControlNet models from huggingface
def download_all_control_models():
    if hf_read_token is not None and hf_read_token != '':
        HF_TOKEN = {hf_read_token}
    mkdir /content/huggface_cache
    huggingface-cli login --token {HF_TOKEN}
    from huggingface_hub import snapshot_download
    # bloated repository ckpt/ControlNet-v1-1
    path = snapshot_download(repo_id="lllyasviel/ControlNet-v1-1", repo_type="model", revision="main", local_dir=f"{WEBUI_PATH}/extensions/sd-webui-controlnet/models", local_dir_use_symlinks=False)
    path = snapshot_download(repo_id="TencentARC/T2I-Adapter", repo_type="model", revision="main", local_dir=f"{WEBUI_PATH}/extensions/sd-webui-controlnet", local_dir_use_symlinks=False, allow_patterns="models/*")
    wget --content-disposition https://huggingface.co/spaces/LiheYoung/Depth-Anything/resolve/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/CiaraRowles/TemporalNet/blob/main/diff_control_sd15_temporalnet_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    clear_output()
    print(f'All ControlNet models downloaded...')
    return 1


def write_json_to_file(json_string, file_path):
    try:
        # Try to parse the JSON string to validate it
        json_data = json.loads(json_string)

        # Write the JSON data to the specified file
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=2)

        print(f"JSON data successfully written to {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")

def write_ui_config(json_string):
    inip = Path(f'{WEBUI_PATH}/ui-config.json')
    if not inip.is_file():
        write_json_to_file('{' + json_string + '}', f'{WEBUI_PATH}/ui-config.json')
    else:
        print(f"ui-config.json already exists.")

json_adetailer = '''
    "customscript/!adetailer.py/txt2img/Enable ADetailer/visible": true,
    "customscript/!adetailer.py/txt2img/Enable ADetailer/value": false,
    "customscript/!adetailer.py/txt2img/Skip img2img/value": false,
    "txt2img/ADetailer model/visible": true,
    "txt2img/ADetailer model/value": "face_yolov8n.pt",
    "txt2img/ad_prompt/visible": true,
    "txt2img/ad_prompt/value": "",
    "txt2img/ad_negative_prompt/visible": true,
    "txt2img/ad_negative_prompt/value": "",
    "txt2img/Detection model confidence threshold/visible": true,
    "txt2img/Detection model confidence threshold/value": 0.3,
    "txt2img/Detection model confidence threshold/minimum": 0.0,
    "txt2img/Detection model confidence threshold/maximum": 1.0,
    "txt2img/Detection model confidence threshold/step": 0.01,
    "txt2img/Mask only the top k largest (0 to disable)/visible": true,
    "txt2img/Mask only the top k largest (0 to disable)/value": 0,
    "txt2img/Mask only the top k largest (0 to disable)/minimum": 0,
    "txt2img/Mask only the top k largest (0 to disable)/maximum": 10,
    "txt2img/Mask only the top k largest (0 to disable)/step": 1,
    "txt2img/Mask min area ratio/visible": true,
    "txt2img/Mask min area ratio/value": 0.0,
    "txt2img/Mask min area ratio/minimum": 0.0,
    "txt2img/Mask min area ratio/maximum": 1.0,
    "txt2img/Mask min area ratio/step": 0.001,
    "txt2img/Mask max area ratio/visible": true,
    "txt2img/Mask max area ratio/value": 1.0,
    "txt2img/Mask max area ratio/minimum": 0.0,
    "txt2img/Mask max area ratio/maximum": 1.0,
    "txt2img/Mask max area ratio/step": 0.001,
    "txt2img/Mask x(\u2192) offset/visible": true,
    "txt2img/Mask x(\u2192) offset/value": 0,
    "txt2img/Mask x(\u2192) offset/minimum": -200,
    "txt2img/Mask x(\u2192) offset/maximum": 200,
    "txt2img/Mask x(\u2192) offset/step": 1,
    "txt2img/Mask y(\u2191) offset/visible": true,
    "txt2img/Mask y(\u2191) offset/value": 0,
    "txt2img/Mask y(\u2191) offset/minimum": -200,
    "txt2img/Mask y(\u2191) offset/maximum": 200,
    "txt2img/Mask y(\u2191) offset/step": 1,
    "txt2img/Mask erosion (-) / dilation (+)/visible": true,
    "txt2img/Mask erosion (-) / dilation (+)/value": 4,
    "txt2img/Mask erosion (-) / dilation (+)/minimum": -128,
    "txt2img/Mask erosion (-) / dilation (+)/maximum": 128,
    "txt2img/Mask erosion (-) / dilation (+)/step": 4,
    "txt2img/Mask merge mode/visible": true,
    "txt2img/Mask merge mode/value": "None",
    "txt2img/Inpaint mask blur/visible": true,
    "txt2img/Inpaint mask blur/value": 4,
    "txt2img/Inpaint mask blur/minimum": 0,
    "txt2img/Inpaint mask blur/maximum": 64,
    "txt2img/Inpaint mask blur/step": 1,
    "txt2img/Inpaint denoising strength/visible": true,
    "txt2img/Inpaint denoising strength/value": 0.4,
    "txt2img/Inpaint denoising strength/minimum": 0.0,
    "txt2img/Inpaint denoising strength/maximum": 1.0,
    "txt2img/Inpaint denoising strength/step": 0.01,
    "txt2img/Inpaint only masked/visible": true,
    "txt2img/Inpaint only masked/value": true,
    "txt2img/Inpaint only masked padding, pixels/visible": true,
    "txt2img/Inpaint only masked padding, pixels/value": 32,
    "txt2img/Inpaint only masked padding, pixels/minimum": 0,
    "txt2img/Inpaint only masked padding, pixels/maximum": 256,
    "txt2img/Inpaint only masked padding, pixels/step": 4,
    "txt2img/Use separate width/height/visible": true,
    "txt2img/Use separate width/height/value": false,
    "txt2img/inpaint width/visible": true,
    "txt2img/inpaint width/value": 512,
    "txt2img/inpaint width/minimum": 64,
    "txt2img/inpaint width/maximum": 2048,
    "txt2img/inpaint width/step": 4,
    "txt2img/inpaint height/visible": true,
    "txt2img/inpaint height/value": 512,
    "txt2img/inpaint height/minimum": 64,
    "txt2img/inpaint height/maximum": 2048,
    "txt2img/inpaint height/step": 4,
    "txt2img/Use separate steps/visible": true,
    "txt2img/Use separate steps/value": false,
    "txt2img/ADetailer steps/visible": true,
    "txt2img/ADetailer steps/value": 28,
    "txt2img/ADetailer steps/minimum": 1,
    "txt2img/ADetailer steps/maximum": 150,
    "txt2img/ADetailer steps/step": 1,
    "txt2img/Use separate CFG scale/visible": true,
    "txt2img/Use separate CFG scale/value": false,
    "txt2img/ADetailer CFG scale/visible": true,
    "txt2img/ADetailer CFG scale/value": 7.0,
    "txt2img/ADetailer CFG scale/minimum": 0.0,
    "txt2img/ADetailer CFG scale/maximum": 30.0,
    "txt2img/ADetailer CFG scale/step": 0.5,
    "txt2img/Use separate checkpoint/visible": true,
    "txt2img/Use separate checkpoint/value": false,
    "txt2img/ADetailer checkpoint/visible": true,
    "txt2img/ADetailer checkpoint/value": "Use same checkpoint",
    "txt2img/Use separate VAE/visible": true,
    "txt2img/Use separate VAE/value": false,
    "txt2img/ADetailer VAE/visible": true,
    "txt2img/ADetailer VAE/value": "Use same VAE",
    "txt2img/Use separate sampler/visible": true,
    "txt2img/Use separate sampler/value": false,
    "txt2img/ADetailer sampler/visible": true,
    "txt2img/ADetailer sampler/value": "DPM++ 2M Karras",
    "txt2img/Use separate noise multiplier/visible": true,
    "txt2img/Use separate noise multiplier/value": false,
    "txt2img/Noise multiplier for img2img/visible": true,
    "txt2img/Noise multiplier for img2img/value": 1.0,
    "txt2img/Noise multiplier for img2img/minimum": 0.5,
    "txt2img/Noise multiplier for img2img/maximum": 1.5,
    "txt2img/Noise multiplier for img2img/step": 0.01,
    "txt2img/Use separate CLIP skip/visible": true,
    "txt2img/Use separate CLIP skip/value": false,
    "txt2img/ADetailer CLIP skip/visible": true,
    "txt2img/ADetailer CLIP skip/value": 1,
    "txt2img/ADetailer CLIP skip/minimum": 1,
    "txt2img/ADetailer CLIP skip/maximum": 12,
    "txt2img/ADetailer CLIP skip/step": 1,
    "txt2img/Restore faces after ADetailer/visible": true,
    "txt2img/Restore faces after ADetailer/value": false,
    "txt2img/ControlNet model/visible": true,
    "txt2img/ControlNet model/value": "None",
    "txt2img/ControlNet module/value": "None",
    "txt2img/ControlNet weight/visible": true,
    "txt2img/ControlNet weight/value": 1.0,
    "txt2img/ControlNet weight/minimum": 0.0,
    "txt2img/ControlNet weight/maximum": 1.0,
    "txt2img/ControlNet weight/step": 0.01,
    "txt2img/ControlNet guidance start/visible": true,
    "txt2img/ControlNet guidance start/value": 0.0,
    "txt2img/ControlNet guidance start/minimum": 0.0,
    "txt2img/ControlNet guidance start/maximum": 1.0,
    "txt2img/ControlNet guidance start/step": 0.01,
    "txt2img/ControlNet guidance end/visible": true,
    "txt2img/ControlNet guidance end/value": 1.0,
    "txt2img/ControlNet guidance end/minimum": 0.0,
    "txt2img/ControlNet guidance end/maximum": 1.0,
    "txt2img/ControlNet guidance end/step": 0.01,
    "txt2img/ADetailer model 2nd/visible": true,
    "txt2img/ADetailer model 2nd/value": "None",
    "txt2img/ad_prompt 2nd/visible": true,
    "txt2img/ad_prompt 2nd/value": "",
    "txt2img/ad_negative_prompt 2nd/visible": true,
    "txt2img/ad_negative_prompt 2nd/value": "",
    "txt2img/Detection model confidence threshold 2nd/visible": true,
    "txt2img/Detection model confidence threshold 2nd/value": 0.3,
    "txt2img/Detection model confidence threshold 2nd/minimum": 0.0,
    "txt2img/Detection model confidence threshold 2nd/maximum": 1.0,
    "txt2img/Detection model confidence threshold 2nd/step": 0.01,
    "txt2img/Mask only the top k largest (0 to disable) 2nd/visible": true,
    "txt2img/Mask only the top k largest (0 to disable) 2nd/value": 0,
    "txt2img/Mask only the top k largest (0 to disable) 2nd/minimum": 0,
    "txt2img/Mask only the top k largest (0 to disable) 2nd/maximum": 10,
    "txt2img/Mask only the top k largest (0 to disable) 2nd/step": 1,
    "txt2img/Mask min area ratio 2nd/visible": true,
    "txt2img/Mask min area ratio 2nd/value": 0.0,
    "txt2img/Mask min area ratio 2nd/minimum": 0.0,
    "txt2img/Mask min area ratio 2nd/maximum": 1.0,
    "txt2img/Mask min area ratio 2nd/step": 0.001,
    "txt2img/Mask max area ratio 2nd/visible": true,
    "txt2img/Mask max area ratio 2nd/value": 1.0,
    "txt2img/Mask max area ratio 2nd/minimum": 0.0,
    "txt2img/Mask max area ratio 2nd/maximum": 1.0,
    "txt2img/Mask max area ratio 2nd/step": 0.001,
    "txt2img/Mask x(\u2192) offset 2nd/visible": true,
    "txt2img/Mask x(\u2192) offset 2nd/value": 0,
    "txt2img/Mask x(\u2192) offset 2nd/minimum": -200,
    "txt2img/Mask x(\u2192) offset 2nd/maximum": 200,
    "txt2img/Mask x(\u2192) offset 2nd/step": 1,
    "txt2img/Mask y(\u2191) offset 2nd/visible": true,
    "txt2img/Mask y(\u2191) offset 2nd/value": 0,
    "txt2img/Mask y(\u2191) offset 2nd/minimum": -200,
    "txt2img/Mask y(\u2191) offset 2nd/maximum": 200,
    "txt2img/Mask y(\u2191) offset 2nd/step": 1,
    "txt2img/Mask erosion (-) / dilation (+) 2nd/visible": true,
    "txt2img/Mask erosion (-) / dilation (+) 2nd/value": 4,
    "txt2img/Mask erosion (-) / dilation (+) 2nd/minimum": -128,
    "txt2img/Mask erosion (-) / dilation (+) 2nd/maximum": 128,
    "txt2img/Mask erosion (-) / dilation (+) 2nd/step": 4,
    "txt2img/Mask merge mode 2nd/visible": true,
    "txt2img/Mask merge mode 2nd/value": "None",
    "txt2img/Inpaint mask blur 2nd/visible": true,
    "txt2img/Inpaint mask blur 2nd/value": 4,
    "txt2img/Inpaint mask blur 2nd/minimum": 0,
    "txt2img/Inpaint mask blur 2nd/maximum": 64,
    "txt2img/Inpaint mask blur 2nd/step": 1,
    "txt2img/Inpaint denoising strength 2nd/visible": true,
    "txt2img/Inpaint denoising strength 2nd/value": 0.4,
    "txt2img/Inpaint denoising strength 2nd/minimum": 0.0,
    "txt2img/Inpaint denoising strength 2nd/maximum": 1.0,
    "txt2img/Inpaint denoising strength 2nd/step": 0.01,
    "txt2img/Inpaint only masked 2nd/visible": true,
    "txt2img/Inpaint only masked 2nd/value": true,
    "txt2img/Inpaint only masked padding, pixels 2nd/visible": true,
    "txt2img/Inpaint only masked padding, pixels 2nd/value": 32,
    "txt2img/Inpaint only masked padding, pixels 2nd/minimum": 0,
    "txt2img/Inpaint only masked padding, pixels 2nd/maximum": 256,
    "txt2img/Inpaint only masked padding, pixels 2nd/step": 4,
    "txt2img/Use separate width/height 2nd/visible": true,
    "txt2img/Use separate width/height 2nd/value": false,
    "txt2img/inpaint width 2nd/visible": true,
    "txt2img/inpaint width 2nd/value": 512,
    "txt2img/inpaint width 2nd/minimum": 64,
    "txt2img/inpaint width 2nd/maximum": 2048,
    "txt2img/inpaint width 2nd/step": 4,
    "txt2img/inpaint height 2nd/visible": true,
    "txt2img/inpaint height 2nd/value": 512,
    "txt2img/inpaint height 2nd/minimum": 64,
    "txt2img/inpaint height 2nd/maximum": 2048,
    "txt2img/inpaint height 2nd/step": 4,
    "txt2img/Use separate steps 2nd/visible": true,
    "txt2img/Use separate steps 2nd/value": false,
    "txt2img/ADetailer steps 2nd/visible": true,
    "txt2img/ADetailer steps 2nd/value": 28,
    "txt2img/ADetailer steps 2nd/minimum": 1,
    "txt2img/ADetailer steps 2nd/maximum": 150,
    "txt2img/ADetailer steps 2nd/step": 1,
    "txt2img/Use separate CFG scale 2nd/visible": true,
    "txt2img/Use separate CFG scale 2nd/value": false,
    "txt2img/ADetailer CFG scale 2nd/visible": true,
    "txt2img/ADetailer CFG scale 2nd/value": 7.0,
    "txt2img/ADetailer CFG scale 2nd/minimum": 0.0,
    "txt2img/ADetailer CFG scale 2nd/maximum": 30.0,
    "txt2img/ADetailer CFG scale 2nd/step": 0.5,
    "txt2img/Use separate checkpoint 2nd/visible": true,
    "txt2img/Use separate checkpoint 2nd/value": false,
    "txt2img/ADetailer checkpoint 2nd/visible": true,
    "txt2img/ADetailer checkpoint 2nd/value": "Use same checkpoint",
    "txt2img/Use separate VAE 2nd/visible": true,
    "txt2img/Use separate VAE 2nd/value": false,
    "txt2img/ADetailer VAE 2nd/visible": true,
    "txt2img/ADetailer VAE 2nd/value": "Use same VAE",
    "txt2img/Use separate sampler 2nd/visible": true,
    "txt2img/Use separate sampler 2nd/value": false,
    "txt2img/ADetailer sampler 2nd/visible": true,
    "txt2img/ADetailer sampler 2nd/value": "DPM++ 2M Karras",
    "txt2img/Use separate noise multiplier 2nd/visible": true,
    "txt2img/Use separate noise multiplier 2nd/value": false,
    "txt2img/Noise multiplier for img2img 2nd/visible": true,
    "txt2img/Noise multiplier for img2img 2nd/value": 1.0,
    "txt2img/Noise multiplier for img2img 2nd/minimum": 0.5,
    "txt2img/Noise multiplier for img2img 2nd/maximum": 1.5,
    "txt2img/Noise multiplier for img2img 2nd/step": 0.01,
    "txt2img/Use separate CLIP skip 2nd/visible": true,
    "txt2img/Use separate CLIP skip 2nd/value": false,
    "txt2img/ADetailer CLIP skip 2nd/visible": true,
    "txt2img/ADetailer CLIP skip 2nd/value": 1,
    "txt2img/ADetailer CLIP skip 2nd/minimum": 1,
    "txt2img/ADetailer CLIP skip 2nd/maximum": 12,
    "txt2img/ADetailer CLIP skip 2nd/step": 1,
    "txt2img/Restore faces after ADetailer 2nd/visible": true,
    "txt2img/Restore faces after ADetailer 2nd/value": false,
    "txt2img/ControlNet model 2nd/visible": true,
    "txt2img/ControlNet model 2nd/value": "None",
    "txt2img/ControlNet module 2nd/value": "None",
    "txt2img/ControlNet weight 2nd/visible": true,
    "txt2img/ControlNet weight 2nd/value": 1.0,
    "txt2img/ControlNet weight 2nd/minimum": 0.0,
    "txt2img/ControlNet weight 2nd/maximum": 1.0,
    "txt2img/ControlNet weight 2nd/step": 0.01,
    "txt2img/ControlNet guidance start 2nd/visible": true,
    "txt2img/ControlNet guidance start 2nd/value": 0.0,
    "txt2img/ControlNet guidance start 2nd/minimum": 0.0,
    "txt2img/ControlNet guidance start 2nd/maximum": 1.0,
    "txt2img/ControlNet guidance start 2nd/step": 0.01,
    "txt2img/ControlNet guidance end 2nd/visible": true,
    "txt2img/ControlNet guidance end 2nd/value": 1.0,
    "txt2img/ControlNet guidance end 2nd/minimum": 0.0,
    "txt2img/ControlNet guidance end 2nd/maximum": 1.0,
    "txt2img/ControlNet guidance end 2nd/step": 0.01
'''

def download_all_control_models_new():
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_style_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_sketch_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_seg_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_openpose_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_keypose_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_depth_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_color_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_canny_sd14v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_canny_sd15v2.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_depth_sd15v2.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_sketch_sd15v2.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models
    wget --content-disposition https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_zoedepth_sd15v1.pth -P {WEBUI_PATH}/extensions/sd-webui-controlnet/models

def move_files_recursively(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"The source folder {source_folder} does not exist.")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for item in os.listdir(source_folder):
        if item.startswith('.'):
            continue
        source_item_path = os.path.join(source_folder, item)
        destination_item_path = os.path.join(destination_folder, item)
        if os.path.isdir(source_item_path):
            move_files_recursively(source_item_path, destination_item_path)
        else:
            if os.path.exists(destination_item_path):
                os.remove(destination_item_path)
            shutil.move(source_item_path, destination_item_path)


#
# 2/8 : INSTALL
#

if not skip_install_system:
    if not return__isValidFile('/content/installed'):
        cd /content
        clear_output()
        print(f'Installing libraries and software...')
        env TF_CPP_MIN_LOG_LEVEL=1
        apt -y update -qq
        wget https://github.com/camenduru/gperftools/releases/download/v1.0/libtcmalloc_minimal.so.4 -O /content/libtcmalloc_minimal.so.4
        env LD_PRELOAD=/content/libtcmalloc_minimal.so.4
        apt -y install -qq aria2 libcairo2-dev pkg-config python3-dev
        pip install -q torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 torchtext==0.15.2 torchdata==0.6.1 --extra-index-url https://download.pytorch.org/whl/cu118 -U
        pip install -q xformers==0.0.20 triton==2.0.0 gradio_client==0.2.7 -U

        #pip install -q gradio==3.50.2 gradio_client==0.6.1 -U

        pip install httpx==0.24.1
        pip install --upgrade huggingface_hub
        create_empty_file('/content/installed')
        clear_output()
        print(f'Done!')
    else:
        env TF_CPP_MIN_LOG_LEVEL=1
        env LD_PRELOAD=/content/libtcmalloc_minimal.so.4
        clear_output()
        print(f'Installing libraries and software...')
        print(f'Already done!')


#
# 4/8 : Cloning repositories
#
if not skip_install:
    cd $WEBUI_ROOT
    clear_output()
    print(f'Installing WebUI and Extensions...')
    git clone -b {webui_version} https://github.com/camenduru/stable-diffusion-webui {WEBUI_PATH}

    git {CLONE_ARG} https://huggingface.co/embed/negative {WEBUI_PATH}/embeddings/negative
    git {CLONE_ARG} https://huggingface.co/embed/lora {WEBUI_PATH}/models/Lora/positive
    wget --content-disposition https://huggingface.co/embed/upscale/resolve/main/4x-UltraSharp.pth -d {WEBUI_PATH}/models/ESRGAN -o 4x-UltraSharp.pth
    wget https://raw.githubusercontent.com/camenduru/stable-diffusion-webui-scripts/main/run_n_times.py -O {WEBUI_PATH}/scripts/run_n_times.py

    rm -Rf {WEBUI_PATH}/embeddings/.git
    rm -Rf {WEBUI_PATH}/models/Lora/positive/.git

    if webui_version == 'v2.4':
        git clone -b v2.4 https://github.com/camenduru/sd-webui-tunnels {WEBUI_PATH}/extensions/sd-webui-tunnels
        git {CLONE_ARG} https://github.com/camenduru/a1111-sd-webui-locon {WEBUI_PATH}/extensions/a1111-sd-webui-locon
        git clone -b v2.4 https://github.com/camenduru/batchlinks-webui {WEBUI_PATH}/extensions/batchlinks-webui
        git clone -b v2.4 https://github.com/camenduru/stable-diffusion-webui-rembg {WEBUI_PATH}/extensions/stable-diffusion-webui-rembg
    else:
        git {CLONE_ARG} https://github.com/camenduru/sd-webui-tunnels {WEBUI_PATH}/extensions/sd-webui-tunnels
        git {CLONE_ARG} https://github.com/camenduru/a1111-sd-webui-locon {WEBUI_PATH}/extensions/a1111-sd-webui-locon
        git {CLONE_ARG} https://github.com/etherealxx/batchlinks-webui {WEBUI_PATH}/extensions/batchlinks-webui

    #error git {CLONE_ARG} https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg {WEBUI_PATH}/extensions/stable-diffusion-webui-rembg
    #git {CLONE_ARG} https://github.com/tjm35/asymmetric-tiling-sd-webui {WEBUI_PATH}/extensions/asymmetric-tiling-sd-webui
    #git {CLONE_ARG} https://github.com/hnmr293/posex {WEBUI_PATH}/extensions/posex
    # Fix for WebUI
    #git {CLONE_ARG} https://github.com/zif002/posex {WEBUI_PATH}/extensions/posex

    if ext_bulk_controllnet:
        pip install fvcore mediapipe onnxruntime svglib handrefinerportable depth_anything
        pip install insightface
        git {CLONE_ARG} https://github.com/Mikubill/sd-webui-controlnet {WEBUI_PATH}/extensions/sd-webui-controlnet
        #From ControlNet extension v1.1.411, users no longer need to install this extension locally, as ControlNet extension now uses the remote endpoint at https://huchenlei.github.io/sd-webui-openpose-editor/
        #git {CLONE_ARG} https://github.com/huchenlei/sd-webui-openpose-editor {WEBUI_PATH}/extensions/sd-webui-openpose-editor
        git {CLONE_ARG} https://github.com/fkunn1326/openpose-editor {WEBUI_PATH}/extensions/openpose-editor
        git {CLONE_ARG} https://github.com/nonnonstop/sd-webui-3d-open-pose-editor {WEBUI_PATH}/extensions/sd-webui-3d-open-pose-editor
        git {CLONE_ARG} https://github.com/jexom/sd-webui-depth-lib {WEBUI_PATH}/extensions/sd-webui-depth-lib

    if ext_inf_img_browsing:
        git {CLONE_ARG} https://github.com/zanllp/sd-webui-infinite-image-browsing {WEBUI_PATH}/extensions/sd-webui-infinite-image-browsing
    elif ext_bulk_two:
        git {CLONE_ARG} https://github.com/camenduru/stable-diffusion-webui-images-browser {WEBUI_PATH}/extensions/stable-diffusion-webui-images-browser

    if ext_bulk_one:
        git {CLONE_ARG} https://github.com/s0md3v/sd-webui-roop  {WEBUI_PATH}/extensions/sd-webui-roop
        git {CLONE_ARG} https://github.com/Bing-su/adetailer {WEBUI_PATH}/extensions/adetailer
        write_ui_config(json_adetailer)
        git {CLONE_ARG} https://github.com/adieyal/sd-dynamic-prompts.git  {WEBUI_PATH}/extensions/sd-dynamic-prompts

    if ext_bulk_two:
        git {CLONE_ARG} https://github.com/deforum-art/deforum-for-automatic1111-webui {WEBUI_PATH}/extensions/deforum-for-automatic1111-webui
        git {CLONE_ARG} https://github.com/camenduru/stable-diffusion-webui-huggingface {WEBUI_PATH}/extensions/stable-diffusion-webui-huggingface
        git {CLONE_ARG} https://github.com/camenduru/sd-civitai-browser {WEBUI_PATH}/extensions/sd-civitai-browser

    if ext_bulk_three:
        git {CLONE_ARG} https://github.com/ashen-sensored/stable-diffusion-webui-two-shot {WEBUI_PATH}/extensions/stable-diffusion-webui-two-shot
        git {CLONE_ARG} https://github.com/thomasasfk/sd-webui-aspect-ratio-helper {WEBUI_PATH}/extensions/sd-webui-aspect-ratio-helper
        git {CLONE_ARG} https://github.com/pharmapsychotic/clip-interrogator-ext.git {WEBUI_PATH}/extensions/clip-interrogator-ext
        git {CLONE_ARG} https://github.com/kohya-ss/sd-webui-additional-networks {WEBUI_PATH}/extensions/sd-webui-additional-networks
        #git clone -b v2.4 https://github.com/camenduru/sd-webui-additional-networks {WEBUI_PATH}/extensions/sd-webui-additional-networks

    #git {CLONE_ARG} https://github.com/camenduru/stable-diffusion-webui-catppuccin {WEBUI_PATH}/extensions/stable-diffusion-webui-catppuccin
    #git {CLONE_ARG} https://github.com/AlUlkesh/stable-diffusion-webui-images-browser {WEBUI_PATH}/extensions/stable-diffusion-webui-images-browser
    #git {CLONE_ARG} https://github.com/yownas/shift-attention {WEBUI_PATH}/extensions/shift-attention

    # gradio-3.41.2 & sd-webui 1.6
    #git {CLONE_ARG} https://github.com/canisminor1990/sd-webui-lobe-theme {WEBUI_PATH}/extensions/sd-webui-lobe-theme

    if ext_cozy_nest:
        git {CLONE_ARG} https://github.com/mix1009/model-keyword  {WEBUI_PATH}/extensions/model-keyword
        git {CLONE_ARG} https://github.com/DominikDoom/a1111-sd-webui-tagcomplete  {WEBUI_PATH}/extensions/a1111-sd-webui-tagcomplete
        git {CLONE_ARG} https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper  {WEBUI_PATH}/extensions/Stable-Diffusion-Webui-Civitai-Helper
        git {CLONE_ARG} https://github.com/Nevysha/Cozy-Nest  {WEBUI_PATH}/extensions/Cozy-Nest

    print('Downloading Lora and Textual Inversion files')
    git {CLONE_ARG} https://huggingface.co/steinhaug/kista-webui /content/webui
    move_files_recursively('/content/webui', f"{WEBUI_PATH}")
    rm -Rf /content/webui

    cd {WEBUI_PATH}

    git reset --hard
    git -C {WEBUI_PATH}/repositories/stable-diffusion-stability-ai reset --hard

    #sed -i -e '''/    prepare_environment()/a\    os.system\(f\"""sed -i -e ''\"s/dict()))/dict())).cuda()/g\"'' {WEBUI_PATH}/repositories/stable-diffusion-stability-ai/ldm/util.py""")''' {WEBUI_PATH}/launch.py
    #sed -i -e 's/\"sd_model_checkpoint\"\,/\"sd_model_checkpoint\,sd_vae\,CLIP_stop_at_last_layers\"\,/g' {WEBUI_PATH}/modules/shared.py

    sed -i -e '''/from modules import launch_utils/a\import os''' {WEBUI_PATH}/launch.py
    sed -i -e '''/        prepare_environment()/a\        os.system\(f\"""sed -i -e ''\"s/dict()))/dict())).cuda()/g\"'' {WEBUI_PATH}/repositories/stable-diffusion-stability-ai/ldm/util.py""")''' {WEBUI_PATH}/launch.py
    sed -i -e 's/\["sd_model_checkpoint"\]/\["sd_model_checkpoint","sd_vae","CLIP_stop_at_last_layers"\]/g' {WEBUI_PATH}/modules/shared.py

    clear_output();
    print('Completed installing WebUI and Extensions...')

#
# 5/8 : ControlNet
#
if not skip_install:
    print('ControlNet, checking...')
    if ext_bulk_controllnet and do_dir_contain_controlnet_models(dir__controlnet):
        print('ControlNet cached with Google Drive')
    elif ext_bulk_controllnet:
        print('ControlNet will now download all models...')
        download_all_control_models_new()
        clear_output()
        if task__cache_controlnet:
            if not return__isValidDir(dir__controlnet):
                print(f'Creating new drive folder: ./{os.path.basename(DEFAULT_CONTROLNET_FOLDER)}')
                os.makedirs(DEFAULT_CONTROLNET_FOLDER, exist_ok=True)
                dir__controlnet = DEFAULT_CONTROLNET_FOLDER
            print('Copying all models into gDrive cache folder...')
            copy_files__directory(f'{WEBUI_PATH}/extensions/sd-webui-controlnet/models', dir__controlnet)
            task__cache_controlnet = False
            update_KISTA_config()
            clear_output()
            print('ControlNet cache in gDfrive completed, settings updated...')
    else:
        clear_output()
        print('Continuing...')

    if sources__copy_lauras != "":
        print('Copying LORA files into model folder...')
        copy_sources(f'{WEBUI_PATH}/models/Lora', sources__copy_lauras)
        clear_output()
        print('Done.')

    if sources__copy_textual_inversion != "":
        print('Copying TEXTUAL_INVERSION files into model folder...')
        copy_sources(f'{WEBUI_PATH}/embeddings', sources__copy_textual_inversion)
        clear_output()
        print('Done.')

#if not skip_install:
#    hashes_json_bck = f'{KISTA_DRIVE_PATHS}/config_KISTA_WebUI_hashes.json'
#    hashes_json_org = f'{WEBUI_PATH}/extensions/sd-webui-additional-networks/hashes.json'
#    if return__isValidFile(hashes_json_bck):
#        print('Additional networks hashes backup detected...')
#        if return__isValidFile(hashes_json_org):
#            print('... removing default settings.')
#            os.remove(hashes_json_org)
#        print('Copying backup settings with hashes...')
#        move_single_file(hashes_json_bck, hashes_json_org,True)
#        print('Done!')

#
# 6/8 : Checkpoint
#
if do_we_need_to_download_checkpoint():
    print('Downloading uberRealisticPornMerge_urpmv13')
    wget --content-disposition https://huggingface.co/ckpt/urpm/resolve/main/uberRealisticPornMerge_urpmv13.safetensors -d {WEBUI_PATH}/models/Stable-diffusion -o uberRealisticPornMerge_urpmv13.safetensors
    if task__cache_checkpoints:
        if not return__isValidDir(dir__models):
            dir__models = DEFAULT_CHECKPOINTS_FOLDER
            os.makedirs(dir__models, exist_ok=True)

        clear_output()
        print(f'Copying checkpoint to Google Drive folder...')
        path_cpkt = dir__models + '/uberRealisticPornMerge_urpmv13.safetensors'
        shutil.copy2(f'{WEBUI_PATH}/models/Stable-diffusion/uberRealisticPornMerge_urpmv13.safetensors', dir__models)
        task__cache_checkpoints = False
        update_KISTA_config()
        print(f'Copy complete, KISTA settings updated...')

#
# 7/8 : Post installer checks
#
cd $WEBUI_PATH
clear_output()
EnvFileData = '''
IIB_SECRET_KEY=
IIB_SERVER_LANG=en
IIB_ACCESS_CONTROL=disable
'''

print('*** Post installer checks:')
if not skip_install:
    print('Patching extension: roop')
    print(' -- disabling naked checker')
    commentOutLinesStartingWith(f'{WEBUI_PATH}/extensions/sd-webui-roop/scripts/cimage.py', ['chunks =','for chunk','shapes.append'],'    # ')

if not skip_install and ext_inf_img_browsing:
    print('Patching extension: infinite-image-browsing...')
    print(' -- setting up .env file')
    createFile__ifNotExist(f'{WEBUI_PATH}/extensions/sd-webui-infinite-image-browsing', '.env', EnvFileData)
    print(' -- correcting .db path')
    openReplaceStringMatch(f'{WEBUI_PATH}/extensions/sd-webui-infinite-image-browsing/scripts/iib/db/datamodel.py','"iib.db"','"/content/drive/MyDrive/docs/config_KISTA_WebUI.db"')


#
# build settings always
#
inip = Path(f'{WEBUI_PATH}/config.json')
if not skip_install:
    if not inip.is_file():
        print('Preparing WebUI config.json with KISTA settings')
        import json
        conf_ini_json = {
            "outdir_samples": dir__outdir_samples,
            "outdir_grids": dir__outdir_grids,
            "control_net_models_path": dir__controlnet,
            "quicksettings": "sd_model_checkpoint,sd_vae,CLIP_stop_at_last_layers,initial_noise_multiplier,img2img_color_correction",
            "save_txt": True,
            "do_not_add_watermark": True,
            "control_net_no_detectmap": True,
            "hide_samplers": [
                "LMS",
                "Heun",
                "DPM2",
                "DPM2 a",
                "DPM fast",
                "DPM adaptive",
                "LMS Karras",
                "PLMS",
                "DPM++ 2S a Karras",
                "DPM2 a Karras",
                "DPM2 Karras"
            ],
            "additional_networks_hash_thread_count": 4.0,
            "additional_networks_back_up_model_when_saving": False,
            "unload_models_when_training": True,
            "training_xattention_optimizations": True,
            "additional_networks_extra_lora_path": dir__extra_loras_search
        }
        with open("config.json", "w") as jsonfile:
            json.dump(conf_ini_json, jsonfile)
    else:
        print('WebUI config.json already exists, all done.')



# Now we can run the app builder
if ext_inf_img_browsing:
    print('akko dikko, bypass app run')
elif 1 == 2:
    from google.colab.output import serve_kernel_port_as_iframe, serve_kernel_port_as_window
    from google.colab import output; import sys; import os
    output.clear()
    print('Installing dependencies for infinite image galleries')
    cd $WEBUI_PATH/extensions/sd-webui-infinite-image-browsing
    pip install -r requirements.txt
    sys.path.append( os.getcwd() )
    output.clear()

    import app;

    if not return__isValidDir("/content/image-galleries"):
        os.makedirs("/content/image-galleries", exist_ok=True)
    port = 9998
    extra_paths = [ "/content/image-galleries" ]
    sd_webui_config = f"{WEBUI_PATH}/config.json"
    update_image_index = True
    serve_kernel_port_as_iframe(port)
    await app.async_launch_app(
        port = port,
        extra_paths = extra_paths,
        update_image_index = update_image_index,
        sd_webui_config = sd_webui_config,
    )

    print('Done... continuing...')
    cd $WEBUI_PATH



#if not return__isValidFile(f"{WEBUI_PATH}/models/ESRGAN/8x_NMKD-Superscale_150000_G.pth"):
#    wget --content-disposition https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/8x_NMKD-Superscale_150000_G.pth?download=true -P {WEBUI_PATH}/models/ESRGAN

#if not return__isValidFile(f"{WEBUI_PATH}/models/ESRGAN/4x_NMKD-Superscale-SP_178000_G.pth"):
#    cd {WEBUI_PATH}/models/ESRGAN
#    wget --content-disposition https://drive.usercontent.google.com/u/0/uc?id=1p5FzzD3FmHS10KDg7EkNRYB390blDUVO&export=download -P {WEBUI_PATH}/models/ESRGAN
#    cd {WEBUI_PATH}

import os
import shutil
def copy_file_if_not_exists(filepath, directorypath):
    filename = os.path.basename(filepath)
    full_path_in_directory = os.path.join(directorypath, filename)
    if not os.path.exists(full_path_in_directory):
        shutil.copy(filepath, directorypath)
        return f"{directorypath}/{filename}"
    else:
        return f"{directorypath}/{filename}"

cpkt_path = path_cpkt
# copy model to model folder
cpkt_path = copy_file_if_not_exists(path_cpkt,f"{WEBUI_PATH}/models/Stable-diffusion/")

#
# 8/8: Run WebUI
#
cd $WEBUI_PATH
clear_output()

# python launch.py --listen --xformers --enable-insecure-extension-access --theme dark --gradio-queue --multiple

args = "--share --xformers --enable-insecure-extension-access"
if skip_install:
    args = args + " --skip-install"
#if run_from_drive:
#    args = args + " --skip-torch-cuda-test"
if len(cpkt_path) and os.path.isfile(cpkt_path):
    ckpt_file = cpkt_path
else:
    ckpt_file = ''
if dir__models != "":
    args = args + " --ckpt-dir=\"" + dir__models + "\""
    if ckpt_file == '':
        ckpt_file = checkpoint_file = find_checkpoint_file(dir__models)
if ckpt_file != "":
    args = args + " --ckpt=\"" + ckpt_file + "\""
else:
    print('NOTICE! Default --ckpt invalid, skipped parameter.')

#print('Launching WebUI...')
#python launch.py $args

print("Launch command:")
print(f"!python launch.py {args}")
