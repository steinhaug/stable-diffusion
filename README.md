# stable-diffusion

A collection of colabs that I maintain for myself while playing with Stable Diffusion and other AI models. Do register an Issue if you encounter problems with any of the notebooks here, everything is updating everywhere and all the time lately so things easily fall apart unless being maintained at a weekly basis.

## You want to train your model with high quality

Trust me, there are so much to learn and understand so unless you have the time for this I recommend trying Joe Penna's notebook and just accomodate whatever tips he has while running the notebook. Thinking hmmm I wonder what could improve the quality is a road that will take time with small rewards even no rewards :D 

<a href="https://colab.research.google.com/github/JoePenna/Dreambooth-Stable-Diffusion/blob/main/dreambooth_colab_joepenna.ipynb"><img src="https://img.shields.io/badge/-Joe_pennas_Dreambooth-001660?logo=google" alt="Joe Penna's Dreambooth"></a>

## Dreambooth_Colab_edition_for_people_in_a_hurry_fp16.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/Dreambooth_Colab_edition_for_people_in_a_hurry_fp16.ipynb" target="_blank"><img alt="Open in Colab" src="https://img.shields.io/badge/-COLAB_v1.5-000000?logo=github"></a>

Super easy demonstration of Stable Diffusion and Dreambooth. In under 60 minutes you will have trained your model and created 100+ AI images as I have automated the entire process, so unless the internet have broken again you should be ready for a treat. So if you are OK with not having to understand what an LLM, a transformer, machine learning, diffusion models, python or any of the technical fancy pancy details... then lets go! 

**prerequisites**

- A Google Drive account, comes with any Google accounts. You can register one for free if you do not already have one.
- A huggingface token, read token will do but write token if you want to save the trained model.
- 6 or 8 images of the subject you want to train.

Time from start to end: an hour of your time

Have fun!

Version v1.5: _Installation of libraries verified with Colab Pro._  
Version v1.4: _Installation of libraries verified with Colab Pro, does not work anymore with free Colab._  
Version v1.3: _Like a glove update. Added checks for crashed notebooks, notifying user of replaying cell containing all needed values. Added more error detection for situations things dont work out as planned... in colab world more often than not..._  
Version v1.2: _AutoAI maintained for gender, checkpoint file created earlier and model card for upload is detailed now._  
Version v1.1: _Added model selection._  
Version v1.0: _Initial notebook_  

## Kista WebUI Colab v1.5 <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/KISTA_WebUI_Colab.ipynb?v1.5" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Colab notebook based on a [![Open in Colab](https://img.shields.io/badge/Camenduru-❕-blue?logo=github)](https://github.com/camenduru) notebook, extended with editable settings and
auto cache modes for saving large files and loading then from your Drive.

**extension pipeline:**  
Cozy-Nest, ControlNet, roop, adetailer, infinite-image-browsing, clip-interrogator and loads more.

**version history:**  
v1.4: Corrected installer errors that suddenly appeared in colab.    
v1.3: _Additional-networks hashes cache added, added Lora search paths._  
v1.2: _Fixing variables_  
v1.1: _Adding default configuration with tasks that sets a new user up at first try_  
v1.0: _Initial release_  

## Kista AUTOMATIC1111 WebUI <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/KISTA_AUTOMATIC1111_WebUI.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

USE: Kista WebUI Colab  

Colab notebook for launching Stable Diffusion with the popular AUTOMATIC1111 WebUI, requires Google Drive and automatically saves your settings
for easy install and updateing of the notebook.

**Extensions:**
* [openpose-editor](https://github.com/fkunn1326/openpose-editor)
* [controlnet](https://github.com/Mikubill/sd-webui-controlnet)
* [images-browser](https://github.com/yfszzx/stable-diffusion-webui-images-browser)
* [huggingface](https://github.com/camenduru/stable-diffusion-webui-huggingface)
* [civitai-browser](https://github.com/camenduru/sd-civitai-browser)

## fast_stable_diffusion_AUTOMATIC1111+ <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/fast_stable_diffusion_AUTOMATIC1111%2B.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

The Last Ben notebook, enhanced for https://www.painthua.com/.

## steinhaug_trainer <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/steinhaug_trainer.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Colab notebook for training your model using Dreambooth.

**Features:**
* Converts diffusers to checkpoint
* Converts checkpoint to diffusers
* Stable Diffusion instance for generating images
* Batch image generator
* Huggingface uploader for your trained model

## Kista ControlNet_Video.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/ControlNet_Video.ipynb" target="_blank"><img alt="Open in Colab" src="https://img.shields.io/badge/steinhaug-Open%20in%20Colab-blue?logo=google-colab"></a>

ControlNet demos for all models, and ControlNet-Video for video processing.

ControlNet colab:<br>
[![Open in Colab](https://img.shields.io/badge/diffusers-Open%20in%20Colab-blue?logo=google-colab)](https://colab.research.google.com/github/huggingface/notebooks/blob/main/diffusers/controlnet.ipynb)
 
## Infinite Zoom v1.1 [![Open in Colab](https://img.shields.io/badge/steinhaug-Open%20in%20Colab-blue?logo=google-colab)](https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/smooth_infinite_zoom.ipynb)

Enhance or super zoom, in reality it's more like a full reverse. Needless to say, you can create some zoom effects with this colab.

## control_net_openpose_webui_colab.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/control_net_openpose_webui_colab.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Todo.

## stable_diffusion_demonstration.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/stable_diffusion_demonstration.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Todo.

## converter_colab.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/tool/converter_colab.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Convert your stable diffusion model to any format.

## wav2lip-colab.ipynb <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/tool/wav2lip-colab.ipynb" target="_blank"><img alt="Open in Colab" src="https://raw.githubusercontent.com/steinhaug/stable-diffusion/main/assets/badges/colab-badge.svg"></a>

Resync any video with a wav file. 

Source: <a href="https://colab.research.google.com/github/camenduru/wav2lip-colab/blob/main/wav2lip-colab.ipynb" target="_parent"><img src="https://img.shields.io/badge/camenduru-Open%20in%20Colab-blue?logo=google-colab" alt="Open In Colab"/></a> <a href="https://github.com/camenduru/wav2lip-colab/" target="_parent"><img src="https://img.shields.io/badge/camenduru-Open%20in%20Colab-blue?logo=github"></a>


## faceswap video <a href="https://colab.research.google.com/github/steinhaug/stable-diffusion/blob/main/faceswap/Video_Face_Swapper__For_people_in_a_hurry.ipynb?1" target="_blank"><img alt="Open Notebook in Colab" src="https://img.shields.io/badge/Video%20Face%20Swapper%20--%20for%20people%20in%20a%20hurry-Notebook-blue?logo=googlecolab"></a>

Takes a videofile and 1 image, using ROOP library and swaps the entiry video.

## Credits

All colabs above are derived work from theese repositories.

* [ShivamShrirao](https://github.com/ShivamShrirao/)
* [camenduru](https://github.com/camenduru/)
* [TheLastBen](https://github.com/TheLastBen)

## About me

- Kim Steinhaug
- steinhaug at gmail dot com
