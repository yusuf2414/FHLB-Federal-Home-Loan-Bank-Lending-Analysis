import os
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)

### default for the multiple years csv starting from 
data_folder = os.getenv("DATA_DIR", "data_folder")
os.makedirs(data_folder, exist_ok=True)

combined_data_folder = os.getenv("DATA_DIR", "combined_data_folder")
os.makedirs(combined_data_folder, exist_ok=True)

class DataCombining:
    def __init__(self):
        self.folder_path = data_folder  
        self.contents = os.listdir(self.folder_path)
    
    def data_combination(self):
        combined_df = pd.DataFrame()

        try:
            for item in self.contents:
                if item.endswith('.csv'):
                    file_path = os.path.join(self.folder_path, item)
                    df = pd.read_csv(file_path)

                    print(f"Reading file: {item}")
                    print(f"File path: {len(df.columns)}")

                    combined_df = pd.concat([combined_df, df], ignore_index=True)

            #combined_df_path = os.path.join(combined_data_folder, 'combined_df.csv')
            #combined_df.to_csv(combined_df_path, index=False, header=True)
            #print(f"Combined CSV saved to: {combined_df_path}")

            self.combined_df = combined_df

            return combined_df

        except Exception as e:
            logging.error(f"Error while combining files: {e}")
            raise

class Data_Transformation:
    def __init__(self, combined_df):  
        self.combined_df = combined_df

    def add_format_columns(self):
        LTV_category_column = []
        for i in range(len(self.combined_df['LTVRatioPercent'])):
            if self.combined_df['LTVRatioPercent'].iloc[i] <= 80:
                LTV_category_column.append('Lower_Risk_LTV')
            else:
                LTV_category_column.append('Higher_Risk_LTV')

            ####Create another df 
        self.combined_df['LTV_category_column'] = LTV_category_column

        
        ### Change adjusting name for borrower 1 and 2 , race , sex 
        race_map = { 
                1: 'American_indian',2: 'Asian',
                3: 'African_American',4: 'Native_Hawaiian',
                5: 'White', 6: 'N/A',7: 'Institution'       
            }

        self.combined_df['Borrower1Race1Type'] = self.combined_df['Borrower1Race1Type'].map(race_map)
        self.combined_df['Borrower1Race2Type'] = self.combined_df['Borrower1Race2Type'].map(race_map)

        sex_map = {
             1 : 'Male', 2 :'Female'
        }
        self.combined_df['Borrower1SexType'] = self.combined_df['Borrower1SexType'].map(sex_map)
        self.combined_df['Borrower2SexType'] = self.combined_df['Borrower2SexType'].map(sex_map)
        
        self.combined_df['Borrower1Race1Type'] = self.combined_df['Borrower1Race1Type'].map(race_map)
        #####

        #### Checking the income area category to see if individuals that are being borrowed belong to which category 
        income_area = []

        for i in range(len(self.combined_df)):
            determinant = 0.8 * self.combined_df['HUDMedianIncomeAmount'].iloc[i]
            if self.combined_df['CensusTractMedFamIncomeAmount'].iloc[i] < determinant:
                income_area.append('Lower_income_area')
            else:
                income_area.append('high_income_area')

        self.combined_df['IncomeAreaCategory'] = income_area

        print(f"Number of columns in the new combined df: {len(self.combined_df.columns)}")
        combined_df_path = os.path.join(combined_data_folder, 'combined_df.csv')
        self.combined_df.to_csv(combined_df_path, index=False, header=True)

        return self.combined_df
   

# if __name__ == "__main__":
#     combiner = DataCombining()
#     combined_df = combiner.data_combination()
#     Transformation_instance = Data_Transformation(combined_df)
#     final_combination = Transformation_instance.add_format_columns()