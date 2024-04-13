## Media Source Files

This project utilizes media resources (documentaries and Python programming lessons) to enrich the learning experience. Two methods are available for incorporating these resources:

**Method 1: Download from External Source (Optional)**

**Note:** Downloading from external sources might introduce security risks. Proceed with caution and only download from trusted sources.

1. If you prefer to download the media files from an external repository, click the following link (ensure you trust the source):

   [Link Download](https://drive.google.com/file/d/1g_OaCiRvcXWXhRyMpiXMHvI6EJLiDpYi/view?usp=sharing)

2. Extract the downloaded file (usually a compressed archive like ZIP or RAR) to create a folder named "media".

**Method 2: Local File Integration (Recommended)**

1. If you have the media files prepared locally, create a folder named "media" within your project workspace.

2. Place your media files (documentaries and Python lesson files) inside the "media" folder.

**Important:** Regardless of the chosen method, ensure the "media" folder is located within your project's root directory for the website to function correctly.


## Project Setup

1. **Development Environment:**

   * It's recommended to use a code editor or IDE like Visual Studio Code for development. You can download it from https://code.visualstudio.com/download.

2. **Project Dependencies:**

   * This project likely has dependencies on Python libraries. Refer to a separate `requirements.txt` file or project documentation for instructions on installing these dependencies. Common tools for dependency management include `pip` for Python. You can find installation instructions for `pip` at https://pip.pypa.io/en/stable/installation/.

3. **Running the Project:**

   * **Method 1: Using a Terminal (Command Line) (Optional):**

     Open a terminal or command prompt window and navigate to your project's root directory (where the `manage.py` file is located). Then, run the following command:

       ```bash
       python manage.py runserver
       ```

     This will start the development server, allowing you to access the website in your web browser (usually at `http://localhost:8000/`).

   * **Method 2: Using Visual Studio Code (Recommended):**

     - Open the project in Visual Studio Code.
     - In the "Run and Debug" tab, locate a configuration option that allows you to run the project (e.g., "Python: Current File" or a custom configuration).
     - Click the "Run" button (usually a green play button) to start the development server.

     This method provides a more user-friendly interface for running and debugging your project.
