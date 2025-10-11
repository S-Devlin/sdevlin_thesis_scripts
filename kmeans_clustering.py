import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

def read_excel_data(file_path, sheet_name=0):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Successfully loaded {len(df)} samples from Excel file")
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def validate_data(df):
    if len(df.columns) < 3:
        print(f"Error: Need at least 3 columns, found {len(df.columns)}")
        return False
    
    first_col = df.iloc[:, 0]
    if pd.api.types.is_numeric_dtype(first_col) and first_col.dtype in ['int64', 'int32']:
        print("Warning: First column appears to be integers - expected sample names")
    
    second_col = df.iloc[:, 1]
    third_col = df.iloc[:, 2]
    
    if not pd.api.types.is_numeric_dtype(second_col):
        print("Error: Second column (PC1) should contain numeric values")
        return False
    
    if not pd.api.types.is_numeric_dtype(third_col):
        print("Error: Third column (PC2) should contain numeric values")
        return False
    
    print(f"Data validation passed:")
    print(f"  Column 1 ({df.columns[0]}): Sample names")
    print(f"  Column 2 ({df.columns[1]}): PC1 coordinates (numeric)")
    print(f"  Column 3 ({df.columns[2]}): PC2 coordinates (numeric)")
    
    return True

def find_elbow(k_values, wss_values):
    k_norm = np.array(k_values) / max(k_values)
    wss_norm = np.array(wss_values) / max(wss_values)
    
    distances = []
    for i in range(len(k_norm)):
        x1, y1 = k_norm[0], wss_norm[0]
        x2, y2 = k_norm[-1], wss_norm[-1]
        x0, y0 = k_norm[i], wss_norm[i]
        
        distance = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / np.sqrt((y2-y1)**2 + (x2-x1)**2)
        distances.append(distance)
    
    return k_values[np.argmax(distances)]

def calculate_elbow_plot(data):
    wss = []
    k_range = range(1, min(11, len(data)))  
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        wss.append(kmeans.inertia_)
    
    return k_range, wss

def create_wss_dataframe(k_range, wss, optimal_k):
    wss_df = pd.DataFrame({
        'K_Value': list(k_range),
        'WSS': wss,
        'Is_Optimal': [k == optimal_k for k in k_range]
    })
    return wss_df

def perform_clustering(data, sample_names, optimal_k):
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_assignments = kmeans.fit_predict(data)
    centroids = kmeans.cluster_centers_
    
    return cluster_assignments, centroids

def create_results_dataframe(df, cluster_assignments, centroids, optimal_k):
    results_df = df.copy()
    results_df['Cluster'] = cluster_assignments + 1  
    
    centroids_df = pd.DataFrame({
        'Cluster': range(1, optimal_k + 1),
        'Centroid_PC1': centroids[:, 0],
        'Centroid_PC2': centroids[:, 1],
        'Cluster_Size': [np.sum(cluster_assignments == i) for i in range(optimal_k)]
    })
    
    return results_df, centroids_df

def save_results_to_excel(results_df, centroids_df, wss_df, output_path, optimal_k):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='Cluster_Results', index=False)
        
        wss_df.to_excel(writer, sheet_name='WSS_Analysis', index=False)
        
        centroids_df.to_excel(writer, sheet_name='Centroids', index=False)
        
        summary_df = pd.DataFrame({
            'Analysis_Parameter': [
                'Optimal_Number_of_Clusters',
                'Total_Samples',
                'Min_WSS_Value',
                'Max_WSS_Value',
                'WSS_at_Optimal_K'
            ],
            'Value': [
                optimal_k,
                len(results_df),
                wss_df['WSS'].min(),
                wss_df['WSS'].max(),
                wss_df[wss_df['Is_Optimal']]['WSS'].iloc[0]
            ]
        })
        summary_df.to_excel(writer, sheet_name='Analysis_Summary', index=False)
        
        cluster_sizes_df = pd.DataFrame({
            'Cluster': range(1, optimal_k + 1),
            'Sample_Count': [np.sum(results_df['Cluster'] == i) for i in range(1, optimal_k + 1)]
        })
        cluster_sizes_df.to_excel(writer, sheet_name='Cluster_Sizes', index=False)
        
        for cluster_id in range(1, optimal_k + 1):
            cluster_samples = results_df[results_df['Cluster'] == cluster_id]
            sheet_name = f'Cluster_{cluster_id}_Data'
            cluster_samples.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    input_file = "path/to/input/excel.xlsx" 
    output_file = "path/to/output/excel.xlsx" 
    
    print("K-means Clustering Analysis with Elbow Method")
    print("=" * 50)
    
    print("1. Reading data from Excel file...")
    df = read_excel_data(input_file)
    if df is None:
        return
    
    if not validate_data(df):
        return
    
    data = df.iloc[:, [1, 2]].values  
    sample_names = df.iloc[:, 0].values  
    
    print(f"Loaded {len(data)} samples with PC1 and PC2 coordinates")
    
    print("\n2. Calculating optimal number of clusters...")
    k_range, wss = calculate_elbow_plot(data)
    optimal_k = find_elbow(list(k_range), wss)
    
    print(f"Optimal number of clusters: {optimal_k}")
    
    print(f"\n3. Performing k-means clustering with k={optimal_k}...")
    cluster_assignments, centroids = perform_clustering(data, sample_names, optimal_k)
    
    print("\n4. Creating comprehensive results...")
    results_df, centroids_df = create_results_dataframe(df, cluster_assignments, centroids, optimal_k)
    wss_df = create_wss_dataframe(k_range, wss, optimal_k)
    
    print(f"\n5. Saving all results to Excel for Prism analysis...")
    save_results_to_excel(results_df, centroids_df, wss_df, output_file, optimal_k)
    
    print(f"\nAnalysis complete! Results saved to: {output_file}")
    print(f"Excel file contains sheets ready for Prism:")
    print(f"  - Cluster_Results: Sample data with cluster assignments")
    print(f"  - WSS_Analysis: Elbow plot data (K vs WSS values)")
    print(f"  - Centroids: Centroid coordinates for each cluster")
    print(f"  - Analysis_Summary: Key statistics and optimal K")
    print(f"  - Cluster_Sizes: Number of samples per cluster")
    print(f"  - Cluster_X_Data: Individual data for each cluster")
    print(f"\nOptimal clusters: {optimal_k}")
    print(f"Total samples: {len(results_df)}")

if __name__ == "__main__":
    main()
