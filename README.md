# cs302 Fantasy Stocks
Final project for cs302 where we are starting making a project that is fantasy football acting like stocks

## Setup
**We are using Jupyter notebook, we use vscode for this, but you do not have to. I will not provide other instructions, because I never use Jupyter without vscode. **  
  
Create the virtual environment  
```python3 -m venv .venv```  
activate virtual environment  
```source .venv/bin/activate```  
Install Libraraies  
```pip install -r requirements.txt```  

## Running API
We have an api that the index.html expects to be hosted locally with the port 5555. If you need to host on remote server, you can forward traffic by doing.   
`ssh -L 5555:localhost:5555 username@server_address`   
Then while the virtual environment is active, run `python3 api.py` It will look frozen up, but it is doing initialization, you will see an message ending with `(Press CTRL+C to quit)` when it is ready for you to use.  
Just double click the index.html and you will be able to use the page as intended.

