# I posted 5x a day on Instagram/Youtube for 45 days straight using this. 

I made a Reddit post explaining why I did this and how it helped me as a solopreneur who's struggling to stay consistent with content creation → (LINK TO BE ADDED)  

## Prerequisites  

This program relies on Heygen API. Unfortunately, I can't find a free alternatives to animate a picture.  

Sign up here → [Heygen, not affiliated](https://heygen.com/)  

Obtain the api key and put it in the .env file 

## .env  
Create a .env file and input the heygen api key:  

```
HEYGEN_API_KEY=''
```  

## Installation  
1. Activate virtual environment (I am running WSL2 on Windows 11, so I will use Linux commands)  
```
python3 -m venv venv
source venv/bin/activate
```

2. Clone this repo  
```
git clone 
```

3. Install requirements.txt
```
pip install -r requirements.txt
```  

4. You might need chromium
Pycaps might require chromium to be installed, but you can do this easily by following the instructions on [Pycaps Repo](https://github.com/francozanardi/pycaps)

## Assets
After installation, you will need to add the following assets. Create the folders with the exact name:

1. Create a 'brolls' folder. This is where you put your b-rolls
2. Create a 'media' folder. This will be needed by the program
3. Create an 'output' folder. This is where the finished clip goes

## Scritp
Heygen can read out a script that you give it. Please be aware, the script will be deleted after the video has been recreated. This is to prevent repeating the exact same script in different videos for mass production. 

The script is inside the 'swipe_files' folder in json format.