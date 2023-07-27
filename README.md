# clrs

## *Jupyter notebooks for CLRS algorithms*

This project implements some of the interesting algorithms (mostly graphs) described in the textbook [*Introduction to Algorithms*](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) (4ed 2022) by Professors Cormen, Leiserson, Rivest, and Stein (CLRS 4ed). The Python programmes and the associated explanations are presented as [Jupyter](https://www.amazon.com/Introduction-Algorithms-fourth-Thomas-Cormen/dp/026204630X) notebook interactive documents. The intended audience is the first year Computer Science students taking algorithms, especially those using CLRS, one of the most popular algorithms textbooks.

You will need a copy of CLRS 4ed and you will need to be able to interact with the `.ipynb` IPython notebooks. The most convenient way to use these notebooks is with [JupyterLab Desktop](https://github.com/jupyterlab/jupyterlab-desktop) (JLD). Install JLD as per the instructions provided on that project's documentation.

Next, run JLD by double clicking on its `(lab)` application icon in the `~/Applications` folder. In the welcome window, click on the hamburger menu and select the **Settings** menu item. In the *Settings* dialogue, click on the **Server** tab on the left panel. In the *Server* panel, select the **Bundled Python environment** radio button and press the **Apply & restart** button. This will create a Python virtual environment folder during installation. As of mid 2023 when this project was created, JLD version 4.0.2 comes bundled with Python 3.8.17. On macOS, this virtual environment folder is `~/Library/jupyterlab-desktop/jlab_server/`. Quit JLD.

Now, type in the following shell commands in some folder, say `~/Documents/`, under which you wish to clone this project:

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
