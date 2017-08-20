import pynder
import itertools
import re
import spreadsheet
import datetime

FB_ID = "__PLACEHOLDER__"
FB_TOKEN = "__PLACEHOLDER__"
session = pynder.Session(facebook_id=FB_ID, facebook_token=FB_TOKEN)

MSG_FIRST = " Hey hübsches Bild :) Alles klar bei dir, was machst du gerade?"
MSG_SECOND = " War grad im Gym und jetzt noch bisschen chillen... was geht bei dir am we?"
MSG_ASK_FOR_NUMBER = " Hey pass auf ich bin hier nicht so oft on, lass mal Nummern tauschen dann " \
                     "schreib ich dir in Whatsapp ok? :)"
MSG_NO_NUMBER_RECEIVED = " Keine Sorge, ich ruf in der Regel nicht öfter als 12 Mal am Tag an :P Ich geh am Wochenende in Planet " \
                         "der Affen, hab gehört der soll ganz cool sein. Sonst noch nix vor"


def likeFiveUsers():
    users = session.nearby_users()
    for user in itertools.islice(users, 5):
        print(user.like())


def searchMsgsForNumber():
    matches = list(session.matches())
    for match in matches:
        messages = match.messages
        if messages:
            if messages[len(messages) - 1].body[0] != " ":
                for msg in messages:
                    if re.search("[0-9][0-9][0-9]", msg.body):
                        print("new number (", match.user.name, ", ", match.user.age, "): ", msg.body, sep="")
                        # TODO send notification (E-Mail, bulletpush)


def showNumbersAndNewMessages():
    searchMsgsForNumber()
    print("")

    # print name and last two messages. If she only send one text, only print that text.
    matches = list(session.matches())
    for match in matches:
        messages = match.messages
        if messages:
            if messages[len(messages) - 1].body[0] != " ":

                lastMsg = messages[len(messages) - 1].body
                if messages[len(messages) - 2].body[0] != " ":
                    penultimateMsg = messages[len(messages) - 2].body
                    print(match.user.name, "(", match.user.age, ")  ... ", penultimateMsg, "  +++  ", lastMsg, sep="")
                else:
                    print(match.user.name, "(", match.user.age, ")  ... ", lastMsg, sep="")


def answerAllMessages():
    matches = list(session.matches())
    print("Involved in", len(matches), "conversations.")
    for i in range(0, len(matches)):
        messages = matches[i].messages
        if messages:
            lastMsg = messages[len(messages) - 1].body[0]
            if lastMsg != " ":
                if getConversationLevel(messages) == 0:
                    print("Error: She wrote you first or bug. Check manually.")
                elif getConversationLevel(messages) == 1:
                    matches[i].message(MSG_SECOND)
                    print("Second message was sent to", matches[i].user.name)
                elif getConversationLevel(messages) == 2:
                    matches[i].message(MSG_ASK_FOR_NUMBER)
                    print("Third message was sent to", matches[i].user.name)
                elif getConversationLevel(messages) == 3:
                    if bool(re.search('[0 - 9][0 - 9][0 - 9]', lastMsg)):
                        return
                    matches[i].message(MSG_NO_NUMBER_RECEIVED)
                    print("Third message was sent to", matches[i].user.name)
                else:
                    print("This situation is not covered yet.")
        else:
            matches[i].message(MSG_FIRST)
            print("First message was sent to", matches[i].user.name)


def getConversationLevel(messages):
    # 0 = not opened, 1 = sent her one message, ...
    conversationLevel = 0;
    for i in range(0, len(messages)):
        if messages[i].body[0] == " ":
            conversationLevel += 1
    return conversationLevel


def insertAllMsgIntoSpreadsheet():
    matches = list(session.matches())
    for match in matches:
        messages = match.messages
        msgStrList = convertMessagesToString(messages)
        infoAboutMatch = [match.id, match.user.name, match.user.age]
        listToInsert = infoAboutMatch + msgStrList
        spreadsheet.insertMessage(listToInsert)
    print("All messages have been inserted.")


def convertMessagesToString(messages):
    strList = []
    for msg in messages:
        tmpMsg = [msg.body]
        strList = strList + tmpMsg
    return strList


insertAllMsgIntoSpreadsheet()