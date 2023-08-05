
def remove_comments(file):
    """returns comments from css file str"""
    q,i,x,n,clean = [],0,0,len(file),''
    while i < n-1:
        c = file[i]
        if c == '"' or c =="'":
            if len(q)==0:
                q.append(c)
            elif q[0] == c:
                q.pop()
        i = i+1
        if len(q)>0 or c != '/':
            continue
        if file[i] == '/':
            # remove line comment
            clean += file[x:i-1]
            try:
                x = file.index('\n',i+1)
                i = x+1
            except:
                x = n
                break
        elif file[i]=='*':
            # remove code block
            clean += file[x:i-1]
            try:
                x = file.index('*/',i+1)+2
                i = x
            except:
                # Error invalid js
                x = i-1
                break
            continue
    return clean+file[x:]