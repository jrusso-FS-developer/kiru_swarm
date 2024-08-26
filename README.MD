# Kiru Swarm
## A side-scrolling ninja, extermination game
### Install
> To run and install from terminal, download the entire git repo, and install "Swig" either for Windows, or for Mac.  
> 1. Extract the downloaded .zip file to wherever you like on your machine.  
> 2. Set the following Environment Variables 
> a. Open Environment Variables -> System Variables
> b. Click 'New'
> c. Variable Name = SWIG, and Variable Value = ***the folder you have the swig directory extracted to, Ie. "c:/Program Files"***
> d. Click, 'Ok' to apply and close the 'New System Variable' dialogue.
> e. Double click the 'Path' variable, and click 'New', to add a new node, with the folder that has the 'swig.exe' file.  This will be the root of the directory that was created on extract.  ***Ie. "C:\Program Files\swigwin-4.2.1\"***
>3. Install Python 3.9.0, but no higher, for compatibility purposes. 
> a. Add a path to your Python installed directory,  ***usually, "C:\Users\\{{username}}\AppData\Local\Programs\Python\Python39"***
> b. and to your Python 'Scripts' directory, ***usually, "C:\Users\\{{username}}\AppData\Local\Programs\Python\Python39\Scripts"***
> 4. Create a new Virtual Environment,  `python -m venv kiru_swarm_venv` ***you do not have to name it 'kiru_swarm_venv'.  Feel free to change this.
> 5. Activate your virtual env, `./kiru_swarm_venv/scripts/activate`
> 6. Now install all of the dependencies, `pip3 install -r requirements.txt`