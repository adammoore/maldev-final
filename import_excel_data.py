"""
Script to import data from Excel file into the database.
"""

import pandas as pd
from app import db, create_app
from app.models import LifecycleStage, ToolCategory, Tool, LifecycleConnection

def import_excel_data(file_path):
    """
    Import data from Excel file into the database.
    
    Args:
        file_path (str): Path to the Excel file
    """
    # Read the first sheet (lifecycle stages and exemplars)
    df_stages = pd.read_excel(file_path, sheet_name=0)
    
    # Import lifecycle stages
    for index, row in df_stages.iterrows():
        stage = LifecycleStage(
            name=row['Research Data Lifecycle Stage'],
            description=row['Description'],
            order=index
        )
        db.session.add(stage)
        
        # Import tool categories and exemplars
        category = ToolCategory(
            name=row['Tool Category Type'],
            description=row['Description (1 SENTENCE)'],
            stage=stage
        )
        db.session.add(category)
        
        # Import exemplar tools
        for exemplar in row['EXAMPLES'].split(','):
            tool = Tool(
                name=exemplar.strip(),
                category=category
            )
            db.session.add(tool)
    
    # Import tools from other sheets
    for sheet_name in pd.ExcelFile(file_path).sheet_names[1:]:
        df_tools = pd.read_excel(file_path, sheet_name=sheet_name, header=6)
        stage = LifecycleStage.query.filter_by(name=sheet_name).first()
        
        for index, row in df_tools.iterrows():
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
    
    # Import lifecycle connections (you may need to adjust this based on your Excel structure)
    # This is a placeholder and may need to be updated based on how connections are represented in your Excel file
    stages = LifecycleStage.query.order_by(LifecycleStage.order).all()
    for i in range(len(stages) - 1):
        connection = LifecycleConnection(
            from_stage=stages[i],
            to_stage=stages[i+1],
            connection_type='normal'
        )
        db.session.add(connection)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        import_excel_data('data/research_data_lifecycle.xlsx')
    