import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import readData as rd
import numpy as np
import json
class RecommendationModel:
    def __init__(self):
        # Initialize recommendation model and related resources
        pass

    def get_recommendations(self, transection_df, stock_code):
        # Create CustomerID vs Item (Purchased Items, by StockCode) matrix by pivot table function.
        CustomerID_Item_matrix = transection_df.pivot_table(
            index='CustomerID',
            columns='StockCode',
            values='Quantity',
            aggfunc='sum'
        )
        # Update illustration of the matrix, 1 to represent customer have purchased item, 0 to represent customer haven't purchased.
        CustomerID_Item_matrix = CustomerID_Item_matrix.applymap(lambda x: 1 if x > 0 else 0)
        # Create Item to Item similarity matrix.
        item_item_similarity_matrix = pd.DataFrame(
            cosine_similarity(CustomerID_Item_matrix.T)
        )
        # Update index to corresponding Item Code (StockCode).
        item_item_similarity_matrix.columns = CustomerID_Item_matrix.T.index
        item_item_similarity_matrix['StockCode'] = CustomerID_Item_matrix.T.index
        item_item_similarity_matrix = item_item_similarity_matrix.set_index('StockCode')

        # Randomly pick StockCode (23166) to display the most similar StockCode.
        top_5_similar_items = list(item_item_similarity_matrix.loc[stock_code].sort_values(ascending=False)\
                                  [item_item_similarity_matrix.loc[stock_code].sort_values(ascending=False)<1].iloc[:5].index
        )
        print(type(top_5_similar_items))
        return top_5_similar_items
    
    def get_final_recommendations(self, transection_df, stockcodes ):
        final_recommendations =[]
        for stockcode in stockcodes:
            if stockcode == 'no_item_found':
                # If 'llm_item' is 'no_item_found', set 'Recommended_Items' to "no_recommendations"
                return json.dumps("no_recommendations")
            else:
                recommendations=self.get_recommendations(transection_df, stockcode)
                print(type(recommendations))
                return recommendations
           # final_recommendations.append(recommendation)
        #return json.dumps(recommendation)