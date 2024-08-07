"""
Script to import data from Excel file into the database.
"""

import pandas as pd
import os
from app import db, create_app
from app.models import LifecycleStage, ToolCategory, Tool

def clean_column_names(df):
    """Clean column names by removing newlines and extra spaces."""
    df.columns = df.columns.str.replace('\n', ' ').str.strip()
    return df

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
        df_stages = clean_column_names(df_stages)
        print("Columns in the first sheet:")
        print(df_stages.columns.tolist())
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Map expected column names to actual column names
    column_mapping = {
        'Research Data Lifecycle Stage': 'RESEARCH DATA  LIFECYCLE STAGE',
        'Tool Category Type': 'TOOL CATEGORY TYPE',
        'Description': 'DESCRIPTION (1 SENTENCE)',
        'Examples': 'EXAMPLES'
    }

    print("Column mapping:")
    print(column_mapping)

    # Import lifecycle stages
    stages = {}
    for index, row in df_stages.iterrows():
        try:
            stage_name = row[column_mapping['Research Data Lifecycle Stage']].strip()
            stage = LifecycleStage(
                name=stage_name,
                description=row[column_mapping['Description']]
            )
            db.session.add(stage)
            stages[stage_name] = stage
            
            category = ToolCategory(
                name=row[column_mapping['Tool Category Type']],
                description=row[column_mapping['Description']],
                stage=stage
            )
            db.session.add(category)
            
            examples = row[column_mapping['Examples']]
            if pd.notna(examples):
                for exemplar in str(examples).split(','):
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

    # Commit the changes for stages and initial tools
    db.session.commit()

    # Import tools from other sheets
    for sheet_name in pd.ExcelFile(file_path).sheet_names[1:]:
        if sheet_name not in stages:
            print(f"Skipping sheet {sheet_name} as it's not a lifecycle stage")
            continue

        try:
            df_tools = pd.read_excel(file_path, sheet_name=sheet_name, header=6)
            df_tools = clean_column_names(df_tools)
            print(f"\nColumns in sheet {sheet_name}:")
            print(df_tools.columns.tolist())
        except Exception as e:
            print(f"Error reading sheet {sheet_name}: {e}")
            continue

        stage = stages[sheet_name]

        for index, row in df_tools.iterrows():
            try:
                category = ToolCategory.query.filter_by(name=row['TOOL TYPE'], stage=stage).first()
                if not category:
                    category = ToolCategory(name=row['TOOL TYPE'], stage=stage)
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