import pandas as pd
from io import BytesIO

def generate_excel_file(data):
    
    df = pd.DataFrame(data)
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Categories')
    excel_buffer.seek(0)
    return excel_buffer


