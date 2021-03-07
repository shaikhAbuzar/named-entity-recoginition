# Named Entity Recognition
> The below provided code is divided in two parts:

> 1. The streamlit [app](https://streamlit-ner.herokuapp.com/)
> 2. The flask api

## The Streamlit App:
> ### Approach
1. The input from the user is taken using the streamlit's `text_input()` function which is the topic we need to search in the wikipedia api.
2. Check if the input provided is not a `None` or an **empty string**.
3. If the input is a proper string we use it to get the page using the `wikipediaapi.Wikipedia.page()` function which returns the page if it exists.
4. Check if the page exists, using the `wikipediaapi.Wikipedia.page.exists()` function, if it returns **True**, we extract the text from the page.
5. Process the obtained the using the `nlp` object that we created of the spacy module, and extract the sentences from it.
6. Get the sentence index from the user for the start as well as the end which are being displayed as the `streamlit.slider()` module.
7. Make sure the starting index is less than the ending index, and then display the graph of the label occurence of the selected sentences.
8. We use `streamlit.beta_expander()` module to display all the sentences in the specified format.

> Url for the streamlit app: https://streamlit-ner.herokuapp.com/

> ### Use the app:
1. Go to the ur given above
2. Select a topic you want to search
3. If the topic exists it will show you the graph, and a table with the count of each tag.
4. Use the slider to selecter the index of the sentences
5. The expander below shows the visual representation of the sentences with the tags in them.

> ### Note: The app might be slow to load due to the free tier of the heroku services.
---

## The Flask API:
> ### Approach:
The approach for the api can be summarised as folows:
1. You get the authentication token value first using a POST request.
2. Then you use the value of that post request to first authenticate your request for fetching the results.
3. The api is built on the flask web framework, and the token authentication is done using the Pyjwt library (Json Web Token).

> ### Using the API
1. To utilize the api, you can use **Postman** (a platform for testing apis) if you have postman installed you can use it, else got to this [link](https://www.postman.com/postman/workspace/postman-open-technologies-data/api/).
2. Go to the **APIs** section in the sidebar on the left and then click the **+** button to open up a new tab to test the API. It will give you a prompt to sign in / sign up just a create an account and you are good to go.
3. Then use the following url [https://ner-flaskapi.herokuapp.com/login] and change the method to **POST**, in the bottom section, click on the authorization tab, and in the authorization **Type** select the **Basic Auth** option and fill the **Username** field anything you wish, as for the **Password** field please use the **Password** as the value.
```python
    For Eg:
    Username: Abuzar
    Password: Password
```
4. Now in the body section of the app you will receice a `json` response, with the `token`. An example token:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWJ1emFyIiwiZXhwIjoxNjE1MDUzNjI4fQ.PU2x58R05pX3O-yIFcpTGAqFq3G_-a_THoE9y7UsFKY"
}
```
5. Copy the value of the token, we will using it for authenticate in the next step. Now open a new tab for the request and in the url section add the following url [https://ner-flaskapi.herokuapp.com/perform-ner], the method for this type is also **POST**, now in the **Params** section in the key add the **token** and in the value section add the value of the token that we received. And then add a new key **topic** and the value for the corresponding as the topic for which you want to search wikipedia, click on *Send*.
6. You will receive the output in the body section, among the bottom options click on the *Preview* button and then it will show you the visual format of the document.
### NOTE: If the steps are confusing to follow , feel free to watch the video file that is provided in the **Demo** folder.
---
> ### To run the application and/or API on your local system, do the following:
1. Download or clone the repo.
2. Create a virtual environment using the command `virtualenv venv`.
3. Activate the environment.
    1. For Windows: `venv\Scripts\activate`
    2. For Linux/Mac: `source venv/bin/activate`
4. Install all the requirements file using the *requirements.txt* provide with the repo, using the command `pip install -r requirements.txt`
5. To run the streamlit app, type the following command `streamlit run app.py`. It will provide you the local ip and the remote ip you can use either of them to view the application. All you need to do is copy either one of them and paste them into the url section of your browser.
6. To run the Flask API use the command `python flaskapp.py` to run the app, it will provide you the local ip of your machine, to test the API use the instructions same as above but replace the **https://ner-flaskapi.herokuapp.com** with **your-localhost-ip** wherever necessary.
```bash
Eg:
    https://ner-flaskapi.herokuapp.com/login will be replaced to http://localhost:5000/login
```
### You are up and ready to go.