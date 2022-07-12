
with open('ip_1.txt','r+') as f:

    txt = f.readline()
    while txt:
        txt = f.readline()
        if len(txt) != 0:
            txt = "{'HTTPS': '" + txt +"'}"
            txt = txt.replace("\n","")
            print(txt)

            # with open('ip_2.txt','w+') as e:
            #     e.write(txt)


f.close()