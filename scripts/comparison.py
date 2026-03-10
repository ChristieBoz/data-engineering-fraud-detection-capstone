def comparison():
    
  import pandas as pd
  import matplotlib.pyplot as plt
  
  baseline = pd.read_csv("baseline_results.csv")
  curated = pd.read_csv("curated_results.csv")
  
  results = pd.concat([baseline, curated]).reset_index(drop=True)
  
  results.to_csv("model_comparison.csv", index=False)
  
  print(results)
  
  #visual

  plt.figure(figsize=(8,5))
  plt.bar(results["Model"], results[F1"])
  plt.title("Fraud Detection Model Comparison")
  plt.ylabel("F1 Score")
  plt.xticks(rotation=30)

  plt.tight_layout()
  plt.savefig("model_comparison.png")
  plt.show()
