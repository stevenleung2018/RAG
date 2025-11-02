# RAG

This is a simple RAG (Retrieval-Augmented Generation) system that uses a vector database to store and retrieve documents. It is designed to be easy to use and extend.

## Installation

To set up the rag environment, choose the appropriate YAML for your hardware:

For most users, use env_cpu.yml
For Macs with Apple Silicon, use env_mps.yml
For systems with NVIDIA GPUs, use env_cuda.yml
Create the environment with:

```{bash}
conda env create -f env_cpu.yml  # Or env_mps.yml / env_cuda.yml
```

Activate with:

```{bash}
conda activate rag
```

# Context documents

Here are some example documents that can be used with the RAG system.  Please download and save them in the `docs` directory.
- [Species at Risk Act (SARA)](https://laws-lois.justice.gc.ca/PDF/S-15.3.pdf)
- [You manage federal land](https://www.canada.ca/content/dam/eccc/migration/sara/6ac53f6b-550e-473d-9bdb-1ccbf661f521/fedland-eng.pdf)
- [You manage private land](https://www.canada.ca/content/dam/eccc/migration/sara/6ac53f6b-550e-473d-9bdb-1ccbf661f521/privland-eng.pdf)
- [You operate a business](https://www.canada.ca/content/dam/eccc/migration/sara/6ac53f6b-550e-473d-9bdb-1ccbf661f521/business-eng.pdf)
