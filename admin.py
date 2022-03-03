from flask import *
from database import *
import matplotlib.pyplot as plt

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')


@admin.route('/admin_manage_subject',methods=['get','post'])	
def admin_manage_subject():
	data={}
	if 'manage' in request.form:
		subject_name=request.form['s_name']
		q="insert into subject value(NULL,'%s')"%(subject_name)
		insert(q)
	q="select * from subject"
	res=select(q)
	data['subject']=res
		#return redirect(url_for('admin.admin_manage_subject'))
	return render_template("admin_manage_subject.html",data=data)


@admin.route('/admin_manage_student',methods=['get','post'])	
def admin_manage_student():
	data={}

	q="select * from student_reg"
	res=select(q)
	data['student_reg']=res
	print(res)

	if 'register' in request.form:
		firstname=request.form['fname']
		lastname=request.form['lname']
		phoneno=request.form['pno']
		gender=request.form['Gender']
		email=request.form['email']
		course=request.form['Course']
		semester=request.form['sem']
		housename=request.form['hname']
		place=request.form['place']
		pincode=request.form['pin']
		username=request.form['uname']
		password=request.form['pwd']
		q="insert into login values(null,'%s','%s','student')"%(username,password)
		id=insert(q)
		q="insert into student_reg values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,firstname,lastname,phoneno,gender,email,course,semester,housename,place,pincode)
		insert(q)
		return redirect(url_for('admin.admin_manage_student'))

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from student_reg where login_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_student'))

	if action=="update":
		q="select * from student_reg where login_id='%s'"%(id)
		res=select(q)
		data['stud']=res

	if 'update' in request.form:
		firstname=request.form['fname']
		lastname=request.form['lname']
		phone=request.form['pno']
		email=request.form['email']
		gender=request.form['gender']
		course=request.form['course'] 
		semester=request.form['sem']
		housename=request.form['hname']
		place=request.form['place']
		pin=request.form['pin']
		q="update student_reg set first_name='%s',last_name='%s',phone='%s',gender='%s',email='%s',course='%s',semester='%s',house_name='%s',place='%s',pincode='%s' where login_id='%s'"%(firstname,lastname,phone,gender,email,course,semester,housename,place,pin,id)
		update(q)			
		return redirect(url_for('admin.admin_manage_student'))
	return render_template("admin_manage_student.html",data=data)


@admin.route('/admin_manage_teacher',methods=['get','post'])	
def admin_manage_teacher():
	data={}
	q="select * from subject"
	res=select(q)
	data['subject']=res

	q="select * from teacher inner join subject using(subject_id)"
	res=select(q)
	data['teacher']=res

	if 'register' in request.form:
		subjectname=request.form['subject']
		firstname=request.form['fname']
		lastname=request.form['lname']
		phone=request.form['pno']
		email=request.form['email']
		username=request.form['uname']
		password=request.form['pwd']
		q="insert into login values(NULL,'%s','%s','teacher')"%(username,password)
		ids=insert(q)
		q="insert into teacher values(null,'%s','%s','%s','%s','%s','%s')"%(ids,firstname,lastname,phone,email,subjectname)
		insert(q)
		return redirect(url_for('admin.admin_manage_teacher'))
	if 'action' in request.args:
		action=request.args['action']
		ids=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from teacher where login_id='%s'"%(ids)
		delete(q)
		return redirect(url_for('admin.admin_manage_teacher'))

	if action=="update":
		q="select * from teacher where login_id='%s'"%(ids)
		res=select(q)	
		data['teach']=res
	if 'update' in request.form:
		ids=request.args['id']
		firstname=request.form['fname']
		lastname=request.form['lname']
		phone=request.form['pno']
		email=request.form['email']
		q="update teacher set first_name='%s',last_name='%s',phone='%s',email='%s' where login_id='%s'"%(firstname,lastname,phone,email,ids)
		update(q)			
		return redirect(url_for('admin.admin_manage_teacher'))

	return render_template("admin_manage_teacher.html",data=data)


@admin.route('/admin_manage_exam',methods=['get','post'])	
def admin_manage_exam():
	data={}

	q="select * from subject"
	res=select(q)
	data['sub']=res

	q="select * from exam inner join subject using(subject_id)"
	res=select(q)
	data['exam']=res
	print(res)

	if 'ADD' in request.form:
		subid=request.form['subid']
		datetime=request.form['datetime']
		notification_details=request.form['notification_details']
		q="insert into exam values(null,'%s','%s','pending')"%(subid,datetime)
		id=insert(q)
		print(q)
		q="insert into notification_students values(null,'%s','%s')"%(id,notification_details)
		insert(q)
		print(q)
		return redirect(url_for('admin.admin_manage_exam'))

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from exam where exam_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_exam'))
	if action=="start":
		q="update exam set status='Start' where exam_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_exam'))
	if action=="stop":
		q="update exam set status='Stop' where exam_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_exam'))
	if action=="plot":
		q="select *,concat(first_name,' ',last_name) as name from result inner join student_reg using(student_id) where exam_id='%s'" %(id)
		res=select(q)
		print(q)
		x=[]
		y=[]
		for row in res:
			x.append(row['name'])
			y.append(row['total_marks'])
		# x axis values
		# x = ("1","2","3")
		# corresponding y axis values
		# y = [2,4,1]
		 
		# plotting the points
		plt.plot(x, y)
		 
		# naming the x axis
		plt.xlabel('x - axis')
		# naming the y axis
		plt.ylabel('y - axis')
		 
		# giving a title to my graph
		plt.title('My first graph!')
		 
		# function to show the plot
		plt.show()

	if action=="update":
		q="select * from exam where exam_id='%s'"%(id)
		res=select(q)
		data['updater']=res

	if 'update' in request.form:
		datetime=request.form['datetime']
		
		q="update exam set datetime='%s' where exam_id='%s'"%(datetime,id)
		update(q)			

		return redirect(url_for('admin.admin_manage_exam'))

	return render_template("admin_manage_exam.html",data=data)



@admin.route('/admin_view_exam_added_teachers')
def admin_view_exam_added_teachers():
	data={} 
	id=request.args['id']
	data['exam_id']=id
	q="select * from teacher  where staff_id IN(select distinct(staff_id) FROM `questions` WHERE exam_id='%s')"%(id)
	res=select(q)
	data['teacher']=res
	print(res)
	
	return render_template('admin_view_exam_added_teachers.html',data=data)

@admin.route('/admin_view_questions')
def admin_view_questions():
	data={} 
	sid=request.args['sid']
	examid=request.args['examid']
	q="select * from questions where staff_id='%s' and exam_id='%s'"%(sid,examid)
	res=select(q)
	data['questions']=res
	print(res)
	
	
	return render_template('admin_view_questions.html',data=data)








