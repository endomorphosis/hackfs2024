**HACKFS Hackathon**

Progress:

  IPFS Agents
    The purpose of this module is to take the information from the IPFS Model Manager, and the peers that also run the model manager which are broadcasting what models they use, then use that list to return a list of what tools can be used in the Huggingface Agents library, to make requests to other Agents or download the missing models and complete the execution plan.  

  IPFS Accelerate
    The purpose of this module is to overload the the load_checkpoint_and_dispatch() method of the huggingface accelerate library, such that it starts a docker container on a crypto machine learning service, and will automatically trust whatever identities have been specified for it to trust, when it launches the IPFS Model Manager and IPFS Agents library.

**Developer Logs**

Because alot of work had to go into fixing / refactoring previous work, I am including the other repsitories that I had modified.

Other Repositories Touched:

https://github.com/endomorphosis/ipfs_model_manager

https://github.com/endomorphosis/ipfs_model_manager_js

https://github.com/endomorphosis/orbitdb_kit

https://github.com/endomorphosis/ipfs_kit

New Repositories Created:

https://github.com/endomorphosis/ipfs_accelerate

https://github.com/endomorphosis/ipfs_agents

**Blocking issues**

python pylibp2p has limited functionality
