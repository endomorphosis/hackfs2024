from transformers import AutoModel
from ipfs_transformers import AutoModel
#from accelerate import load_checkpoint_and_dispatch
from ipfs_accelerate import load_checkpoint_and_dispatch

model = load_checkpoint_and_dispatch(
    model, checkpoint=checkpoint_file, device_map="auto"
)


model = AutoModel.from_auto_download("bge-small-en-v1.5")  

