"""
Script to import data from Excel file into the database.
"""

import pandas as pd
import os
from app import db, create_app
from app.models import LifecycleStage, ToolCategory, Tool, LifecycleConnection

def import_excel_data(file_path):
    """
    Import data from Excel file into the database.
    
    Args:
        file_path (str): Path to the Excel file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found at {file_path}")

    # Read the first sheet (lifecycle stages and exemplars)
    try:
        df_stages = pd.read_excel(file_path, sheet_name=0)
        print("Columns in the first sheet:")
        print(df_stages.columns.tolist())
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Map expected column names to actual column names
    column_mapping = {
        'Research Data Lifecycle Stage': 'RESEARCH DATA LIFECYCLE STAGE',
        'Description': 'DESCRIPTION (1 SENTENCE)',
        'Tool Category Type': 'TOOL CATEGORY TYPE',
        'Examples': 'EXAMPLES'
    }

    # Import lifecycle stages
    for index, row in df_stages.iterrows():
        try:
            stage = LifecycleStage(
                name=row[column_mapping['Research Data Lifecycle Stage']],
                description=row[column_mapping['Description']],
                order=index
            )
            db.session.add(stage)
            
            category = ToolCategory(
                name=row[column_mapping['Tool Category Type']],
                description=row[column_mapping['Description']],
                stage=stage
            )
            db.session.add(category)
            
            for exemplar in row[column_mapping['Examples']].split(','):
                tool = Tool(
                    name=exemplar.strip(),
                    category=category
                )
                db.session.add(tool)
        except KeyError as e:
            print(f"Missing column in Excel file: {e}")
            db.session.rollback()
            return
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            db.session.rollback()
            return

    # Import tools from other sheets
    for sheet_name in pd.ExcelFile(file_path).sheet_names[1:]:
        try:
            df_tools = pd.read_excel(file_path, sheet_name=sheet_name, header=6)
            print(f"\nColumns in sheet {sheet_name}:")
            print(df_tools.columns.tolist())
        except Exception as e:
            print(f"Error reading sheet {sheet_name}: {e}")
            continue

        stage = LifecycleStage.query.filter_by(name=sheet_name).first()
        if not stage:
            print(f"Stage not found for sheet {sheet_name}")
            continue

        for index, row in df_tools.iterrows():
            try:
                category = ToolCategory.query.filter_by(name=row['TOOL CATEGORY TYPE'], stage=stage).first()
                if not category:
                    category = ToolCategory(name=row['TOOL CATEGORY TYPE'], stage=stage)
                    db.session.add(category)
                
                tool = Tool(
                    name=row['TOOL NAME'],
                    description=row['TOOL CHARACTERISTICS (ADDITIONAL USEFUL INFORMATION)'],
                    url=row['LINK TO TOOL (URL)'],
                    category=category
                )
                db.session.add(tool)
            except KeyError as e:
                print(f"Missing column in sheet {sheet_name}, row {index}: {e}")
            except Exception as e:
                print(f"Error processing row {index} in sheet {sheet_name}: {e}")

    try:
        db.session.commit()
        print("Data import completed successfully")
    except Exception as e:
        print(f"Error committing changes to database: {e}")
        db.session.rollback()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        excel_path = os.path.join(os.path.dirname(__file__), 'data', 'research_data_lifecycle.xlsx')
        import_excel_data(excel_path)