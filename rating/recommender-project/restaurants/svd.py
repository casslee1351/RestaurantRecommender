import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

import joblib

def train_svd(data):
    # Compute the SVD of the data
    U, s, Vt = svds(data, k=20)
    # Create the SVD model
    model = (U, s, Vt)
    # Save the model to a file using joblib
    joblib.dump(model, 'svd_model.joblib')

def predict_svd(user_id, item_id):
    # Load the SVD model from the file using joblib
    U, s, Vt = joblib.load('svd_model.joblib')
    # Compute the predicted rating for the user and item
    pred_rating = (U[user_id - 1, :] * np.diag(s) * Vt[:, item_id - 1]).sum()
    # Return the predicted rating
    return pred_rating
### TODO: TEST JOBLIB IMPLEMENTATION - EDIT TRAIN AND PREDICT FUNCTIONS TO SUIT MY USE CASE
def computeSVD(df):
    """
    columns of df must be in user, name, rating format
    """
    df['rating'] = df['rating'].astype('float')
    pivoted = pd.pivot_table(data=df, index="user", columns="name", values="rating", fill_value=0., aggfunc=np.sum)
    avg = pivoted.mean(axis=1)
    user_item_centered = pivoted.sub(avg, axis=0)
    u, e, vt = svds(user_item_centered.to_numpy(), k=5)
    recalc = np.dot(u, np.dot(np.diag(e), vt))
    recalc = recalc + avg.values.reshape(-1, 1)
    recs = pd.DataFrame(recalc,
                   index=pivoted.index,
                   columns=pivoted.columns)
    recs["user"] = recs.index
    recs = pd.melt(recs, id_vars=["user"])
    recs = recs.groupby(['user']).apply(lambda x: x.sort_values(by='value', ascending=False)).reset_index(drop=True)
    
    recs = recs[["user", "name"]]
    return recs