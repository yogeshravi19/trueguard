# Table I — 10-Dataset Benchmark Suite, Splits, and Exclusions

| # | Dataset | Protocol Role | Raw Rows | Usable Rows | Groups | Label 0 | Label 1 | Prevalence | Excluded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | halueval_dialogue | IN_DOMAIN_CV_AND_POOL | 10000 | 4000 | 2000 | 2000 | 2000 | 0.500 | 0 |
| 2 | halueval_qa | IN_DOMAIN_CV_AND_POOL | 10000 | 4000 | 2000 | 2000 | 2000 | 0.500 | 0 |
| 3 | halueval_summarization | IN_DOMAIN_CV_AND_POOL | 10000 | 4000 | 2000 | 2000 | 2000 | 0.500 | 0 |
| 4 | truthful_qa | IN_DOMAIN_CV_AND_POOL | 817 | 1634 | 817 | 817 | 817 | 0.500 | 0 |
| 5 | halueval_general | IN_DOMAIN_CV_AND_POOL | 4507 | 4507 | 4507 | 3692 | 815 | 0.181 | 0 |
| 6 | faithdial | UNSEEN_ZEROSHOT_TEST | 3539 | 3507 | 791 | 946 | 2561 | 0.730 | 32 |
| 7 | wikibio_gpt3 | UNSEEN_ZEROSHOT_TEST | 1908 | 1908 | 238 | 516 | 1392 | 0.730 | 0 |
| 8 | xsum_factuality | UNSEEN_ZEROSHOT_TEST | 5597 | 1868 | 498 | 185 | 1683 | 0.901 | 1 |
| 9 | fever | UNSEEN_CLAIM_VERIFICATION_TRANSFER | 18999 | 6666 | 6666 | 3333 | 3333 | 0.500 | 12333 |
| 10 | trivia_qa | Closed-Book Mitigation (Cal+Test) | 17944 | 250 cal + 250 test | 500 | Dynamic | Dynamic | 0.660 (test) | 0 |
