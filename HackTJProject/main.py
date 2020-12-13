import random, string
from flask import Flask, render_template, request
import pandas as pd
import data
import json

ID = '1knnSrX1pczjHgy28ru58JLxlPJQtmAzlztXxna6j1CE'
#ID = '1hJuPWMPbExSns9IwUquM7YqT4e3cBgQmk0nRUkLQ8MY'

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

#res = data.getData("English", ID)
#print("DATA: ")
#print(res)

student_data = data.getData("English", ID)
header = student_data[0]
body = student_data[1:]
student_df = pd.DataFrame(body, columns = header)
print("dataframe: ")
print(student_df)
student_json = json.loads(student_df.to_json(orient='records'))
print("json: ")
print(student_json)

ok_chars = string.ascii_letters + string.digits

@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'index.html'
	)

@app.route('/index.html')  # What happens when the user visits the site
def index_page():
	return render_template(
		'index.html'
	)

@app.route('/assignments.html')  # What happens when the user visits the site
def assignments_page():
  id = 1
  courses = 'English'
  rec = data.calcHourNew(courses)
  #print("recommended hours:")
  #print(rec)
  return render_template('assignments.html',rec = rec, course = courses, id = id)

@app.route('/students2.html')
def students_page():
  name = 'Allen'
  id = 1
  courses = 'English'
  #student_data = pd.DataFrame(data.getData("English", ID))
  student_df['Grade'] = student_df['Points'].astype('int') / student_df['Total'].astype('int')
  avg_grade = (student_df['Grade'].mean().round(decimals=3) *100)
  avg_hours = student_df['Hours of work'].astype('int').mean().round(decimals=3)
  avg_test = student_df["Tests"].astype('int').mean().round(decimals=3)
  egrades = []
  for i in student_df["Grade"]:
    egrades.append(i*100)
  #print(egrades)
  return render_template('students2.html', student_json = student_json, avg_grade = avg_grade, avg_hours = avg_hours, avg_test = avg_test,egrades = egrades)

# @app.route('/')  # What happens when the user visits the site
# def base_page():

# 	random_num = random.randint(1, 100000)  # Sets the random number
# 	return render_template(
# 		'base.html',  # Template file path, starting from the templates folder. 
# 		random_number=random_num  # Sets the variable random_number in the template
# 	)


# @app.route('/2')
# def page_2():
# 	rand_ammnt = random.randint(10, 100)
# 	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
# 	return render_template('site_2.html', random_str=random_str)


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0', 
		port=random.randint(2000, 9000) 
	)