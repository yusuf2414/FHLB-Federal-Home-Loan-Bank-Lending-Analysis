import os 
from src.data_sourcing import DataCombining
from src.data_sourcing import Data_Transformation
from eda.eda_analysis import OverallImages




combiner = DataCombining()
combined_df = combiner.data_combination()
Transformation_instance = Data_Transformation(combined_df)
final_combination = Transformation_instance.add_format_columns()
Images_class_instance = OverallImages(dataframe = combined_df)
Images_class_instance.metricimages()
Images_class_instance.lower_income_area()


