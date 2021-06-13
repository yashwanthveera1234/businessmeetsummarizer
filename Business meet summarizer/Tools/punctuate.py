# import requests

# data = {
#   'text': 'hello world'
# }

# response = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)

# print(response.text)

def punctuateFunc(text):
    import requests
    data = {
        'text': text
    }
    response = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
    return response.text

if __name__ == "__main__":
    text = '''
    if you've never used linux before don't worry this course is designed for those who are brand new to linux we will be using a virtual machine to install linux so we won't be overwriting your computer's original operating system you should be comfortable installing software on your computer and you will also need to be sure that you have administrator access while we will be using windows in this course the software is also cross platform so if you have a mac you can also follow along we will be downloading some very large files so be sure you have a fast internet connection and at least ten to fifteen gigabytes of available storage on your hard drive
    '''
    print('text = ',text)
    print('punctuatated text = ', punctuateFunc(text))