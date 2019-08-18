# Posting comics to VK.COM
***
## Brief introduction
It is a training _Python_ project for better understanding  
of how to handle API services.  
It takes a picture from one place and sends to another via API  
The source site is [xkcd.com](https://xkcd.com/)  
The destination site for posting comics is [vk.com](https://vk.com) 


## Installing
Python 3.7 is used as an interpreter.  
`requirements.txt` contain all other libraries needed for setup  
It is easy to install by typing `pip install requirements.txt`  
Registration is required for the access to [vk.com](https://vk.com) API   
It is needed to have an account and a group for publishing  pictures  
[Dev page](https://vk.com/dev) contain the information for developers.  
You have to register a standalone application  
After the application has been registered you will get several key files  
It is needed to create `.env` file for retain key information:

* `VK_ACCESS_TOKEN = token`
* `VK_ID = clienr_id`
 

## Usage
The executable module is `vk_publisher.py`  
It takes args. 
  
* `img_name` - File name which is used for file operations
* `img_id` - Can be skipped and has random value
* `img_dir` are used for for file operations

Module can be executed within default arguments  
Without arguments app downloads random picture from source  
The picture will be saved in specified folder with specified name  
App posts the comic picture to the wall and deletes temporary folder 

just type `python vk_publisher.py`  
or with args `python vk_publisher.py --img_name comic `

It should output id of the posted message if everything is ok  

You can check the published comics on your personal wall  
 on [vk.com](https://vk.com)
 

## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/modules/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/psergal/bitly/blob/master/license.md) file for details  
