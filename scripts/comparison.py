import pandas as pd
import matplotlib.pyplot as plt

def comparison():
    
	baseline = pd.read_csv("baseline_results.csv")
	curated = pd.read_csv("curated_results.csv")
	results = pd.concat([baseline, curated]).reset_index(drop=True)
	results.to_csv("model_comparison.csv", index=False)
  
	print(results)
  
	#F1 compare

	plt.figure(figsize=(8,5))
	plt.bar(results["Model"], results["F1"])
	plt.title("F1 Score Comparison")
	plt.ylabel("F1 Score")
	plt.xticks(rotation=30)

	plt.tight_layout()
	plt.savefig("f1_model_comparison.png")
	plt.show()


	#ROC AUC	

	plt.figure(figsize=(8,5))
	plt.bar(results["Model"], results["ROC_AUC"])
	plt.title("ROC_AUC Comparison")
	plt.ylabel("ROC_AUC")
	plt.xticks(rotation=30)

	plt.tight_layout()
	plt.savefig("roc_auc_model_comparison.png")
	plt.show()

	#Recall

	plt.figure(figsize=(8,5))
	plt.bar(results["Model"], results["Recall"])
	plt.title("Recall Comparison")
	plt.ylabel("Recall")
	plt.xticks(rotation=30)

	plt.tight_layout()
	plt.savefig("recall_model_comparison.png")
	plt.show()


	#precision

	plt.figure(figsize=(8,5))
	plt.bar(results["Model"], results["Precision"])
	plt.title("Precision Comparison")
	plt.ylabel("Precision")
	plt.xticks(rotation=30)

	plt.tight_layout()
	plt.savefig("precision_model_comparison.png")
	plt.show()
