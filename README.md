# clrs

## *Jupyter notebooks for CLRS algorithms*

This project implements some of the interesting algorithms (mostly graphs) described in the textbook [*Introduction to Algorithms*](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) (4ed 2022) by Professors Cormen, Leiserson, Rivest, and Stein (CLRS 4ed). The Python programmes and the associated explanations are presented as [Jupyter](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) notebook interactive documents.

This is an ongoing project. It begins with the graph representation, the elementary graph algorithms, and two applications presented in Chapter 20 of CLRS. More implementations and commentaries will be added in due course.

The main purpose of this project is to be the practical companion to CLRS, which can be quite theoretical at places. It shows how to convert the English descriptions of algorithms given in the textbook into *code* and how to use the proven mathematical properties to implement *test* cases for the code. Jupyter is chosen for its excellent literate programming environment that produces documents with mathematical equations and runnable programmes. Python is chosen because it is one of the most comprehensible programming languages. It is fairly succinct, has a reasonably small syntactic constructs, and possesses relatively few quirks.

The primary audience of this project is the first year Computer Science students taking algorithms, especially those using CLRS, one of the most popular algorithms textbooks. The secondary audience is the IT practitioners interested in algorithm design and implementation.

# DEPENDENCIES

- [`util.ipynb`](./util.ipynb)—utility types and functions
  - [`graph.ipynb`](./graph.ipynb)—graph representation, BFS, and DFS from Chapter 20
    - [`graphtest.ipynb`](./graphtest.ipynb)—tests of BFS and DFS algorithms with visualisations

  - [`mst.ipynb`](./mst.ipynb)—Kruskal's and Prim's MST algorithms from Chapter 21
    - [`msttest.ipynb`](./msttest.ipynb)—tests of MST algorithms with visualisations


# INSTALLATION

You will need a copy of CLRS 4ed and you will want to be able to interact with the `.ipynb` IPython notebooks. If you merely wish to read the pre-rendered documents, just click on the `.ipynb` notebooks in this project [repository](https://github.com/amenzwa/clrs). GitHub will render the notebooks as static web pages.

The simplest way to use the notebooks is use [MyBinder.org](https://mybinder.org/v2/gh/amenzwa/clrs/HEAD); all you need do is to type in the link `https://mybinder.org/v2/gh/amenzwa/clrs/HEAD` in your browser and meditate, while the Binder cloud contemplates whether or not to run the notebooks. And if you are a software developer, you should use VSCode to write IPython notebooks.

But for most users, running [JupyterLab Desktop](https://github.com/jupyterlab/jupyterlab-desktop) (JLD) locally is the most sensible option. Install JLD as per the instructions given in that project's documentation. After installation, run JLD. In the welcome window, as shown in the screenshot below, click on the hamburger menu and select the **Settings** menu item. In the *Settings* dialogue, click on the **Server** tab on the left panel. In the *Server* panel, select the **Bundled Python environment** radio button and press the **Apply & restart** button. This will create a Python virtual environment folder during installation. As of mid 2023 when this project was created, JLD version 4.0.2 comes bundled with Python 3.8.17, whereas Python 3.11.4 is the stable release. On macOS, the bundled virtual environment folder is `~/Library/jupyterlab-desktop/jlab_server/`. Now, quit JLD.

![JupyterLab Desktop Settings dialogue](./images/JLDSettings.jpg)

Next, type in the following shell commands in some folder, say `~/Documents/`, under which you wish to clone this project:

```bash
$ ~/Documents
$ git clone https://github.com/amenzwa/clrs.git
```

Then, we install the required Python packages into JLD's virtual environment using as follows:

```bash
$ brew install graphviz # required by Python graphviz library
$ cd ~/Library/jupyterlab-desktop
$ source ./jlab_server/activate
(jlab_server) $ pip3 install -r ~/Documents/clrs/requirements.txt
```

Now, run JLD again and press the **Open...** button on the welcome window, and select the folder `~/Documents/clrs` where you placed this project. You may now interact with the `.ipynb` notebooks.

An IPython notebook is similar to a Python module. But a notebook differs from a module in a few important ways:

- An IPython notebook, by nature, contains both the Markdown text and the Python code.
- When you run JLD, it starts up a new session. If you open an existing notebook in this new session, the cells in the notebook are in their unevaluated states. If you now evaluate some cell lower in the notebook and this cell depends on some earlier cells, you will get "undefined" errors. So, it is advisable to perform **Run → Run All Cells** immediately after opening an existing notebook.
- Sometimes, a notebook cannot see updates made in other notebooks. It may then be necessary to perform **File → Reload Notebook from Disk**. If that did not resolve the issue, perform **Run → Restart Kernel and Run All Cells...**. And if nothing worked, quit JLD and start over again.

# CAUTION

Jupyter, Mathematica, and similar [literate programming](https://en.wikipedia.org/wiki/Literate_programming) environments are excellent for small, mathematical or technical projects that needs to combine textual description with sample code or data visualisation. Class projects, technical publications, internal-use scripts, and similar small projects are all candidates for Jupyter-based literate programming endeavour. Like all "documents", it is the author's responsibility to keep the entire document, not just the text or the code, up-to-date.

However, if the project is large, like a typical enterprise application, using Jupyter will lead only to surprise and sadness. This is because Jupyter, while an excellent platform for its intended purpose—composing live, technical documents—is not at all appropriate for developing substantive applications with intricate dependencies.

For example, even in the initial phase, this project is already fairly large, consisting of several reusable modules. The scope and size of this project will inevitably grow with time. Writing such substantial software in Jupyter is painful at best and, often, it is maddening. The solution is to develop the software in a proper IDE, like Emacs, VSCode, or IntelliJ IDEA, and then transfer the code snippets to Jupyter notebooks to be combined with the textual commentaries, while keeping a tight control over the use of global variables. This, obviously, is tedious and error-prone, but the effects justify the efforts.
