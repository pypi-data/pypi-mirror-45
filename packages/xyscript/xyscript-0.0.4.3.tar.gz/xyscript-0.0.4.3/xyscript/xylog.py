
 # print("\033[1;31m failed \033[0m")
    # print("\033[1;32m success \033[0m")
def faillog(content):
    print("\033[1;31m" + str(content) + "\033[0m")

def successlog(content):
    print("\033[1;32m" + str(content) + "\033[0m")

def warninglog(content):
    print("\033[1;33m" + str(content) + "\033[0m")
