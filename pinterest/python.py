# import requests
# import bs4
 
# # url = input("https://www.pinterest.com/")
# url = input("Enter url")
# response = requests.get(url)
# # print(type(response));
# # print(response.text)
# filename= "index.html";
# bs = bs4.BeautifulSoup(response.text,"html.parser")
# formattext = bs.prettify();
# print(formattext)
# with open(filename,"w")as f:
#     f.write(formattext)
    
#     list_img = bs.find_all('img')
# print(list_img) 
# noof_img =len(list_img)

# print("num of img tag ",noof_img)

from flask import Flask, jsonify, send_file

app = Flask(__name__)

from py3pin.Pinterest import Pinterest

# Initialize Pinterest
pinterest = Pinterest(email='shivani07824@gmail.com',
                      password='ShivAni@7824001shivay',
                      username='shivani07824',
                      cred_root='cred_root')
pinterest.login()

# Fetch Pinterest images
@app.route('/get_pinterest_images')
def get_pinterest_images():
    desired_results =10
    results = []
    next_batch = pinterest.search(scope='boards', query='fashion')

    while next_batch and len(results) < desired_results:
        for board in next_batch:
            if len(results) >= desired_results:
                break

            title = board['name']
            cover_image_url = board['cover_pin']['image_url']

            results.append({'title': title, 'image_url': cover_image_url})

        if len(results) < desired_results:
            next_batch = pinterest.search(scope='boards', query='cloth')
        else:
            break

    return jsonify(results)

@app.route('/')
def index():
    return send_file('pinterest_gallery.html')

if __name__ == '__main__':
    app.run(debug=True)
    