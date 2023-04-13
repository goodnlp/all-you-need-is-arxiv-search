# -*- coding: utf-8 -*-# 
# filename: handle.py
import hashlib
import reply
import receive
import web

import arxiv



class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            #print "Handle Post webdata is ", webData
            #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                #content = "test"
                content = recMsg.Content
                content = content.decode("UTF-8")
                print(content)

                # search arxiv via api
                search = arxiv.Search(query = content, max_results = 10,sort_by = arxiv.SortCriterion.SubmittedDate)
                temp = "为小主奉上今日最新有关%s10篇文章，加油科研！\n"%(content)
                rule = "-"*30 + "\n"
                for result in search.results():
                    text = rule+result.title+"\n"+result.pdf_url+"\n\n"
                    temp+= text
                #send result to user, in string format
                #print(type(temp))
                replyMsg = reply.TextMsg(toUser, fromUser, temp)
                return replyMsg.send()
            else:
                #print "暂且不处理"
                return "success"
        except Exception as e:
            return e
