# Ounass Marktech Developer Case study
Ounass wants to build a marketing platform for social media platforms. As a pilot
project, Facebook Marketing platform has been selected for the implementation. As a
developer, you are tasked to integrate with the Facebook Marketing platform.
Required Credentials:
```python
access_token =EAAGObqCO8AEBAKH53CrBZBQ4a9ZCudLR3mmGEyAC8583GxZCPLuFofzuNKagCS25hCZA3zWEo8rikGjRgCUaQb2xKPJuQGWdbOzTBMztrxBT3I3TWQD3XuHgJVi1uVjML5BNZBnbDasZCdZAnQ2T9WxfUAqEzLKLlWuuYlWVoZAN7RWeLK6ySrKRsakaG3PcBuAZD
ad_account_id = act_3061829570753376
app_secret = ff2002ad9af7137b75aafe9e828571e8
app_id = 438080767979521
page_id = 104413048775500
```

## Task 1: Backend
1. Create a campaign via API
   - The name will be **Conversions Campaign ***[your name here]*****
   - The objective will be ***REACH*** <br>
   ![Campaign Structure](https://scontent.fadb2-1.fna.fbcdn.net/v/t39.2178-6/851593_516881288424097_1568644600_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=5ca315&_nc_ohc=t9A3R8EpF9YAX8CY6oy&_nc_ht=scontent.fadb2-1.fna&oh=00_AT-wBXzwJtRkSlqLquryh6AjAOnm0zH9de_bmffPRE4Yeg&oe=61C9D505)
2. Create an Adset via API
   - The name will be **My First Adset ***[your name here]*****
   - The daily budget will be 2000 USD
   - The campaign will start the day the code is executed and run for 10 days
   - The bid amount will be 5 USD
   - Chose the suitable billing event
   - Chose the right optimization goal
   - The target audience will be story viewers who are between 20-35 years old and located in UAE, KSA, KUWAIT.
3. Create an ad via API.
   - The creative link message will be **try it out**
   - The creative link will be [Gucci](https://www.ounass.ae/designers/gucci)
   - The page id will be **104413048775500**
   - The creative name will be **Gucci AdCreative for Link Ad.**
   - The creative image will be <br> ![The San Juan Mountains are beautiful!](https://i.ibb.co/b38bYmw/gucci-bag.jpg)
4. Use Adset insight API to display the click and impressions results.
   - You may get empty result. Mock the api response from Facebook documentation
5. Use Preview API to display the ad that you created via API
   - If you want, you can use this package [Facebook-Business](https://pypi.org/project/facebook-business/) for API requests.
## Task 2: Frontend (Optional)
Build a UI (vue, react, angular) for the parameters that are entered above, such as
Adset name, daily budget, etc. and preview your ad on the frontend as mentioned in
Task 1.5

## Task3: Dockerize
Dockerize your code, and make sure the project will be up and running with an only
single command.
* Task 2 is optional but implementing task 2 will be a bonus point and positive impact on
the offer amount.