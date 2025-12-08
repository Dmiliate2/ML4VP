# GPR Model

MAC data, calcualted from reported values, is available in ./MAC_Antione, NIST Data and MAC data can be found in Stage 0
---

### STAGE0

Data is split into four partitions. 
A LASSO model is trained to include only useful features; the results are recorded. 
Cross validation is employed.

### STAGE1

Initial GPR training is performed using "constant" and "matern52" for the basis and kernel functions, respectively. 
Cross validation is employed.

### STAGE2

The top models are retrained exploring alternative basis and kernel functions. 
Cross validation is employed.

### STAGE3

The top models are retrained using the 3 folds as training and final evaluation with the holdout test set (fold 4).

### STAGE4

The final top models are retrained using all data (no holdout or cross validation) for deployment.

