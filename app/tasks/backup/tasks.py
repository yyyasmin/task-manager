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
    
    task = Todo.query.order_by(Todo.title).all()    
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

    for d in tasks:
        print("DEST ID: ", d.id)
    print("")
    
    tasks = Todo.query.order_by(Todo.title).all()
    statuses = Status.query.order_by(Status.title).all() 
    
    print("IN edit_tasks_by_title, tasks",  tasks)
    print("IN edit_tasks_by_title, statuses",  statuses)
    print("")
    
    return render_template('edit_tasks_by_title.html', tasks=tasks, statuses=statuses)															

@task.route('/edit_tasks_by_date', methods=['GET', 'POST'])
def edit_tasks_by_date():
    tasks = reset_and_get_tasks()   #get only public tasks 
    statuses = Status.query.order_by(Status.title).all() 
    
    print("IN edit_tasks_by_date")
    print("")
    print("")
 
    return render_template('edit_task_by_date.html', tasks=tasks, task=task, tags=tags, sub_tags=sub_tags)															



@task.route('/edit_tasks_by_sts', methods=['GET', 'POST'])
def edit_tasks_by_sts():
    all_tasks = reset_and_get_tasks()   #get all tasks

    stss = Status.query.all()
    tasks = Todo.query.order_by(Todo.title).all()
    return render_template('edit_task_by_sts.html',
                                            tasks=tasks,
                                            stss=stss)															
   
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_task_form_for_add ################    
@task.route('/dsply_task_form_for_add/<int:from_task_sort_order>', methods=['GET', 'POST'])
def dsply_task_form_for_add(from_task_sort_order):

    print("")
    print ("In dsply_task_form_for_add from_task_sort_order=: ", from_task_sort_order)
    
    form = Todo_form()

    form.sts.choices=[]

    form.sts.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    
    form.due_date.data = date.today()
    
    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_task_form_for_add.html', form=form, from_task_sort_order=from_task_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)
        
    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_task_form_for_add.html', form=form)

    sts = Status.query.filter_by(id=form.sts.data).first()

    new_task = Todo(form.title.data, form.body.data)
    new_task.due_date = form.due_date.data
    
    db.session.add(new_task)
    
    new_task.set_parent(sts)
    
    db.session.commit()
           
    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))
   

################## START  Update task_update ################    
@task.route('/dsply_task_form_for_update/<int:from_task_sort_order>', methods=['GET', 'POST'])
def dsply_task_form_for_update(from_task_sort_order):
    
    updated_task = Destination.query.filter(Destination.selected==True).first()
    if updated_task == None:
        flash("Please select a task to update")
        return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))

    print("")
    print("")
    print("IN dsply_task_form_for_update2 UPDATED DST IS:", updated_task.title)
    print("")
    
    form = Todo_form()

    form.title.data = updated_task.title
    form.body.data =  updated_task.body

    form.sts.choices=[]

    form.sts.choices = [(sts.id, sts.title) for sts in Scrt.query.all()]
    all_stss = Scrt.query.all()    
    for sts in all_stss:
        if updated_task.is_parent_of(sts):
            task_sts = sts
            break
        else:
            if sts.default == True:
                    task_sts = sts
    form.sts.default = task_sts.id
    form.process()
  
    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_task_form_for_update.html', task=updated_task, form=form, from_task_sort_order=from_task_sort_order)

    ### POST Case
    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_task_form_for_update.html', task=updated_task, form=form, from_task_sort_order=from_task_sort_order)
      
    sts = Status.query.filter_by(id=request.form['sts']).first()
    set_child_by_type(updated_task.id, 'Status', sts)    
    
    updated_task.title = request.form['title']      #Current Description  selection
    updated_task.body =  request.form['body']
        
    updated_task.selected=False
    db.session.commit()
      
    return redirect(url_for('tasks.edit_tasks', from_task_sort_order=from_task_sort_order))


@task.route('/dsply_task_form_for_update2/<int:selected_task_id>/<int:from_task_sort_order>', methods=['GET', 'POST'])
def dsply_task_form_for_update2(selected_task_id, from_task_sort_order):
    task = task_select2(selected_task_id)
    return redirect(url_for('tasks.dsply_task_form_for_update', from_task_sort_order=from_task_sort_order))			

############################### END DST Update

@task.route('/task_delete', methods=['GET', 'POST'])
#Here author is user_id
def task_delete():
	  
    task = Todo.query.filter(Todo.selected==True).first()
    if task == None:
        flash("Please select a task to delete first ")
        return redirect(url_for('tasks.edit_tasks', from_task_sort_order=0))
            
    #print(task.id)

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
    
