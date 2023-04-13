# -*- coding: utf-8 -*-# 
# filename: handle.py
import hashlib
import reply
import receive
#import web

from flask import Flask,render_template,url_for,request
import arxiv

app=Flask(__name__)


@app.route('/wx', methods=['POST'])
def wx():
    data=request.data.decode('utf-8')
    #print(data)
    recMsg = receive.parse_xml(data)
    if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        #content = "test"
        content = recMsg.Content
        content=content.decode('UTF-8')# per use, need decode againi
        print(content,toUser, fromUser)
        # search arxiv via api
        search = arxiv.Search(query = content, max_results = 10,sort_by = arxiv.SortCriterion.SubmittedDate)
        nums=len([i for i in search.results()])

        temp = "为小主奉上今日最新有关[%s]%d篇文章，加油科研！\n"%(content,nums)
        rule = "-"*30 + "\n"
        for k,result in enumerate(search.results()):
            text = rule+"[%d] "%(k+1)+result.title+"\n\nSubmitted Time: "+ str(result.published).split(" ")[0] +"\n"+result.pdf_url+"\n\n"
            temp+= text
            #temp+=rule
            #temp+="更多功能正在研发中"
        #send result to user, in string format
        #print(type(temp))
        replyMsg = reply.TextMsg(toUser, fromUser, temp)
        return replyMsg.send()
    else:
        #print "暂且不处理"
        return "success"




if __name__ == '__main__':
    app.run(debug=True)
