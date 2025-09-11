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
        self.df['Bank'] = self.df['Bank'].str.strip()
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
            # 1) Aggregate: counts by year × IncomeAreaCategory
            counts = (bank_data.groupby(['Year', 'IncomeAreaCategory']).size().rename('n_loans').reset_index())

            # 2) Pivot to wide for plotting multiple lines
            pivot = (counts.pivot(index='Year', columns='IncomeAreaCategory', values='n_loans').sort_index().fillna(0))
                
            # (optional) Ensure full 2018–2023 coverage even if some years are missing:
            all_years = list(range(2018, 2024))
            pivot = pivot.reindex(all_years, fill_value=0)

            # 3) Plot: multi-line time series of counts
            fig, ax = plt.subplots(figsize=(10, 6))

            for col in pivot.columns:
                ax.plot(pivot.index, pivot[col], marker='o', linewidth=2, label=str(col))

            ax.set_title(f"Loan Distribution by Income Area Over Time ~ {banktype}", fontsize=14)
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Loans")
            ax.set_xticks(pivot.index)
            ax.grid(True, axis='y', alpha=0.3)
            ax.legend(title="Income Area Category", ncol=2, frameon=False)

            plt.tight_layout()
            line_fname = f"income_area_category_trend_{banktype}.png"
            line_path = os.path.join(bank_folder, line_fname)
            plt.savefig(line_path, dpi=150)
            plt.close()

            print(f"Saved: {line_path}")
                        
            logging.info(f"Income Area Category image saved_{banktype}")
            #plt.show()
                            
            ###### Loan to Value Risk Category 
            colors = {
                'Lower_Risk_LTV': '#1f77b4',   # Blue
                'Higher_Risk_LTV': '#ff7f0e'   # Orange
            }
            # 1) Aggregate: counts by year × IncomeAreaCategory
            counts2 = (bank_data.groupby(['Year', 'LTV_category_column']).size().rename('n_loans').reset_index())

            # 2) Pivot to wide for plotting multiple lines
            pivot = (counts2.pivot(index='Year', columns='LTV_category_column', values='n_loans').sort_index().fillna(0))
                
            # (optional) Ensure full 2018–2023 coverage even if some years are missing:
            all_years = list(range(2018, 2024))
            pivot = pivot.reindex(all_years, fill_value=0)

            fig, ax = plt.subplots(figsize=(10, 6))

            for col in pivot.columns:
                ax.plot(pivot.index, pivot[col], marker='o', linewidth=2, label=str(col))

            ax.set_title(f"Loan Distribution by Risk level Over Time ~ {banktype}", fontsize=14)
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Loans")
            ax.set_xticks(pivot.index)
            ax.grid(True, axis='y', alpha=0.3)
            ax.legend(title="Risk level Category", ncol=2, frameon=False)

            plt.tight_layout()
            line_fname = f"Risk_trend_{banktype}.png"
            line_path2 = os.path.join(bank_folder, line_fname)
            plt.savefig(line_path2, dpi=150)
            plt.close()

            print(f"Saved: {line_path2}")

                #plt.show()
            #logging.info(f"Loan to Value Category saved_{banktype} {fig_LTVCategory}")   

        

        


            
