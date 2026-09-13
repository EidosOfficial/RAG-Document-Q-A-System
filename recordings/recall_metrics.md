**Retrieval Evaluation Metrics (Top K)**

| **Top-K** | **Total Hits** | **Recall@K (%)** | **Avg Latency (ms)** | **Key Finding** |
| -------- | -------- | -------- | -------- | -------- |
| 1  | 10/14  | 71.43% | 92.41 | High Speed but misses 4 boundary questions |
| 2  | 11/14  | 78.57% | 93.91 | Noticable improvement |
| 3  | 13/14  | 92.86% | 93.27 | **Optimal Sweet Spot!** Huge +21.4% recall jump |
| 5  | 13/14  | 92.86% | 91.55 | Diminishing returns (same accuracy as k=3) |
