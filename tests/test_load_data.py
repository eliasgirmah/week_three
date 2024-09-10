import sys
import os

# Add the parent directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# Import functions from scripts
from scripts.load_data import load_data_from_postgres, load_data_using_sqlalchemy

def test_empty_query():
    result = load_data_from_postgres("")
    assert result is None, "Empty query should return None"

def test_invalid_sql_query():
    result = load_data_from_postgres("SELECT * FROM non_existing_table")
    assert result is None, "Invalid query should return None"
