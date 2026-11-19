# Proposed Additional References for Author Approval

**Note:** None of the entries below have been added to `E:\trueguard\ieee\overleaf\references.bib`. The original 40 entries remain completely untouched. Please review and approve these 11 essential primary references (covering our foundation model, four evaluated datasets, our directly reproduced Semantic Entropy baseline, and core statistical/selective-prediction methodology) before LaTeX/BibTeX conversion.

---

### 1. `kuhn2023semantic` (Directly Reproduced External Baseline)
- **Authors:** L. Kuhn, Y. Gal, and S. Farquhar
- **Title:** Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation
- **Venue:** *Proc. 11th Int. Conf. Learn. Represent. (ICLR)*, 2023.
- **Why Required:** Foundational paper defining Semantic Entropy, which we reproduce directly on TriviaQA (`Table VII`).

### 2. `farquhar2024detecting` (Directly Reproduced External Baseline)
- **Authors:** S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
- **Title:** Detecting hallucinations in large language models using semantic entropy
- **Venue:** *Nature*, vol. 630, pp. 625–630, Jun. 2024.
- **Why Required:** Defines the relaxed bidirectional entailment clustering rule and discrete Semantic Entropy variant (`SE_Disc`) used in our Colab reproduction.

### 3. `zhang2024tinyllama` (Foundation Model Used in All Experiments)
- **Authors:** P. Zhang, G. Zeng, T. Wang, and W. Lu
- **Title:** TinyLlama: An Open-Source Small Language Model
- **Venue:** *arXiv preprint arXiv:2401.02385*, 2024.
- **Why Required:** Primary citation for `TinyLlama/TinyLlama-1.1B-Chat-v1.0`, the frozen base LLM used across all 10 datasets.

### 4. `dziri2022faithdial` (Evaluated Benchmark #6)
- **Authors:** N. Dziri, E. Kamalloo, S. Milton, O. Zaiane, M. Yu, E. M. Ponti, and S. Reddy
- **Title:** FaithDial: A Faithful Benchmark for Information-Seeking Dialogue
- **Venue:** *Trans. Assoc. Comput. Linguist. (TACL)*, vol. 10, pp. 1473–1490, 2022.
- **Why Required:** Primary citation for the FaithDial unseen transfer and target-refitting benchmark.

### 5. `maynez2020faithfulness` (Evaluated Benchmark #8)
- **Authors:** J. Maynez, S. Narayan, B. Bohnet, and R. McDonald
- **Title:** On Faithfulness and Factuality in Abstractive Summarization
- **Venue:** *Proc. 58th Annu. Meeting Assoc. Comput. Linguist. (ACL)*, 2020, pp. 1906–1919.
- **Why Required:** Primary citation for the XSum-Factuality benchmark.

### 6. `thorne2018fever` (Evaluated Benchmark #9)
- **Authors:** J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal
- **Title:** FEVER: a Large-scale Dataset for Fact Extraction and VERification
- **Venue:** *Proc. Conf. North Amer. Chapter Assoc. Comput. Linguist.: Human Lang. Technol. (NAACL-HLT)*, 2018, pp. 809–819.
- **Why Required:** Primary citation for the FEVER claim-verification transfer benchmark.

### 7. `joshi2017triviaqa` (Evaluated Benchmark #10)
- **Authors:** M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer
- **Title:** TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension
- **Venue:** *Proc. 55th Annu. Meeting Assoc. Comput. Linguist. (ACL)*, 2017, pp. 1601–1611.
- **Why Required:** Primary citation for the TriviaQA closed-book selective prediction and external-baseline benchmark.

### 8. `geifman2017selective` (Selective Prediction / AURC Metric)
- **Authors:** Y. Geifman and R. El-Yaniv
- **Title:** Selective Classification for Deep Neural Networks
- **Venue:** *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 30, 2017.
- **Why Required:** Foundational reference for risk–coverage curves and selective abstention evaluation.

### 9. `nadeau2003inference` (Statistical Variance Flag for Repeated Seeds)
- **Authors:** C. Nadeau and Y. Bengio
- **Title:** Inference for the Generalization Error
- **Venue:** *Machine Learning*, vol. 52, no. 3, pp. 239–281, 2003.
- **Why Required:** Supports our explicit statistical flag in Section IV-L regarding repeated-seed variance over a fixed 40% test split.

### 10. `burns2023discovering` (Unsupervised White-Box Probing Context)
- **Authors:** C. Burns, H. Ye, D. Klein, and J. Steinhardt
- **Title:** Discovering Latent Knowledge in Language Models Without Supervision
- **Venue:** *Proc. 11th Int. Conf. Learn. Represent. (ICLR)*, 2023.
- **Why Required:** Foundational unsupervised white-box probing method (CCS) cited transparently in Limitations (Section VI-G).

### 11. `chen2024inside` (Unsupervised Activation-Covariance Context)
- **Authors:** C. Chen, K. Liu, Z. Chen, Y. Gu, Y. Wu, M. Tao, Z. Fu, and J. Ye
- **Title:** INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection
- **Venue:** *Proc. 12th Int. Conf. Learn. Represent. (ICLR)*, 2024.
- **Why Required:** Key internal-state EigenScore baseline cited transparently in Limitations (Section VI-G).
