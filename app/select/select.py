from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json

from config import basedir
import config

from app import current_app, db


from app.forms import EditForm
from app.templates import *

from sqlalchemy import update

from sqlalchemy import text # for execute SQL raw SELECT ...


#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
#################
#### imports ####
#################

from flask import Blueprint

from app import forms

################
#### config ####
################

slct = Blueprint(
    'select', __name__,
    template_folder='templates'
) 
from app import *


#####Select a destination from a list 

@slct.route('/task_select2/<int:selected_task_id>', methods=['GET', 'POST'])
def task_select2(selected_task_id):
	
    tasks = Todo.query.all()
    for task in tasks:
        task.selected = False

    task = Todo.query.filter(Todo.id == selected_task_id).first()
    if task==None:
        flash("Please select a task  first")
        redirect(url_for('tasks.edit_tasks'))
    
    task.selected = True
    db.session.commit()

    return task
###Select a task from a list


###Select a status from a list 	
@slct.route('/status_select2/<int:selected_status_id>', methods=['GET', 'POST'])
def status_select2(selected_status_id):
	
    statuss = Status.query.all()
    for status in statuss:
        status.selected = False

    status = Status.query.get_or_404(selected_status_id)				
    status.selected = True
    db.session.commit()

    return status
###Select a status from a list 	


####Select a category_select2 ##########################3	
@slct.route('/category_select2/<int:selected_category_id>', methods=['GET', 'POST'])
def category_select2(selected_category_id):

    categories = Category.query.all()
    for category in categories:
        category.selected = False

    category = Category.query.get_or_404(selected_category_id)				
    category.selected = True
    db.session.commit()

    return category	
    

@slct.route('/general_txt_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def general_txt_select2(selected_general_txt_id):
    
    general_txt =  General_txt.query.filter( General_txt.id==selected_general_txt_id ).first()
   
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("gts.edit_gts"))
             
    general_txts = General_txt.query.all()
    for gt in general_txts:
        gt.selected = False
           
    general_txt.selected = True
    db.session.commit()
    return general_txt

@slct.route('/specific_gt_type_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def specific_gt_type_select2(selected_general_txt_id, gt_type):
    
    print("IN specific_gt_type_select2 gt_type:  selected_general_txt_id: ", gt_type, selected_general_txt_id )
    
    general_txts = eval(gt_type).query.all()
    for general_txt in general_txts:
        general_txt.selected = False

    general_txt =  eval(gt_type).query.filter( eval(gt_type).id==selected_general_txt_id).first()
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("gts.edit_gts"))
        
    general_txt.selected = True
    db.session.commit()

    return general_txt


############# Std_general_txt select 
@slct.route('/std_general_txt_select2/<int:selected_std_id>/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def std_general_txt_select2(selected_std_id, selected_general_txt_id):
    
    std_general_txts = Std_general_txt.query.all()

    for std_general_txt in std_general_txts:
        std_general_txt.selected = False

    std_general_txt = Std_general_txt.query.filter(Std_general_txt.general_txt_id == selected_general_txt_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("students.edit_student_destinations"))
            
    std_general_txt.selected = True
    db.session.commit()

    return std_general_txt
############# Std_general_txt select 

	
	

