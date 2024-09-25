# Setup

`pip install -r requirements.in`

Edit `app.py` `Settings` with the MongoDB name and connection string (default is localhost)

Mongodb on Docker:

`docker run -d --rm --name mongodb -p 27017:27017 mongodb/mongodb-community-server:latest` 

# Run

Run the app:

`python app.py`

Connect to admin:

`http://127.0.0.1/admin`

# Export/import

`python impexp <command> <filepath>`

where command may be:

*   import-system
*   import-tasks
*   export-system
*   export-tasks

For import-\* file path is the input JSON.

For export-\* file path is the output JSON.

In the project the sample input files are under ./admin/ and the sample output files are under ./exported/