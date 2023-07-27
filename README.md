# clrs

## *Jupyter notebooks for CLRS algorithms*

This project implements some of the interesting algorithms (mostly graphs) described in the textbook [*Introduction to Algorithms*](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) (4ed 2022) by Professors Cormen, Leiserson, Rivest, and Stein (CLRS 4ed). The Python programmes and the associated explanations are presented as [Jupyter](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) notebook interactive documents.

This is an ongoing project. It begins with the graph representation, the elementary graph algorithms, and two applications presented in Chapter 20 of CLRS. More implementations and commentaries will be added in due course.

The main purpose of this project is to be the practical companion to CLRS, which can be quite theoretical at places. It shows how to convert the English descriptions of algorithms given in the textbook into *code* and how to use the proven mathematical properties to implement *test* cases for the code. Jupyter is chosen for its excellent literate programming environment that produces documents with mathematical equations and runnable programmes. Python is chosen because it is one of the most comprehensible programming languages. It is fairly succinct, has a reasonably small syntactic constructs, and possesses relatively few quirks.

The primary audience of this project is the first year Computer Science students taking algorithms, especially those using CLRS, one of the most popular algorithms textbooks. The secondary audience is the IT practitioners interested in algorithm design and implementation.

## *installation*

You will need a copy of CLRS 4ed and you will want to be able to interact with the `.ipynb` IPython notebooks. If you merely wish to read the pre-rendered documents, just click on the `.ipynb` notebooks in this project [repository](https://github.com/amenzwa/clrs). GitHub will render the notebooks as static web pages.

The most convenient way to use the notebooks is with [JupyterLab Desktop](https://github.com/jupyterlab/jupyterlab-desktop) (JLD). Install JLD as per the instructions given in that project's documentation. After installation, run JLD. In the welcome window, as shown in the screenshot below, click on the hamburger menu and select the **Settings** menu item. In the *Settings* dialogue, click on the **Server** tab on the left panel. In the *Server* panel, select the **Bundled Python environment** radio button and press the **Apply & restart** button. This will create a Python virtual environment folder during installation. As of mid 2023 when this project was created, JLD version 4.0.2 comes bundled with Python 3.8.17, whereas Python 3.11.4 is the stable release. On macOS, the bundled virtual environment folder is `~/Library/jupyterlab-desktop/jlab_server/`. Now, quit JLD.

![JupyterLab Desktop Settings dialogue](./images/JLDSettings.jpg)

Next, type in the following shell commands in some folder, say `~/Documents/`, under which you wish to clone this project:

```bash
$ ~/Documents
$ git clone https://github.com/amenzwa/clrs.git
```

Then, we install the required Python packages into JLD's virtual environment using as follows:

```bash
$ cd ~/Library/jupyterlab-desktop
$ source ./jlab_server/activate
(jlab_server) $ pip3 install -r ~/Documents/clrs/requirements.txt
```

Now, run JLD again and press the **Open...** button on the welcome window, and select the folder `~/Documents/clrs` where you placed this project. You may now interact with the `.ipynb` notebooks.
