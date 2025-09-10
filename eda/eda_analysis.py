import os 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
from src.logger import logging
from src.exceptions import CustomException


images_folder = os.getenv("STATIC_DIR" , "images_folder")
os.makedirs(images_folder, exist_ok=True)


class OverallImages:
    def __init__(self , dataframe : pd.DataFrame):
        self.df = dataframe

    
        #self.Banks = self.df['bank'].unique().tolist()
    
    def metricimages(self):
        ### Get different bank location images 
        Banks = self.df['Bank'].unique().tolist()
        for banktype in Banks: 

            bank_data = self.df[self.df['Bank'] == banktype]
            bank_folder = os.path.join(images_folder, banktype)
            os.makedirs(bank_folder, exist_ok=True)
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'Distributions of Key Mortgage Metrics ~{banktype}', fontsize=16)

            sns.histplot(data = bank_data, x='LoanAcquisitionActualUPBAmt', ax=axes[0, 0], kde=True)
            axes[0, 0].set_title('Loan Acquisition Actual UPB Amount ~{bank}')

            sns.histplot(data=bank_data, x='HUDMedianIncomeAmount', ax=axes[0, 1], kde=True)
            axes[0, 1].set_title(f'HUD Median Income Amount ~{banktype}')

            sns.histplot(data=bank_data, x='TotalDebtExpenseRatioPercent', ax=axes[1, 0], kde=True)
            axes[1, 0].set_title(f'Total Debt Expense Ratio (%) ~{banktype}')

            sns.histplot(data=bank_data, x='LTVRatioPercent', ax=axes[1, 1], kde=True)
            axes[1, 1].set_title(f'Loan-to-Value Ratio at Origination (%) ~ {banktype}')

            # Improve layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            filename = f"Distributions of Key Mortgage Metrics_{banktype}.png"
            bank_filesave_path = os.path.join(bank_folder,filename)
            plt.savefig(bank_filesave_path, dpi=150)
            plt.close()
        
    #def lower_income_area(self):
            ##### Loan Distribution by Income Area
            sns.set(style="whitegrid")

            fig_IncomeAreaCategory = sns.countplot(data=bank_data, x='IncomeAreaCategory',
                                                hue = 'IncomeAreaCategory', 
                                                palette='Blues_d' , legend=False)

            plt.title(f"Loan Distribution by Income Area ~{banktype}", fontsize=16, weight='bold')
            plt.xlabel("Income Area Category")
            plt.ylabel("Number of Loans")
            plt.tight_layout()
            #plt.savefig(f"{fig_IncomeAreaCategory}", dpi=150)
            incomeareaimage_file_name = f'income_area_category_plot_{banktype}.png'
            incomearea_path = os.path.join(bank_folder , incomeareaimage_file_name)
            plt.savefig(incomearea_path, dpi=150)
            plt.close()
            
            logging.info(f"Income Area Category image saved_{banktype}  {fig_IncomeAreaCategory}")
            #plt.show()

                  
            ###### Loan to Value Risk Category 
            colors = {
                'Lower_Risk_LTV': '#1f77b4',   # Blue
                'Higher_Risk_LTV': '#ff7f0e'   # Orange
            }

            # Draw countplot with specific color mapping
            fig_LTVCategory = sns.countplot(data= bank_data, x='LTV_category_column',hue='LTV_category_column',
                                            palette=[colors[val] for val in self.df['LTV_category_column'].unique()]
                                            ,legend = False)

            ltv_file_name = f'ltv_category_plot_{banktype}.png'
            ltv_file_save_path = os.path.join(bank_folder , ltv_file_name)
            plt.savefig(ltv_file_save_path, dpi=150)
            plt.close()
                #plt.show()
            logging.info(f"Loan to Value Category saved_{banktype} {fig_LTVCategory}")   

        

        


            
