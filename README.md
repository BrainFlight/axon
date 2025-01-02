<a id="readme-top"></a>
<br />
<div align="center">

  <a href="https://github.com/ammar-s847/fydp-repo"><img width="140px" src="./docs/images/logo.png"></a>

  <h3 align="center">Axon - ML Platform</h3>

  <p align="center">
    ML platform for training, versioning, and experimenting with VLA models at scale
    <br />
    <a href="https://github.com/ammar-s847/fydp-repo"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<!-- <details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details> -->



<!-- ABOUT THE PROJECT -->
## About The Project

API Example

<div align="center">
<img width="60%" style="text-align: center" src="./docs/images/endpoint-example-1.png">
</div>
<!-- ![alt text](./docs/images/endpoint-example-1.png) -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With



<img width="50" height="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png"></img> <img style="padding: 0 0 0 5px" width="50" height="50" src="https://user-images.githubusercontent.com/25181517/182534006-037f08b5-8e7b-4e5f-96b6-5d2a5558fa85.png"></img> <img width="auto" height="50" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png"></img><img style="padding: 0 0 0 10px" width="50" height="50" src="https://user-images.githubusercontent.com/25181517/192107855-e669c777-9172-49c5-b7e0-404e29df0fee.png"></img> <img style="padding: 0 0 0 5px" width="auto" height="40" src="https://miro.medium.com/v2/resize:fit:640/1*dpXAaEpwsJcs2UbZEp5jJw.png"></img> <img style="padding: 0 0 0 5px" width="auto" height="50" src="https://cdn.icon-icons.com/icons2/2699/PNG/512/pytorch_logo_icon_169823.png"></img> <img style="padding: 0 0 0 5px" width="auto" height="50" src="https://logos-world.net/wp-content/uploads/2023/05/Cohere-Logo.png"></img>  <img width="auto" height="50" src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo-with-title.svg"></img>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started


### Prerequisites

Get API Keys for

`.env` file:
```sh
ANTHROPIC_API_KEY=""
OPENAI_API_KEY=""
HF_ACCESS_TOKEN=""
COHERE_API_KEY=""
WANDB_API_KEY="" # Weights and Biases
```

### Installation

1. Install dependencies
```sh
poetry install
```

### API and Swagger Docs

1. Run the API

```sh
cd platform
fastapi dev main.py
```

2. Visit http://localhost:8000/docs

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [] Build Inference Pods
- [] Setup K8S Infra

<p align="right">(<a href="#readme-top">back to top</a>)</p>
