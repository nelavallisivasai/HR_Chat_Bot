import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class CustomPythonTool:
    def __init__(self):
        # Initialize database connection with provided configuration
        self.conn = psycopg2.connect(
            dbname=os.getenv("db_name"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port")
        )
        self.cursor = self.conn.cursor()

    def run(self, query):
        try:
            # Execute the SQL query
            self.cursor.execute(query)
            # Fetch the result
            result = self.cursor.fetchall()
            # Transform result to the required format: [('lower(column1)'), ('lower(column2)'), ...]
            formatted_result = [(f"lower({row[0]})",) for row in result]
            return formatted_result
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            # Commit if there are any updates
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

python_tool = CustomPythonTool()
    
query = '''
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'employee_details' 
  AND table_schema = 'public'
ORDER BY ordinal_position;
'''

dataset_columns = python_tool.run(query)

print(dataset_columns)
