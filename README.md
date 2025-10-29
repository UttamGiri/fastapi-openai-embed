

<b>FAST API ENDPOINT TO EMBED FILE AND SEARCH</b>

<b>EMBED</b>
<p>
It takes the uploaded file’s bytes and filename, converts them into vector embeddings, and stores them for later search.
The uploaded file’s bytes are converted into readable text.The text is split into overlapping pieces (1,000 characters each, with 100 characters overlap).
This makes large files manageable and improves embedding quality.Each text chunk becomes a Document object, tagged with metadata about its source file.LangChain + FAISS create numerical embeddings (vectors) for each chunk.These embeddings capture the semantic meaning of the text.The generated FAISS index is saved in your app/embeddings/ folder — this is the vector database used for semantic search.Returns the folder path where the embedding data is stored.
</p>
<b>SEARCH</b>
<p>
Fetches saved FAISS index and finds the most relevant text chunks. The flag allow_dangerous_deserialization=True must be used only if you trust the file (e.g., it was created by your own app).Finds the top 3 chunks that are semantically similar to your query.Returns a clean JSON object showing the query and the matching text snippets.
</p>
```

# fastapi-openai-embed
TO FIX DEPENDENCIES ISSUES
#Just having it in requirements.txt is not enough — you must install it into the Python environment that your editor or Docker uses.
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r app/requirements.txt
# quick check
python -c "import fastapi, fastapi.responses; print('ok')"





# Build and Run


# Build image
docker build -t fastapi-embed-service .

# Run container with .env file
docker run -d -p 8000:8000 --env-file .env fastapi-embed-service

docker ps
docker ps -a
docker logs <container_id>

docker stop <container_id>
docker rm <container_id>


http://localhost:8000/docs

FOR DEBUGGING

docker run -d -p 8080:8000 -p 5678:5678 --env-file .env fastapi-embed-service


CURSOR IDE : RUN > Start Debugging > Python Debugger 
http://localhost:8000/docs

```
