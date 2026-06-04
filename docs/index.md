# Python Programming Guide

Structured notes and reference for Python3

## :material-language-python: What's here

| Section | Topic | Highlights |
|---|---|---|
| :material-school: [Tutorial](versions/3.14.5/tutorial/index.md) | Getting started | Interpreter, syntax, data structures, modules, classes, exceptions, venv |
| :material-bookshelf: [Standard Library](versions/3.14.5/standard-library/index.md) | Built-in modules | I/O, networking, data types, concurrency, development tools |
| :material-file-document: [Language Reference](versions/3.14.5/language-reference/index.md) | Syntax and semantics | Lexical analysis, data model, statements, imports, grammar |


## :material-chart-tree: Data structures and algorithms

| Section | Topic | Highlights |
|---|---|---|
| :material-chart-tree: [Overview](dsa/index.md) | Hub and learning roadmap | Complexity, recursion, structures, sorting and searching |
| :material-timer-sand-empty: [Complexity](dsa/complexity/index.md) | Time and space analysis | Big O, best/worst/average case, trade-offs |
| :material-repeat: [Recursion](dsa/recursion/index.md) | Thinking recursively | Recurrence relations, call stack, base and inductive step, tail recursion |
| :material-algorithm: [Data structures](dsa/data-structures/index.md) | Core structures | Lists, trees, heaps, graphs, hash tables |
| :material-algorithm: [Algorithms](dsa/algorithms/index.md) | Sorting and searching | Comparison sorts, radix and bucket sort, quickselect |

## :material-brain: Coding Interview Practice

| Subject | Description |
|---------|-------------|
| [LeetCode](leetcode/index.md) | Coding interview practice problems and solutions organized by topic and difficulty. |

## :material-web: Web Development

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-lightning-bolt: FastAPI](https://fastapi.tiangolo.com/) | FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. |

## :material-database-outline: Database

### :material-link-variant: Object-Relational Mappers (ORM)

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-database: SQLAlchemy](https://www.sqlalchemy.org/) | SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. |

### :material-table-large: Relational Databases (RDBMS)

| :material-database: Database | :material-information-outline: Description |
|---|---|
| [:material-elephant: PostgreSQL](https://www.postgresql.org/) | PostgreSQL is a powerful, open-source object-relational database system that supports advanced features like ACID transactions, foreign keys, and complex queries. |

### :material-database: NoSQL Databases

| :material-database: Database | :material-information-outline: Description |
|---|---|
| [:material-leaf: MongoDB](https://www.mongodb.com/) | MongoDB is a popular, open-source NoSQL database that uses a document-oriented data model, offering flexible schema design and horizontal scalability. |
| [:material-blur: Cassandra](https://cassandra.apache.org/) | Cassandra is a distributed, column-oriented database designed for high availability and scalability, popular for big data and real-time applications. |
| [:material-flash: Redis](https://redis.io/) | Redis is an in-memory, open-source data structure store, used as a database, cache, and message broker, known for its high performance and flexibility. |
| [:material-graph: Neo4j](https://neo4j.com/) | Neo4j is a graph database management system that stores data as nodes and relationships, enabling powerful graph queries and traversals for complex data relationships. |


## :material-table: Data Manipulation & Analysis

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-table-large: Pandas](https://pandas.pydata.org/) | Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. |
| [:material-chart-areaspline: NumPy](https://numpy.org/) | NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays. |
| [:material-function-variant: SciPy](https://www.scipy.org/) | SciPy is a library for scientific computing in Python. It features various tools for optimization, integration, interpolation, linear algebra, Fourier transforms, signal processing, and more. |

## :material-chart-bar: Data Visualization

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-chart-line: Matplotlib](https://matplotlib.org/) | Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. |
| [:material-palette: Seaborn](https://seaborn.pydata.org/) | Seaborn is a library for making statistical graphics in Python. It is built on top of Matplotlib and integrates closely with pandas data structures. |
| [:material-poll: Plotly](https://plotly.com/) | Plotly is a Python library for creating interactive, publication-quality graphs. |

## :material-magnify: Search engines

| :material-magnify: Search Engine | :material-information-outline: Description |
|---|---|
| [:material-cloud-search: Elasticsearch](https://www.elastic.co/elasticsearch/) | Elasticsearch is a distributed, open-source search and analytics engine for building real-time applications, offering powerful full-text search, aggregation, and analytics capabilities. |
| [:material-cloud-search-outline: Solr](https://solr.apache.org/) | Solr is a search platform built on Apache Lucene, offering full-text search, faceted navigation, and analytics for large datasets. |
| [:material-book-search: Sphinx](https://www.sphinxsearch.com/) | Sphinx is a full-text search server that provides fast, relevant search results for web applications and websites. |
| [:material-file-search: Whoosh](https://whoosh.readthedocs.io/) | Whoosh is a fast, pure Python full-text indexing and searching library, ideal for building custom search engines and applications. |

## :material-brain: AI Engineering & Machine Learning

### :material-robot-outline: AI Agents Frameworks

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-graph-outline: LangChain](https://python.langchain.com/) / [:material-graph: LangGraph](https://langchain-ai.github.io/langgraph/) | LangChain is a framework for building LLM-powered applications with composable chains, tools, and retrieval; LangGraph extends it with graph-based orchestration for stateful, multi-step agents and workflows. |
| [:material-link-variant: LlamaIndex](https://docs.llamaindex.ai/) | LlamaIndex is a data framework for connecting custom data sources to large language models, with tools for ingestion, indexing, retrieval, and building RAG pipelines. |

### :material-cog-transfer: LLM Fine-Tuning & Inference

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-robot-industrial: Hugging Face Transformers](https://huggingface.co/docs/transformers/en/index) | Transformers is a library for natural language processing, providing pre-trained models and tools for fine-tuning and inference. |
| [:material-robot: OpenAI](https://openai.com/) | OpenAI is a company that provides a platform for building AI applications, including a library for fine-tuning and inference. |
| [:material-robot: Anthropic](https://www.anthropic.com/) | Anthropic is a company that provides a platform for building AI applications, including a library for fine-tuning and inference. |

### :material-vector-combine: Vector Databases

| :material-database: Database | :material-information-outline: Description |
|---|---|
| [:material-vector-arrange: Pinecone](https://www.pinecone.io/) | Pinecone is a fully managed vector database service designed for similarity search and AI applications, enabling fast and scalable retrieval of embeddings for tasks like semantic search and recommendation. |
| [:material-vector-difference-ab: Weaviate](https://weaviate.io/) | Weaviate is an open-source vector database with built-in machine learning and support for hybrid search, semantic search, and generative AI integrations. |
| [:material-vector-point: Milvus](https://milvus.io/) | Milvus is a high-performance, open-source vector database that supports scalable storage and similarity search of vector embeddings, popular for AI and deep learning applications. |
| [:material-vector-square: Qdrant](https://qdrant.tech/) | Qdrant is an open-source vector similarity search engine and database, offering efficient and reliable search and filtering of large-scale embedding data. |
| [:material-vector-arrange-ab: Chroma](https://www.trychroma.com/) | Chroma is a simple, open-source embedding database for AI applications, providing easy-to-use APIs and persistent storage for vector data. |

### :material-chart-scatter-plot: Core Machine Learning & Statistical Modeling

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-brain: Scikit-learn](https://scikit-learn.org/) | Scikit-learn is a machine learning library for Python. It features various classification, regression and clustering algorithms including support vector machines, random forests, gradient boosting, k-means and DBSCAN, and is designed to interoperate with the Python numerical and scientific libraries NumPy and SciPy. |
| [:material-chart-bell-curve: Statsmodels](https://www.statsmodels.org/) | Statsmodels is a library for statistical modeling and econometrics in Python. It features various tools for regression analysis, time series analysis, and more. |

### :material-chart-timeline-variant: Gradient Boosting Libraries

| :material-folder-open-outline: Library | :material-information-outline: Description |
|---|---|
| [:material-chart-donut: XGBoost](https://xgboost.readthedocs.io/) | XGBoost is a library for gradient boosting in Python. It features various tools for gradient boosting, including regression, classification and ranking. |
| [:material-leaf: LightGBM](https://lightgbm.readthedocs.io/) | LightGBM is a library for gradient boosting in Python. It features various tools for gradient boosting, including regression, classification and ranking. |
| [:material-paw: CatBoost](https://catboost.ai/) | CatBoost is a library for gradient boosting in Python. It features various tools for gradient boosting, including regression, classification and ranking. |

### :material-cube-outline: Machine Learning Frameworks

| :material-cube: Framework | :material-information-outline: Description |
|---|---|
| [:material-cube: TensorFlow](https://www.tensorflow.org/) | TensorFlow is a comprehensive open-source library for machine learning and deep learning, offering a wide range of tools and features for building and training models. |

### :material-brain: Deep Learning Frameworks

| :material-cube-outline: Framework | :material-information-outline: Description |
|---|---|
| [:material-fire: PyTorch](https://pytorch.org/) | PyTorch is a powerful, flexible deep learning framework that provides a seamless path from research prototyping to production deployment. |
| [:material-function: Keras](https://keras.io/) | Keras is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano. |

## Local development

```bash
source setup.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Regenerate the sidebar navigation after adding doc sections:

```bash
./scripts/update_mkdocs_nav.sh
```
