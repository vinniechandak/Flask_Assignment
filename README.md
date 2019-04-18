# Environment Setup

1. Clone the repository
2. Import it in PyCharm
3. Download the plugins if required.
4. Run Request.py
5. Run Response.py
6. Hit http://localhost:4049/request on browser.
7. Download the CSV from available link.

# Approach

I created a Request.py which reads data.json file and makes a request to another port(we can replace it by another server). The request is created by port 4049.

The Response.py works as another server which is running on port 4050 and accepts json from the request. 

I have kept different method for each business rule so that they can be modified individually at the later point in time if required.
I understand that this will cause multiple iteration on the data but flexibility was my prime goal. All the rules can be achieved in a single iteration and this can be improved.

I have used dictionary, lists and generators for this task.
