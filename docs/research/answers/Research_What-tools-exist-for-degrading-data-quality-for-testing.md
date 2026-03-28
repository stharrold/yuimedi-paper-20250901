# Libraries and Tools for Making Clean Datasets Messy

## Overview
This document summarizes libraries and tools available for making clean datasets messy, useful for benchmarking robust algorithmic data modeling and testing ML model resilience.

---

## Key Libraries and Tools

### 1. Adversarial Robustness Toolbox (ART)
- **Paper:** Adversarial Robustness Toolbox v1.0.0
- **Authors:** MI Nicolae, M Sinn, MN Tran, B Buesser et al.
- **Source:** arXiv preprint, 2018
- **Citations:** 842
- **Description:** Python library for creating and testing defenses against adversarial threats in ML models, which inherently involves generating adversarial examples or "messy data"
- **Key Features:**
  - Generates adversarial attacks against various ML models (DNNs, GBDTs, SVMs)
    - Enables generation of deliberately modified inputs (images, texts, tabular data)
      - Implements techniques like Fast Gradient Sign Method (FGSM) and Universal Adversarial Perturbations
        - Methods to "make a clean dataset messy" through controlled perturbations

        ### 2. Foolbox
        - **Paper:** Foolbox: A python toolbox to benchmark the robustness of machine learning models
        - **Authors:** J Rauber, W Brendel, M Bethge
        - **Source:** arXiv preprint arXiv:1707.04131, 2017
        - **Citations:** 640
        - **Description:** Python package designed to generate adversarial perturbations, effectively making clean inputs "messy" for ML models
        - **Key Features:**
          - Quantifies and compares model robustness against adversarial examples
            - Implements various adversarial attack methods
              - Finds minimum perturbation needed to craft adversarial examples
                - Reference implementations of most published adversarial attack methods

                ### 3. Generating High-Fidelity Synthetic Patient Data
                - **Paper:** Generating high-fidelity synthetic patient data for assessing machine learning healthcare software
                - **Authors:** A Tucker, Z Wang, Y Rotalinti, P Myles
                - **Source:** NPJ digital medicine, 2020
                - **Citations:** 261
                - **Description:** Method for generating realistic synthetic datasets that capture complexities of original data (distributions, non-linear relationships, noise)
                - **Key Features:**
                  - Synthetic Data Methodology: Integrates resampling, probabilistic graphical modeling, latent variable identification
                    - Handles missingness and complex interactions in data
                      - Uses GANs for generating synthetic data with fewer biases

                      ### 4. CleanML Benchmark
                      - **Paper:** CleanML: A benchmark for joint data cleaning and machine learning
                      - **Authors:** P Li, X Rao, J Blase, Y Zhang, X Chu
                      - **Source:** arXiv preprint, 2019
                      - **Citations:** 71
                      - **URL:** https://chu-data-lab.github.io/CleanML/
                      - **Description:** Benchmark that systematically investigates the impact of data cleaning on downstream ML models
                      - **Key Features:**
                        - Five common error types for introducing noise
                          - Seven different ML models for testing robustness
                            - Publicly available and extensible benchmark
                              - Resource for creating messy datasets for benchmarking

                              ### 5. Benchmarking Unsupervised Outlier Detection
                              - **Paper:** Benchmarking unsupervised outlier detection with realistic synthetic data
                              - **Authors:** G Steinbuss, K Böhm
                              - **Source:** ACM Transactions on Knowledge Discovery, 2021
                              - **Citations:** 82
                              - **Description:** Generic process for generating datasets for benchmarking unsupervised outlier detection
                              - **Key Features:**
                                - Generates specific outliers (local outliers) for comparative evaluation
                                  - Outlier Characterization Approach for generating synthetic data
                                    - Useful for benchmarking robust algorithmic data modeling

                                    ### 6. DeepRobust
                                    - **Paper:** Deeprobust: A platform for adversarial attacks and defenses
                                    - **Authors:** Y Li, W Jin, H Xu, J Tang
                                    - **Source:** Proceedings of AAAI conference, 2021
                                    - **Citations:** 60
                                    - **Description:** PyTorch platform for generating adversarial examples by adding perturbations to clean datasets
                                    - **Key Features:**
                                      - Adversarial Examples APIs for image and graph data domains
                                        - Robustness Evaluation Tool for testing against adversarial examples
                                          - Supports benchmarking of robust algorithmic data modeling

                                          ### 7. Performance and Scalability of Data Cleaning Tools
                                          - **Paper:** Performance and Scalability of Data Cleaning and Preprocessing Tools: A Benchmark on Large Real-World Datasets
                                          - **Authors:** P Martins, F Cardoso, P Váz, J Silva, M Abbasi
                                          - **Source:** Data, 2025
                                          - **Citations:** 10
                                          - **Description:** Benchmarking study simulating genuine messy data challenges
                                          - **Key Features:**
                                            - Error injection rates: 2-5% duplicates, 2-3% placeholder-based missing values
                                              - Methodology for curating datasets from healthcare, finance, and industrial telemetry
                                                - Datasets up to 100 million records for simulating messy data challenges
                                                  - Evaluates robustness of downstream ML models

                                                  ### 8. FenceBox
                                                  - **Paper:** Fencebox: A platform for defeating adversarial examples with data augmentation techniques
                                                  - **Authors:** H Qiu, Y Zeng, T Zhang, Y Jiang, M Qiu
                                                  - **Source:** arXiv preprint arXiv:2012.01701, 2020
                                                  - **Citations:** 22
                                                  - **Description:** Comprehensive framework leveraging 15 different data augmentation techniques
                                                  - **Key Features:**
                                                    - Preprocesses input samples and removes adversarial perturbations
                                                      - Makes data "messy" for benchmarking robust algorithmic data modeling
                                                        - Deployable APIs for enhanced robustness against adversarial attacks
                                                          - Evaluates effectiveness of preprocessing solutions

                                                          ### 9. PuckTrick
                                                          - **Paper:** PuckTrick: A Library for Making Synthetic Data More Realistic
                                                          - **Authors:** A Agostini, A Maurino, B Spahiu
                                                          - **Source:** arXiv preprint arXiv:2506.18499, 2025
                                                          - **Citations:** 1
                                                          - **Description:** Python library designed to systematically contaminate synthetic datasets by introducing controlled errors
                                                          - **Key Features:**
                                                            - Supported Error Types: missing data, noisy values, outliers, label misclassification, duplication, class imbalance
                                                              - Benchmarking and Robustness Tool for evaluating ML model resilience
                                                                - Precise control over type and level of errors introduced
                                                                  - Powerful tool for evaluating data-cleaning algorithms

                                                                  ---

                                                                  ## Error Types for Making Data Messy

                                                                  | Error Type | Description | Tools Supporting |
                                                                  |------------|-------------|------------------|
                                                                  | Missing Values | Placeholder-based or random missing data | CleanML, PuckTrick, Performance Benchmark |
                                                                  | Duplicates | Exact or near-duplicate records | CleanML, Performance Benchmark |
                                                                  | Noisy Values | Random perturbations to feature values | PuckTrick, ART, Foolbox |
                                                                  | Outliers | Anomalous data points | Outlier Detection Benchmark, PuckTrick |
                                                                  | Label Noise | Misclassified labels | PuckTrick, CleanML |
                                                                  | Adversarial Perturbations | Carefully crafted modifications | ART, Foolbox, DeepRobust, FenceBox |
                                                                  | Class Imbalance | Skewed class distributions | PuckTrick |

                                                                  ---

                                                                  ## Citation Statistics

                                                                  - **Most cited tool:** Adversarial Robustness Toolbox (842 citations)
                                                                  - **Second most cited:** Foolbox (640 citations)
                                                                  - **Most cited for synthetic data:** High-fidelity synthetic patient data (261 citations)
                                                                  - **Newest tools:** PuckTrick (2025), Performance Benchmark (2025)

                                                                  ---

                                                                  ## Use Cases

                                                                  1. **ML Model Robustness Testing:** ART, Foolbox, DeepRobust
                                                                  2. **Data Cleaning Algorithm Evaluation:** CleanML, PuckTrick, Performance Benchmark
                                                                  3. **Synthetic Data Generation:** High-fidelity synthetic patient data, PuckTrick
                                                                  4. **Outlier Detection Benchmarking:** Unsupervised Outlier Detection Benchmark
                                                                  5. **Adversarial Defense Testing:** FenceBox, ART, DeepRobust

                                                                  ---

                                                                  *Source: Google Scholar Labs search results*
                                                                  *Query: "what libraries exist to make a clean dataset messy for benchmarking robust algorithmic data modeling?"*
                                                                  *Retrieved: December 2025*
