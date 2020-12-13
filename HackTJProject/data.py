from googleapiclient.discovery import build
from google.oauth2 import service_account
import math

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def createDemoClass():
  addClass("testClass, dw")
  addStudent("Kevin", 1561441, classes)
  addStudent("Michael", 265414, classes)
  addStudent("Allen", 1351415, classes)
  addStudent("Arnav", 1443234, classes)
  addStudent("Evan", 1542842, classes)
  addStudent("Myles", 1652133, classes)
ID = '1knnSrX1pczjHgy28ru58JLxlPJQtmAzlztXxna6j1CE'
#ID = '1hJuPWMPbExSns9IwUquM7YqT4e3cBgQmk0nRUkLQ8MY'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def getData(course, id):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A1:F100").execute()
  s = s.get('values', [])
  print("this is s: ")
  print(s)
  return s

def addClass(name):
  request_body = {"requests" : [{'addSheet': {'properties': {'title': name}}}]}
  sheet.batchUpdate(spreadsheetId=ID, body=request_body).execute();
  service.spreadsheets().values().update(spreadsheetId=ID, range=(name + "!A1"), valueInputOption="USER_ENTERED", body={"values":[[name, "Name", "Points", "Total", "Hours of work", "Tests"]]}).execute()

def classAddStudent(course, name, id):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A1:F100").execute()
  size = len(s.get('values', []))
  service.spreadsheets().values().update(spreadsheetId=ID, range=course+"!A" + str(size+1), valueInputOption="USER_ENTERED", body = {"values":[[id, name, 0, 0, 0, 0]]}).execute()

def addStudent(name, id, courses):
  for course in courses:
    classAddStudent(course, name, id)
  add = [id, name]
  add.extend(courses)
  add.append(0)
  add.append(0)
  print(add)
  service.spreadsheets().values().update(spreadsheetId=ID, range="Students!A" + str(id+1), valueInputOption="USER_ENTERED", body={"values":[add]}).execute()

def updateGrade(course, id, points, outof):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A2:F100").execute()
  s = s.get('values', [])
  pos = 1;
  for a in s:
    pos += 1
    if int(a[0]) == int(id):
      a[2] = int(a[2]) + points
      a[3] = int(a[3]) + outof
      service.spreadsheets().values().update(spreadsheetId=ID, range=course+"!A" + str(pos), valueInputOption="USER_ENTERED", body={"values":[a]}).execute()

def getGrade(course, id):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A2:F100").execute()
  s = s.get('values', [])
  pos = 1;
  for a in s:
    pos += 1
    if int(a[0]) == int(id):
      if int(a[3]) == 0:
        return -1
      return math.trunc(10000 * (int(a[2])/int(a[3])))/100

def editHour(course, id, hour):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A2:F100").execute()
  s = s.get('values', [])
  pos = 1;
  for a in s:
    pos += 1
    if int(a[0]) == int(id):
      a[4] = int(a[4]) + hour
      service.spreadsheets().values().update(spreadsheetId=ID, range=course+"!A" + str(pos), valueInputOption="USER_ENTERED", body={"values":[a]}).execute()
  t = sheet.values().get(spreadsheetId=ID, range= "Students!A" + str(id+1) + ":K" + str(id+1)).execute()
  t = t.get('values', [])
  t[0][9] = int(t[0][9]) + hour
  service.spreadsheets().values().update(spreadsheetId=ID, range="Students!A" + str(id+1), valueInputOption="USER_ENTERED", body={"values":t}).execute()

def editTest(course, id, test):
  s = sheet.values().get(spreadsheetId=ID, range= course + "!A2:F100").execute()
  s = s.get('values', [])
  pos = 1;
  for a in s:
    pos += 1
    if int(a[0]) == int(id):
      a[5] = int(a[5]) + test
      service.spreadsheets().values().update(spreadsheetId=ID, range=course+"!A" + str(pos), valueInputOption="USER_ENTERED", body={"values":[a]}).execute()
  t = sheet.values().get(spreadsheetId=ID, range= "Students!A" + str(id+1) + ":K" + str(id+1)).execute()
  t = t.get('values', [])
  t[0][10] = int(t[0][10]) + test
  service.spreadsheets().values().update(spreadsheetId=ID, range="Students!A" + str(id+1), valueInputOption="USER_ENTERED", body={"values":t}).execute()

def calcHourNew(course):
  s = sheet.values().get(spreadsheetId=ID, range= "Students!A2:K100").execute()
  s = s.get('values', [])
  t = sheet.values().get(spreadsheetId=ID, range= course+"!A2:F100").execute()
  t = t.get('values', [])
  ctot = 0;
  ccnt = 0;
  for a in t:
    ctot += int(a[4])
    ccnt += 1
  tot = 0
  cnt = 0
  for a in s:
    print(a)
    tot += int(a[9])
    cnt += 1
  return max(0, min(2, 8-tot*2//cnt/2) - (2 * ctot//cnt/2) )

def calcTestNew(course):
  s = sheet.values().get(spreadsheetId=ID, range= "Students!A2:K100").execute()
  s = s.get('values', [])
  t = sheet.values().get(spreadsheetId=ID, range= course+"!A2:F100").execute()
  t = t.get('values', [])
  ctot = 0;
  ccnt = 0;
  for a in t:
    ctot += int(a[5])
    ccnt += 1
  tot = 0
  cnt = 0
  for a in s:
    print(a)
    tot += int(a[9])
    cnt += 1
  return max(0, min(1, 2-tot//cnt) - (ctot//ccnt))



#print(calcAvg("English"))
classes = ["Math", "Science", "PE", "History", "English", "Language", "Comp Sci"]

'''
for course in classes:
  addClass(course)
addStudent("Kevin", 1, classes)
addStudent("Michael", 2, classes)
addStudent("Allen", 3, classes)
addStudent("Arnav", 4, classes)
addStudent("Evan", 5, classes)
addStudent("Myles", 6, classes)

#classAdd("English", "Myles Bao", 6)
'''
'''
updateGrade("English", 2, 1, 2)
editHour("English", 1, 5)
editTest("English", 1, 1)

for i in range(1, 7):
  editHour("English", i, i)
'''
'''
editHour("English", 1, 2)
print(calcHourNew("English"))
print(calcTestNew("English"))
'''
#print(getGrade("English", 2))