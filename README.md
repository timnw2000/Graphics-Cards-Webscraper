# Webscraper for Graphics Cards
---
The Purpose of this Webscraper is too give you the cheapest graphics card available on `alternate.de`, `mindfactory.de` and `arlt.de`.
You can specify the desired graphics card and the script does the rest. Furthermore the script sends you an WhatsApp message with the results of the search including links to the cheapest graphics cards.

## Installation
---
Before you can start using this webscraper to get cheapest graphics card of your desired model. You need to `pip install` a few dependencies to your python environment. For this cause you can use the requirements.txt file, which includes every dependency.

    pip install -r requirements.txt

This should install everything you need for this script.


## Before Usage
---
When you want to use the WhatApp fuctionality make sure, that you create an Account on [GreenApi](https://green-api.com/en). 
It is important that you create an Instance, so you get an instance_id and an api_key.

Follow these steps:

1. Create an account on [GreenApi](https://green-api.com/en)

2. Create an Instance on your account

3. Authorize the Instance via QR-Code


## Usage
---
The script is pretty straight forward. I will prompt you for the model of the desired graphics card. The script proceeds to scrape data from `alternate.de`, `mindfactory.de` and `arlt.de` looking for the specified model. This can take up to a minute depending on your internet connection and you computer. When the script finished scraping the needed data, it will prompt you for your `instance_id`, your `api_key` and your `chat_id`. You can copy and paste your `instance_id` (IdInstance) and your `api_key` (ApiTokenInstance) from your GreenApi account. You'll find this information by clicken on your instance. Your `chat_id` however is basically a variation of your phone number. e.g. phone number: +49 111222333444; chat_id: 49111222333444. You can also find your `chat_id` like the othe information by clicking on your Instance.

The instance_id looks something like this:

    7823477410

The Api_key looks something like this:

    f6ff92a04c777ab131957df988a753341c4409ce37b3b123cae


The Chat_id looks smothing like this:

    491575568987654


## Examples
---
This short example shows how to use the script.

1 Type in graphics card model

    Which Graphics Card do you want: rtx 4080

2 Waiting for script to do it's thing (takes up to one minute)

3 Type in Instance_id from GreenApi

    Instance_id from GreenAPI: 7823477410

4 Type in Api_key from GreenApi

    Api_Key from GreenAPI: 6ff92a04c777ab131957df988a753341c4409ce37b3b123cae

5 Type in your chat_id

    Chat_id from GreenAPI (usually your phone number +49 111222333444 -> chat_id 49111222333444): 491575568987654


### License
---
This Script is licensed under the [MIT License](LICENSE)
