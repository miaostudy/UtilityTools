# UtilityTools
## Download Datasets from remote
### kaggle
```python
python download.py -u <datasets url>
```


| parameter | 	describe               | 	type	     | default | 	required |
|-----------|-------------------------|------------|---------|-----------|
| -u, --url | 	 Dataset URL (format: username/dataset-name)	 | 	string	   | -	| True      |
|-o, --output|	Output directory	| string     |	./| 	False    |
|--use-proxy	|Whether to enable proxy for downloading		| store_true |	False	| False         |
|-p, --proxy	|Proxy address	| string	    |127.0.0.1:7890| 	False|
|--force	|Force delete files without confirmation| 	store_true   |	False	| False         |
