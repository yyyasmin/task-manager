from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json

from config import basedir
import config

from app import current_app, db

from app.forms import EditForm

from sqlalchemy import update

from app.gts.gts import set_child_by_type, get_child_by_type

### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
task = Blueprint(
    'tasks', __name__,
    template_folder='templates'
)  
 
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import task_select2, status_select2
							  
from app.gts.gts import get_gt_default

from app import *

from datetime import date

                                                                
@task.route('/reset_and_get_tasks', methods=['GET', 'POST'])
def reset_and_get_tasks():

    delete_gts = General_txt.query.filter(General_txt.title=='New').all()
    for d in delete_gts:
        db.session.delete(d)
        db.session.commit()
        
    tasks = Todo.query.filter(Todo.hide==False).order_by(Todo.title).all() 

    gts = General_txt.query.all()
    for gt in gts:
        gt.selected=False
        
    db.session.commit()

    return tasks


@task.route('/edit_tasks/<int:from_task_sort_order>', methods=['GET', 'POST'])
def edit_tasks(from_task_sort_order):
    
    print("")
    print("IN tasks/edit_tasks   from_task_sort_order=: ", from_task_sort_order)
    
    task = Todo.query.filter(Todo.hide==False).order_by(Todo.title).all()    
    #############################old_task_sts pdb.set_trace()
 
    if from_task_sort_order == 2: 
        return redirect(url_for('tasks.edit_tasks_by_title', from_task_sort_order=from_task_sort_order))

    if from_task_sort_order == 3: 
        return redirect(url_for('tasks.edit_tasks_by_date', from_task_sort_order=from_task_sort_order))

    if from_task_sort_order == 4: 
        return redirect(url_for('tasks.edit_tasks_by_sts', from_task_sort_order=from_task_sort_order)) 

    return redirect(url_for('tasks.edit_tasks_by_title', from_task_sort_order=from_task_sort_order))


@task.route('/edit_tasks_by_title', methods=['GET', 'POST'])
def edit_tasks_by_title():
    
    print("In edit_tasks_by_title")
    print("")

    tasks = reset_and_get_tasks()     # get only public tasks
    
    form = Search_by_field_form()           
    form.sts.choices = [(sts.id, sts.title) for sts in Status.query.all()]

    
    if request.method=='POST':    # COMES FROM SEARCH BY STATUS
    
        print("form.sts.data", form.sts.data)
        print("form.from_date.data", form.from_date.data)
        print("form.to_date.data", form.to_date.data)
        
        if form.sts.data != None:
            return filter_by_status(form)
         
        if form.to_date.data != None:
            return filter_by_date(form)
              
    tasks = Todo.query.filter(Todo.hide==False).order_by(Todo.title).all()
    statuses = Status.query.order_by(Status.title).all() 
    
    print("IN edit_tasks_by_title, tasks",  tasks)
    print("IN edit_tasks_by_title, statuses",  statuses)
    print("")
    
    return render_template('edit_tasks_by_title.html', tasks=tasks, statuss=statuses, form=form)															


@task.route('/filter_by_status', methods=['GET', 'POST'])
def filter_by_status(form):
                    
    status_to_get_by = form.sts.data             # IN CASe OF POST IT COMES FROM SEARCH
    
    selected_status = Status.query.filter(Status.id==status_to_get_by).first()
    
    if  selected_status == None:
 
        flash("There is no such Status in DataBase: ".format(status_to_get_by) )
        return -1
    
    all_tasks = Todo.query.filter(Todo.hide==False).order_by(Todo.title).all()    

    return render_template('filter_by_status.html', tasks=all_tasks, sts=selected_status)


@task.route('/filter_by_date', methods=['GET', 'POST'])
def filter_by_date(form):
                    
    print("IN filter_by_date")
    print("")
        
    from_date = form.from_date.data
    to_date =   form.to_date.data
        
    tasks = Todo.query.filter(Todo.hide==False).filter(Todo.due_date.between(from_date, to_date)).order_by(Todo.due_date.desc())

    statuses = Status.query.order_by(Status.title).all() 
    
    return render_template('filter_by_date.html', tasks=tasks, statuss=statuses)



@task.route('/edit_tasks_by_date', methods=['GET', 'POST'])
def edit_tasks_by_date():
    tasks = reset_and_get_tasks()
    statuses = Status.query.order_by(Status.title).all() 
    
    print("IN edit_tasks_by_date")
    print("")
    print("")
 
    return render_template('edit_tasks_by_date.html', tasks=tasks, statuss=statuses)


@task.route('/edit_tasks_by_sts', methods=['GET', 'POST'])
def edit_tasks_by_sts():
    all_tasks = reset_and_get_tasks()   #get all tasks

    statuses = Status.query.all()
    tasks = Todo.query.filter(Todo.hide==False).order_by(Todo.title).all()
    return render_template('edit_task_by_status.html', tasks=tasks, statuss=statuses)
                                             
    
@task.route('/add_task/<int:from_task_sort_order>', methods=['GET', 'POST'])
def add_task(from_task_sort_order):
    
    print("IN add_task")
    print("")

    statuses = Status.query.all()
    
    if request.method == 'GET':
        return render_template('add_task.html', from_task_sort_order=from_task_sort_order, 
                                                statuss=statuses)
        
    title = request.form.get('title')
    body =  request.form.get('body')    
    task = Todo(title,body)
    db.session.add(task)
    
    task.due_date = request.form.get('due_date')    
    status_title = request.form.get('selected_status')
    status = Status.query.filter(Status.title == status_title).first()
    task.status_id = status.id
    task.set_parent(status)
         
    db.session.commit()

    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))
  
    
    #### POST ###
    
    task = Student(id, title, body)
    
    #get data from form and insert to student in studentgress  db
    task.title = request.form.get('title')
    task.body = request.form.get('body')
    task.due_date = request.form.get('due_date')
    task.status_id = request.form.get('sts')
    sts = Status.query.filter(Status.id == task.status_id).first()
    task.set_parent(sts)

    db.session.commit()  

    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))
  
    
@task.route('/get_filtered_dates/<int:from_task_sort_order>', methods=['GET', 'POST'])
def get_filtered_dates(from_task_sort_order):
    
    print("IN get_filtered_dates")
    print("")
            
    from_date =  request.form.get('from_date')
    to_date = request.form.get('to_date')
               
    tasks = Todo.query.filter(Todo.hide==False).filter(Todo.due_date.between(from_date, to_date)).order_by(Todo.due_date.desc())

    statuses = Status.query.order_by(Status.title).all() 
    
    return render_template('filter_by_date.html', tasks=tasks, statuss=statuses)
      
    
@task.route('/update_task/<int:selected_task_id>/<int:from_task_sort_order>', methods=['GET', 'POST'])
def update_task(selected_task_id, from_task_sort_order):
    
    print("IN update_task")
    print("")
    
    task = task_select2(selected_task_id)
    
    statuses = Status.query.all()
    
    if request.method == 'GET':
        return render_template('update_task.html', from_task_sort_order=from_task_sort_order, 
                                                   task=task, statuss=statuses)
    
    task.title = request.form.get('title')
    task.body = request.form.get('body')
    task.due_date = request.form.get('due_date')
    
    status_title = request.form.get('selected_status')
    status = Status.query.filter(Status.title == status_title).first()
    task.status_id = status.id
    task.set_parent(status)
         
    db.session.commit()

    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))
                                                

@task.route('/task_delete', methods=['GET', 'POST'])
#Here author is user_id
def task_delete():
	  
    task = Todo.query.filter(Todo.selected==True).first()  # HIDE=TRUE <==> DELETE
    if task == None:
        flash("Please select a task to delete first ")
        return redirect(url_for('tasks.edit_tasks', from_task_sort_order=0))
            
    task.hide = True     
    db.session.commit()
    
    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=0)) 
        
#delete from index tasks list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@task.route('/task_delete2/<int:selected_task_id>', methods=['GET', 'POST'])
#Here author is user_id
def task_delete2(selected_task_id):

	#print ("SSSSSSSSSSSSSelected task is", selected_task_id )
	dest = task_select2(selected_task_id)
	return redirect(url_for('tasks.task_delete'))
    
