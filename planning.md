# Project Research and Findings


### Source
---

Godot Docs: https://github.com/godotengine/godot-docs

### Build From Source
---

We are required to use `Sphinx` to transform the `.rst` format repository content into structured `.fjson` files. 

Sphinx is already included as a dependency in the Godot Docs repo, and can be installed with `pip install -r requirements.txt`

### Data Cleaning
---

Now that we have the structured files, we need to extract the useful text content from the surrounding HTML tags and unneeded markup (like headers, nav and footers). We should create and run a Python script for this.

`BeautifulSoup` is a good Python library for this task.

### Semantic Chunking
---

We'll also need to semantically chunk the data, ideally within the same script where we clean the data. The chunked data should be stored as a new .json file. 

It's up to whoever takes this task how to semantically seperate the data (by header, by page title, by sections etc.) but we should avoid making chunks too large or too broad.

### Vectorization
---

We're required to use either `Chroma` or `FAISS` to vectorize the data and set up a vector database. To use them, we'll need to create and run a script to initialize a local embedding model, pull the chunks, calculate their vector representations, and save them in a database folder.

Note that this takes a LONG time, because you're running Sentence Transformers locally. Expect anywhere from 30 minutes to an hour of processing time. 

