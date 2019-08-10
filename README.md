# Posting comics to VK.COM
***
## Brief introduction
THis is a training project for better understanding how handling with API services.
Site which donates comics is [xkcd.com](https://xkcd.com/)  
Site for posting comics is [vk.com](https://vk.com) 


## Installing
Requirements.txt contain all libraries that are needed for executing  
Registration is required for the access to [vk.com](https://vk.com) API   
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
* `api` and `headers` are used for configuration

Module can be executed within default arguments 

just type `python vk_publisher.py`  
or with args `python vk_publisher.py --img_name comic `

It should output id of the posted message.  

You can check the published comics on your personal wall  
 on [vk.com](https://vk.com)
 


## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/modules/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/psergal/bitly/blob/master/license.md) file for details  
