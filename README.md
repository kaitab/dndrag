# dndrag

This repo contains the source code for our COSI 217 Final Project. We built a system that uses a modified langchain sytem for Retrieval Augmented Generation (RAG) that accesses the [5e srd api](https://5e-bits.github.io/docs/) to give highly accurate, quick answers to questions about the dense rules of 5th edition Dungeons and Dragons.

The write-up for this project is available [here](https://docs.google.com/document/d/1yjx_pmMzjqeuZ7DQKZvf2xI7dy_k_q-Pjh43KIv4e-U/edit?usp=sharing) 

<h2>Build/Run</h2>
Since we use Google Gemini as the main react agent through LangChain, the app requires a Gemini API key, either as an environment variable named `GOOGLE_API_KEY` or entered through the console upon running the app.

The code can be run py installing the python package from the project root directory (`pip install .`) and then running `run.py` This is the recommended way, since it is easier to enter your own API token from the console, but it can also be built/run as a docker image

To build the image, run: 

`docker build -t dnd_rag .`

For my version of Docker, this creates the image at `docker.io/library/note_app:latest`, but note the console output in case it adds a different prefix to the name.

To run the container after building the image, use this command:

`docker run -p 5000:5000 -v ./instance:/dnd_rag/instance docker.io/library/note_app:latest`

The flag `-p` matches the port in the Docker image to the port used by system localhost.

The flag `-v` is used to bind the `instance` subdirectories where the SQL database is stored.

After running this command, the website will be running at [127.0.0.1:5000](http://127.0.0.1:5000/) and the database will be saved in your local assignment3/instance folder.

<h4>OS Compatibility Note</h4




A note for native Linux/macOS users: I had to use a workaround for setting the ports while programming with Windows Subsystem for Linux. I don't think with will affect how this runs on native Linux systems, but I've left the debug=True flag on in my Flask app so you can see what port it is running at in case [127.0.0.1:5000](http://127.0.0.1:5000/) doesn't work.
