import torch
from transformers import AutoConfig, AutoModelForCausalLM
from ipfs_transformers import AutoModel, AutoModelForCausalLM
#from accelerate import load_checkpoint_and_dispatch
from accelerate import init_empty_weights
from ipfs_accelerate import load_checkpoint_and_dispatch
#from ipfs_model_manager import model_manager
#from ipfs_kit import ipfs_kit
#from orbitdb_kit import orbitdb_kit 
#from ipfs_model_manager import ipfs_model_manager as model_manager 
#from ipfs_model_manager import load_config, load_collection
#from ipfs_model_manager import list_ipfs_models, list_s3_models, list_local_models, ModelManager

checkpoint = "bge-small-en-v1.5"
#weights_location = hf_hub_download(checkpoint, "pytorch_model.bin")
#weights_location = 
config = AutoConfig.from_pretrained(checkpoint)

with init_empty_weights():
    model = AutoModelForCausalLM.from_config(config)

model = load_checkpoint_and_dispatch(
    model, checkpoint=weights_location, device_map="auto"
)


#model = load_checkpoint_and_dispatch(
#    model, checkpoint=checkpoint_file, device_map="lilypad"
#)

#model = load_checkpoint_and_dispatch(
#    model, checkpoint=checkpoint_file, device_map="akash"
#)


