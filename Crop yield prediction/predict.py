import pandas as pd
import numpy as np
import pickle

def predict_crop_yield(new_data):
    """
    Make predictions using the trained KNN model
    
    Parameters:
    new_data (pd.DataFrame): DataFrame containing new data for prediction
    with columns: 'State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Area'
    
    Returns:
    np.array: Predicted crop production values
    """
    # Load the saved model, scaler, and label encoders
    with open('knn_crop_yield_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    
    # Preprocess the new data
    # Handle categorical features using the saved label encoders
    for col in ['State_Name', 'District_Name', 'Season', 'Crop']:
        if col in new_data.columns:
            le = label_encoders[col]
            # Transform known categories
            new_data[col] = new_data[col].map(lambda x: 
                le.transform([x])[0] if x in le.classes_ else -1)
            
            # Handle unknown categories
            if (new_data[col] == -1).any():
                print(f"Warning: Unknown categories found in {col}")
    
    # Select features in the same order as training
    X_new = new_data[['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Area']]
    
    # Scale the features
    X_new_scaled = scaler.transform(X_new)
    
    # Make predictions
    predictions = model.predict(X_new_scaled)
    
    return predictions

# Example usage:
if __name__ == "__main__":
    # Sample data for prediction
    sample_data = pd.DataFrame({
        'State_Name': ['Kerala'],
        'District_Name': ['THRISSUR'],
        'Crop_Year': [2025],  # Future year
        'Season': ['Whole Year'],
        'Crop': ['Banana'],
        'Area': [2283.36]
    })
    
    # Make predictions
    predicted_yield = predict_crop_yield(sample_data)
    
    # Display results
    sample_data['Predicted_Production'] = predicted_yield
    print("\nPrediction Results:")
    print(sample_data[['State_Name', 'District_Name', 'Crop', 'Area', 'Predicted_Production']])
    
    # Example for batch prediction from a CSV file
    # Uncomment the following code to use it
    """
    # Load data from CSV file
    new_data = pd.read_csv('new_crop_data.csv')
    
    # Make predictions
    predictions = predict_crop_yield(new_data)
    
    # Add predictions to the dataframe
    new_data['Predicted_Production'] = predictions
    
    # Save results
    new_data.to_csv('crop_yield_predictions.csv', index=False)
    print("Predictions saved to 'crop_yield_predictions.csv'")
    """


    # Kerala,THRISSUR,2010,Whole Year ,Banana,2283.36,17962.59