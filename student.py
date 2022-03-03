from flask import *
from database import *
import numpy

student=Blueprint('student',__name__)

@student.route('/studenthome')
def studenthome():
	return render_template('studenthome.html')

@student.route('/student_view_exam')
def student_view_exam():
	data={}
	q="SELECT * FROM exam INNER JOIN SUBJECT USING(subject_id) WHERE `datetime`=CURDATE()"
	res=select(q)
	data['exam']=res
	print(res)

	return render_template('student_view_exam.html',data=data)

@student.route('/student_mark_attendance',methods=['get','post'])
def student_mark_attendance():
	data={}
	q="select * from attendance where student_id='%s' and date=curdate()" %(session['sid'])
	res=select(q)
	if res:
		 flash("Already Marked Attendnace")
	else:
		q="insert into attendance values(NULL,'%s',curdate())"%(session['sid'])
		insert(q)
		flash("Attendnace Marked Successfully")
		return redirect(url_for('student.student_mark_attendance'))

	q="select * from attendance where student_id='%s'" %(session['sid'])
	res1=select(q)
	data['attendance']=res

	return render_template('student_mark_attendance.html',data=data)

@student.route('/startexam',methods=['get','post'])
def startexam():
	data={}
	data['flag']=0
	data['pflag']=0
	data['qstnid']=1

	eid=request.args['eid']
	id=session['lid']
	q="select * from exam where exam_id='%s'" %(eid)
	res1=select(q)
	data['examname']=res1
	q="select *,concat(First_name,' ',last_name) as names from student_reg where login_id='%s'" %(id)
	res3=select(q)
	data['sdetails']=res3
	data['check']=[{'button':"None"}]
	if 'startexam' in request.form:
		q="SELECT * FROM `participation` WHERE `student_id`=(select student_id from student_reg where login_id='%s') AND `exam_id`='%s'"%(id,eid)
		
		print(q)
		res=select(q)
		print(res)
		if res:
			flash("exam is Already attend")
			return redirect(url_for('student.student_view_exam'))
		# select questions
		q="select question_id from questions where exam_id='%s'" %(res1[0]['exam_id'])
		res2=select(q)
		# shuffle the questions
		a = [d.get('question_id', None) for d in res2]
		numpy.random.shuffle(a)
		
		print(len(a))
		data['numofval']=len(a)
		data['numofvalinc']="1"
		data['position']="0"

		# get question details
		q="select * from questions where question_id='%s'" %(a[0])
		print(q)
		res=select(q)
		data['questions']=res
		# get answer details 
		q="select option_id,`option` from options where question_id='%s'" %(a[0])
		res=select(q)
		data['answerdetails']=res

		# check whether answered
		q="select * from answers where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(a[0],id)
		print(q)
		res5=select(q)
		if res5:
			data['answered']=res5
		else:
			data['answered']=[{"option_id":""}]
		print("Haii",data['answered'])

		str1 = ""  

	# traverse in the string   
		for ele in a:
			if str1=="":
				str1=str(ele)
			else:
				str1 = str1+","+str(ele)
		print("aaaaa"+str1)
		data['a']=str1

		# for button check
		data['check']=[{'button':"Clikked"}]
		data['nextcheck']=[{'button':"NotFinished"}]
		data['previouscheck']=[{'button':"First"}]

	# Next Button
	if 'next' in request.form:

		#for check of question number
		numofval=request.form['numofval']
		data['numofval']=numofval
		qstnid=request.form['qstnid']
		
		# check 
		if numofval==qstnid:
			data['qstnid']="1"
		else:
			data['qstnid']=int(qstnid)+1
		# get dict value in a
		a=request.form['dict']
		a = list(a.split(","))
		print(a)
		# get position of dict
		position=request.form['dictposition']
		# get flag check
		flag=request.form['flag']
		# get question id
		qid=request.form['qid']

		if 'selanswer' in request.form:
			selanswer=request.form['selanswer']

			#insert
			q="select * from answers where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(qid,id)
			res=select(q)
			print(res)
			if res:
				q="SELECT * FROM `options` WHERE question_id='%s' AND `option_id`='%s' " %(qid,selanswer)
				resids=select(q)
				print("kkkk")
				if resids:
					print("sdf"+resids[0]['status'])
					if resids[0]['status']=="Yes":
						q="update answers set option_id='%s' and mark_awarded='1' where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(selanswer,qid,id)
						update(q)
					else:
						q="update answers set option_id='%s' and mark_awarded='0' where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(selanswer,qid,id)
						update(q)
			else:
				q="SELECT * FROM `options` WHERE question_id='%s' AND `option_id`='%s' " %(qid,selanswer)
				resids=select(q)
				print(q)
				print(resids)
				if resids:
					print("hh"+resids[0]['status'])
					if resids[0]['status']=="Yes":
						q="insert into answers values(null,'%s',(select student_id from student_reg where login_id='%s'),'%s','1')" %(qid,id,selanswer)
						insert(q)
					else:
						q="insert into answers values(null,'%s',(select student_id from student_reg where login_id='%s'),'%s','0')" %(qid,id,selanswer)
						insert(q)

		# increment position
		position=int(position)+1
		# check flag
		if flag=="1":
			position=0
			data['pflag']=0
		else:
			data['pflag']=1
		# print("fgh"+str(a[int(position)]))
		data['position']=position
		print("dfg"+str(len(a)))	
		if position==len(a):
			q="insert into participation values(null,'%s',(select student_id from student_reg where login_id='%s'))" %(id,eid)
			insert(q)
			q="insert into result values(null,(select student_id from student_reg where login_id='%s'),SELECT SUM(`mark_awarded`) FROM answers INNER JOIN questions USING (question_id) WHERE student_id=(select student_id from student_reg where login_id='%s') AND exam_id='%s'),'%s')" %(id,id,eid,eid)
			flash('Exam Finished')
			return redirect(url_for('student.student_view_exam'))
		# check whether answered
		q="select * from answers where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(a[int(position)],id)
		print(q)
		res5=select(q)
		if res5:
			data['answered']=res5
		else:
			data['answered']=[{"option_id":""}]
		print("Haiissssssss",a[int(position)])
		# get question details
		q="select * from questions where question_id='%s'" %(a[int(position)])
		print(q)
		res=select(q)
		data['questions']=res
		print(res)
		# get answer details 
		q="select option_id,`option` from options where question_id='%s'" %(a[int(position)])
		res=select(q)
		data['answerdetails']=res
		# for next button check

		data['check']=[{'button':"Clikked"}]
		if int(position)==len(a)-1:
			data['flag']=1
		# for previous button check
		data['previouscheck']=[{'button':"NotFirst"}]
		str1=""
		for ele in a:
			if str1=="":
				str1=str(ele)
			else:
				str1 = str1+","+str(ele)
		print("aaaaa"+str1)
		data['a']=str1

	# Previous 

	if 'previous' in request.form:
		#for check of question number
		numofval=request.form['numofval']
		data['numofval']=numofval
		qstnid=request.form['qstnid']
		# check 
		if int(qstnid)==1:
			data['qstnid']=numofval
		else:
			data['qstnid']=int(qstnid)-1
		# get dict value in a
		a=request.form['dict']
		a = list(a.split(","))
		print(a)
		# get position of dict
		position=request.form['dictposition']
		# get flag check
		flag=request.form['flag']
		pflag=request.form['pflag']
		# get question id
		qid=request.form['qid']
		# q="select * from answers where question_id='%s' and student_id='%s'" %(qstnid,id)
		# res5=select(q)
		# data['answerdetail']=res5
		
		if 'selanswer' in request.form:
			selanswer=request.form['selanswer']
			#insert
			q="select * from answers where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(qid,id)
			res=select(q)
			if res:
				q="SELECT * FROM `options` WHERE question_id='%s' AND `option_id`='%s' " %(qid,selanswer)
				resids=select(q)
				if resids:
					print(resids[0]['status'])
					if resids[0]['status']=="Yes":
						q="update answers set option_id='%s' and mark_awarded='1' where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(selanswer,qid,id)
						update(q)
					else:
						q="update answers set option_id='%s' and mark_awarded='0' where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(selanswer,qid,id)
						update(q)
			else:
				q="SELECT * FROM `options` WHERE question_id='%s' AND `option_id`='%s' " %(qid,selanswer)
				resids=select(q)
				if resids:
					print(resids[0]['status'])
					if resids[0]['status']=="Yes":
						q="insert into answers values(null,'%s',(select student_id from student_reg where login_id='%s'),'%s','1')" %(qid,id,selanswer)
						insert(q)
					else:
						q="insert into answers values(null,'%s',(select student_id from student_reg where login_id='%s'),'%s','0')" %(qid,id,selanswer)
						insert(q)
		# decrement position
		position=int(position)-1
		# check flag
		if pflag=="0":
			position=len(a)-1
			data['flag']=1
		else:
			# data['flag']=1
			pass
		print(position)
		data['position']=position

		# check whether answered
		q="select * from answers where question_id='%s' and student_id=(select student_id from student_reg where login_id='%s')" %(a[int(position)],id)
		print(q)
		res5=select(q)
		if res5:
			data['answered']=res5
		else:
			data['answered']=[{"option_id":""}]
		print("Haii",data['answered'])
		# get question details
		q="select * from questions where question_id='%s'" %(a[int(position)])
		print(q)
		res=select(q)
		data['questions']=res
		print(res)
		# get answer details 
		q="select option_id,`option` from options where question_id='%s'" %(a[int(position)])
		res=select(q)
		data['answerdetails']=res
		# for button check

		data['check']=[{'button':"Clikked"}]
		if int(position)==0:
			data['pflag']=0
		else:
			data['pflag']=1
		print(position)
		str1=""
		for ele in a:
			if str1=="":
				str1=str(ele)
			else:
				str1 = str1+","+str(ele)
		print("aaaaa"+str1)
		data['a']=str1
	if 'finish' in request.form:
		q="insert into participation values(null,(select student_id from student_reg where login_id='%s'),'%s')" %(id,eid)
		insert(q)
		q="insert into result values(null,(select student_id from student_reg where login_id='%s'),(SELECT SUM(`mark_awarded`) FROM answers INNER JOIN questions USING (question_id) WHERE student_id=(select student_id from student_reg where login_id='%s') AND exam_id='%s'),'%s')" %(id,id,eid,eid)
		insert(q)
		flash('Exam Finished')

		flash('Exam Finished')
		return redirect(url_for('student.student_view_exam'))

	return render_template("studentexamstart.html",data=data)



@student.route('/student_view_result')
def student_view_result():
	data={}
	eid=request.args['eid']
	sid=session['sid']
	q="SELECT * FROM result where exam_id='%s' and student_id='%s'" %(eid,sid)
	res=select(q)
	data['result']=res
	print(res)

	return render_template('student_view_result.html',data=data)
	

@student.route('/student_view_exam_notification')
def student_view_exam_notification():
	data={}
	sid=session['sid']
	q="SELECT * FROM notification_students INNER JOIN `exam` USING (exam_id) INNER JOIN `subject` USING(subject_id)"
	res=select(q)
	data['notification_students']=res
	print(res)
	return render_template('student_view_exam_notifications.html',data=data)