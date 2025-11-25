from userinterface import UserInterface
from apihandler import APIHandler

def main():
    api = APIHandler()
    ui = UserInterface(api)

if __name__ == "__main__": main()