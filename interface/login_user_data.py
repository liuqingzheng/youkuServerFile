
alive_user={}


# addr[1]:{session:name}
def add_user(key,value):
    alive_user[key]=value

def remove_user(key):
    alive_user.pop(key)