For full documentation for Azure Machine Learning service, visit **https://aka.ms/aml-docs**.
# Distributed HPMLA in Azure Machine Learning service

## **Use your own notebook server**

Video walkthrough:

[`get started video`](https://youtu.be/VIsXeTuW3FU)

1. Setup a Jupyter Notebook server and [install the Azure Machine Learning SDK](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-create-workspace-with-python).
2. Clone [this repository](https://github.com/lliimsft/Distributed-HPMLA/).
3. Start your notebook server.
3. Open and run [Distributed-HPMLA-with-custom-docker](./Distributed-HPMLA-with-custom-docker.ipynb) notebook. There are four steps for the notebooks:
    - Download training dataset and upload to AML blob datastore
    - Crate AML compute target (Batch AI cluster)
    - Run data shredding task on the compute target (single instance)
    - Run distributed HPMLA training on the compute target (multiple instances)
