# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792

from Profile import Profile
from pathlib import Path
import a3
import ds_client as client

SERVERN = '168.235.86.101'
PORT = 3021


def profileCreate():
    uName = input('Please enter the user name: ')
    uPass = input('Please enter the password: ')
    bio = input('Please enter the bio: ')
    prof = Profile(SERVERN, uName, uPass)
    prof.bio = bio
    return prof

def userInteraction():
    done1 = True
    done2 = True
    decided  = False
    print('Welcome!')
    savePath = Path()
    newprof = None
    validity = False
    
    
    while not decided:
        choice = input('Would you like to save a profile '
                    'online or locally? (type \'o\' for online '
                    'and \'l\' to save locally)')
        choice.lower().strip()
        if choice == 'l':
            done1 = False
            done2 = False
            decided = True
        elif choice == 'o':
            onlineMode()

    while not done1:
        try:
            command = input('Do you want to create or '
                            'load a DSU file (type \'c\' to '
                            'create or \'o\' to load): \n').lower().strip()
            if command == 'q':
                done1 = True
                done2 = True
            if command == 'admin':
                a3.admin_mode()
                done1 = True
                done2 = True
                break
            elif command == 'o':
                path = input('Great! What is file path name that you '
                                'want to access?\n').replace('"', '').strip()
                path = Path(path)
                finished, path = a3.open_file(path)
                if not finished:
                    done1 = False
                else:
                    done1 = True
                    newprof = finished
                    savePath = path
            elif command == 'c':
                path = input('Great! Where would you like to place your '
                            'file?\n').replace('"', '').strip()
                name = input('What would you like to name your new file?\n')
                prof, path = a3.create_file(['c', path, '-n', name])
                if prof:
                    done1 = True
                    savePath = path
                    newprof = prof
                    break  
                else:
                    print('none for ')
                    done1 = False                
        except:
            print('Please enter a valid input')

    while not done2:
        try:
            command = input('What would you like to do with your file? '
                            '(Type \'e\' to edit, \'p\' to '
                            'print, and \'u\' to upload ' 
                            'online.)\n').lower().strip()
            if command == 'q':
                break
            elif command == 'e':
                print('Please enter what you would like to edit: '
                    '(Remember to put all entries between quotation marks)')
                print('u to change username')
                print('p to change password')
                print('b to change bio')
                print('a to add a post')
                print('d to delete a post')
                option = input().lower().strip()
                if option == 'u':
                    user = input('What would you like to change your '
                                'username to?\n')
                    a3.profile_editor(savePath, prof, ['-usr', user])
                if option == 'p':
                    passw = input('What would you like to change '
                                'your password to? \n')
                    a3.profile_editor(savePath, newprof, ['-pwd', passw])
                if option == 'b':
                    bio = input('What would you like to change your '
                                'bio to? \n')
                    a3.profile_editor(savePath, newprof, ['-bio', bio])
                if option == 'a':
                    post = input('What would you like your post to say \n')
                    a3.profile_editor(savePath, newprof, ['-addpost', post])
                if option == 'd':
                    dpost = input('What is the post number that you want '
                                'to delete? \n')
                    a3.profile_editor(savePath, newprof, ['-delpost', dpost])
            elif command == 'p':
                print('Please enter what you would like to print:')
                print('usr to print username')
                print('pwd to print password')
                print('bio to print bio')
                print('posts to print all posts')
                print('post to print a specific post')
                print('all to print everything stored in your profile')
                option = input().lower().strip()
                if option == 'usr':
                    a3.printer(newprof, ['p', '-usr', ''])
                elif option == 'pwd':
                    a3.printer(newprof, ['p', '-pwd', ''])
                elif option == 'bio':
                    a3.printer(newprof, ['p', '-bio', ''])
                elif option == 'posts':
                    a3.printer(newprof, ['p', '-posts', ''])
                elif option == 'post':
                    dpost = input('What is the number of the post that '
                                'you want to see? \n')
                    a3.printer(newprof, ['p', '-post', dpost])
                elif option == 'all':
                    a3.printer(newprof, ['p', '-all', ''])
                else:
                    print('Please enter a valid input')
            elif command == 'u':
                servername = input('Please enter the server name \n')
                servername = servername.strip(('\'"'))
                uname = newprof.username
                passw = newprof.password
                bio = newprof.bio
                post = newprof.get_posts()
                i = 0
                posts = ''
                while i < len(post):
                    posts = ''.join(post[i].entry)
                    validity = client.send(servername, PORT, uname, passw, str(posts), bio)
                    if validity:
                        print('Profile was successfully updated online.')
                    else:
                        print('Profile could not be uploaded properly. Please check your inputs.')
                    i += 1
            else:
                print('Please enter a valid input')
        except:
            print('Please enter a valid input')

    print('Thank your for using us!')


def onlineMode():
    print('Welcome to ONLINE mode!')
    servername = ''
    usrName = ''
    pwd = ''
    bio = ''
    quit = False
    post = ''
    validity = False
    while not quit:
        message = input('Please enter what you would like to do: \n'
                        'quit if you want to quit this program \n'
                        'join if you want to log in, or create a new account \n'
                        'post if you want to create a new post \n'
                        'bio if you want to update your bio \n'
                        )
        message = message.strip().lower()
        if message == 'quit':
            quit = True
            return
        elif message == 'join':
            servername = input('Please enter the server name \n')
            servername = servername.strip(('\'"'))
            usrName = input('Please enter your username \n')
            pwd = input('Please enter your password \n')
            post = input('Please enter what you want your post to say \n')
            bio = input('Please enter a bio for your profile (type \'p\' to skip this) \n')
            if bio.lower().strip() == 'p':
                bio = None
            validity = client.send(servername, PORT, usrName, pwd, post, bio)
            if validity:
                print('Profile was successfully updated online.')
            else:
                print('Profile could not be uploaded properly. Please check your inputs.')
        elif message == 'post':
            if not servername:
                print('please connect to the server first')
            else:
                bio = input('If you want to edit your bio, please type '
                            'it here (type \'p\' to skip this) \n')
                if bio.lower().strip() == 'p':
                    bio = None
                validity = client.send(servername, PORT, usrName, pwd, post, bio)
                if validity:
                        print('Profile was successfully updated online.')
                else:
                    print('Profile could not be uploaded properly. Please check your inputs.')
        elif message == 'bio':
            bio = input('Please enter a bio for your profile \n')
            #bio = None
            if not servername:
                print('please connect to the server first')
            else:
                validity = client.send(servername, PORT, usrName, pwd, post, bio)
                if validity:
                        print('Profile was successfully updated online.')
                else:
                    print('Profile could not be uploaded properly. Please check your inputs.')
        else:
            print('Please input a valid action')