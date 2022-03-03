from flask import *
from database import *

teacher=Blueprint('teacher',__name__)

@teacher.route('/teacherhome')
def teacherhome():
	return render_template('teacherhome.html')

@teacher.route('/teacher_view_subject')
def teacher_view_subject():
	data={}
	q="select * from subject"
	res=select(q)
	data['subject']=res
	print(res)

	return render_template('teacher_view_subject.html',data=data)


@teacher.route('/teacher_view_answers')
def teacher_view_answers():
	data={}
	q="select * from answers "
	res=select(q)
	data['answers']=res
	print(res)

	return render_template('teacher_view_answers.html',data=data)


@teacher.route('/teacher_view_exams',methods=['get','post'])	
def teacher_view_exams():
	data={}
	sub_id=session['sub_id']
	q="select * from exam inner join subject using(subject_id) where subject_id='%s'"%(sub_id)
	res=select(q)
	data['exam']=res
	return render_template("teacher_view_exams.html",data=data)


@teacher.route('/teacher_manage_questions',methods=['get','post'])
def teacher_manage_questions():
	data={}
	sid=session['sid']
	eid=request.args['eid']
	data['eid']=eid

	q="select * from  questions  where staff_id='%s' and exam_id='%s'"%(sid,eid)
	res=select(q)
	data['teach']=res

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None


	if action=="delete":
		q="delete from questions where question_id='%s'"%(id)
		delete(q)
		return redirect(url_for('teacher.teacher_manage_questions',eid=eid))	

	if 'add' in request.form:
		question_desc=request.form['question_desc']
		q="insert into questions values(null,'%s','%s','%s')"%(eid,sid,question_desc)
		insert(q)
		flash("Added Sucessfully")
		return redirect(url_for('teacher.teacher_manage_questions',eid=eid))
	return render_template("teacher_manage_questions.html",data=data)

	
@teacher.route('/teacher_add_option',methods=['get','post'])
def teacher_add_option():
	data={}
	qid=request.args['qid']
	
	if 'add' in request.form:
		option=request.form['option']
		status=request.form['status']
		print(status)
		q="select * from options where question_id='%s' and status='true'"%(qid)
		res=select(q)
		if res:
			if status=='true':
				flash("Already added a correct option to this question")
			else:
				q="insert into options values(NULL,'%s','%s','%s')"%(qid,option,status)
				insert(q)
		else:
			q="insert into options values(NULL,'%s','%s','%s')"%(qid,option,status)
			insert(q)
	data['qid']=qid
	q="select * from options inner join questions using(question_id)" 
	res=select(q)
	data['options']=res

	return render_template("teacher_manage_options.html",data=data)

@teacher.route('/teacher_view_student',methods=['get','post'])
def teacher_view_student():
	data={}

	q="select * from student_reg"
	res=select(q)
	data['student_reg']=res
	return render_template("teacher_view_student.html",data=data)

# //////////////////////////////////////////////////

	
@teacher.route('/vqst',methods=['get','post'])
def vqst():
	data={}
	id=session['sid']
	tname=session['tname']
	data['tname']=tname
	print(tname)
	ide=request.args['ide']
	# ids=request.args['ids']
	if 'submit' in request.form:
		noofoption=request.form['noofoption']
		answersel=request.form['answersel']
		qust=request.form['qust']
		q="insert into questions values(null,'%s','%s','%s')" %(ide,id,qust)
		qid=insert(q)
		j=1
		for i in range(0,int(noofoption)):
			val=request.form['text'+str(j)]
			if int(j)==int(answersel):
				status="Yes"
			else:
				status="No"
			q="insert into options values(null,'%s','%s','%s')" %(qid,val,status)
			insert(q)
			j=j+1


	# v="select *,concat(First_Name,Last_Name) as Name from exam INNER JOIN questions using(exam_id ) inner join  teacher using(staff_id) where Exam_id='%s'"%(ide)
	# q=select(v)
	# print(v)
	# data['Viewsub']=q

	return render_template("teacher_manage_question.html",data=data)


	# //////////////////////////////////////////
@teacher.route('/teacher_view_questions',methods=['get','post'])
def teacher_view_questions():
	sid=session['sid']
	data={}

	q="select * from `questions` inner join `exam` using(exam_id)inner join subject using(subject_id) where staff_id='%s'"%(sid)
	res=select(q)
	data['questions']=res
	return render_template("teacher_view_questions.html",data=data)
@teacher.route('/teacher_view_options',methods=['get','post'])
def teacher_view_options():
	qid=request.args['qid']
	data={}

	q="select * from `options` where question_id='%s'"%(qid)
	res=select(q)
	data['options']=res
	return render_template("teacher_view_options.html",data=data)


@teacher.route('/teacher_view_attendancemarked_students',methods=['get','post'])	
def teacher_view_attendancemarked_students():
	data={}
	q="select * from attendance inner join student_reg using(student_id)"
	res=select(q)
	data['attendance']=res
	return render_template("teacher_view_attendancemarked_students.html",data=data)


@teacher.route('/teacher_view_result')
def teacher_view_result():
	data={}
	q="SELECT * FROM `result` INNER JOIN `student_reg` USING(student_id) INNER JOIN `exam` USING(exam_id) INNER JOIN `subject` USING(subject_id)"
	res=select(q)
	data['result']=res
	return render_template("teacher_view_result.html",data=data)

		
		

