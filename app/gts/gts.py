from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json

from flask_login import LoginManager
from config import basedir
from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json

from sqlalchemy import desc   #For Get Max Value of id column


from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import Todo, General_txt

from app.forms import EditForm

from sqlalchemy import update

from flask import json

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
gt = Blueprint(
    'gts', __name__,
    template_folder='templates'
)   


from app.select.select import general_txt_select2, specific_gt_type_select2

from app import *
from datetime import datetime

import os.path

#FROM https://stackoverflow.com/questions/6473925/sqlalchemy-getting-a-list-of-tables					
from sqlalchemy import create_engine

@gt.route('/delete_all', methods=['GET', 'POST'])  # gets to difrantiate it from students same function
def delete_all():
    d_all = General_txt.query.all()
    for d in d_all:
        db.session.delete(d)
        db.session.commit()
    flash("ALL TABLES DELETED")
    return(edit_gts)



@gt.route('/populate_classes', methods=['GET', 'POST'])
def populate_classes():

    print(" IN populate_classes")
    print("")
            
    classes = Gt_class.query.all()
            
    if classes == [] or classes == None:  # IF FIRST TIME SET DB CLASSES NAMES
        table_names  = [r for r in db.engine.table_names()]
        for t in table_names:
            class_t_exist = Gt_class.query.filter(Gt_class.title == t).first()
            if class_t_exist == None or class_t_exist == []:
            
                #print("CREATING CLASS : ", t)
                
                new_t = Gt_class(t, t)
                db.session.add(new_t)
                db.session.commit()
                
                #print("NEW-t", new_t)
                #print("")               
            
    classes = Gt_class.query.order_by(Gt_class.title).all()
         
    db.session.commit()
 
    return edit_gts()
    

@gt.route('/delete_all_new', methods=['GET', 'POST'])
def delete_all_new():

    #print("IN delete_all_new")
    #print("")
    
    delete_gts = General_txt.query.filter(General_txt.title=='Enter your title').all()    
    for d in delete_gts:
    
        #print("DELETEING", d)
        
        db.session.delete(d)
        db.session.commit()
        
    delete_gts = General_txt.query.filter(General_txt.title=='New').all()        
    for d in delete_gts:
    
        #print("DELETEING", d)

        db.session.delete(d)
        db.session.commit()
    
    delete_gts = General_txt.query.filter(General_txt.color=='lightgray').all()    
    for d in delete_gts:
    
        #print("DELETEING", d)

        db.session.delete(d)
        db.session.commit()

@gt.route('/get_class_names', methods=['GET', 'POST'])
def get_class_names():
    
    #classes = populate_classes()   # CALLED IN students.index
    classes = Gt_class.query.order_by(Gt_class.title).all()
    
    #print("IN get_class_names CLASSES GTS: ")
    #print("")
    
    class_names = []
    
    class_names.append('All')

    for cn in classes:
        class_names.append(cn.title)

    return class_names

       
@gt.route('/edit_gts', methods=['GET', 'POST'])
def edit_gts():
   
    print("IN  edit_gts")
    print("")
    
    delete_all_new()
    
    #DEBUG

    #DEBUG
    
    form = Search_form()           
    form.table_names.choices = get_class_names()
    
    if request.method == 'GET':
        gts = General_txt.query.filter(General_txt.hide==False). \
                                filter(General_txt.class_name != 'Gt_class'). \
                                order_by(General_txt.class_name).all() 
        return render_template('edit_gts.html', gts=gts, form=form)

    ### POST ### 

    res = gt_filtered_gts(form)   # IN CASE OF SEARH BY ID gt_filtered_gts calls edit_single_gt

    if not res:  # USER SEARCHED BY ID THAT Is NOT IN DB
        return render_template('edit_gts.html', gts=get_all_gts(), form=form)

    if res == -1:  # USER SEARCHED BY ID THAT Is NOT IN DB
        return render_template('edit_gts.html', gts=get_all_gts(), form=form)
     
    return render_template('edit_gts.html', gts=res, form=form)


       
@gt.route('/get_all_gts', methods=['GET', 'POST'])
def get_all_gts():
    return General_txt.query.filter(General_txt.hide == False).filter(General_txt.class_name != 'Gt_class').order_by(General_txt.title).all()

@gt.route('/gt_filtered_gts', methods=['GET', 'POST'])
def gt_filtered_gts(form):
                    
    class_name = request.form.get('class_name')  # IN CASe OF POST IT COMES FROM SEARCH
    table_name = form.table_names.data           # IN CASe OF POST IT COMES FROM SEARCH

    if table_name == 'All':
        return General_txt.query.all()
    
    if table_name == 'All NOT HIDDEN':
        return General_txt.query.filter(General_txt.hide==False).all()
     
    if table_name == 'HIDDEN':
        return General_txt.query.filter(General_txt.hide==True).all()
        
 
    if class_name != None:    # FREE SEARCH EITHER INT OR STR
        class_to_find_by = class_name
        
    elif table_name != None:
        class_to_find_by = table_name
            
    else:
        #print("NO selection table_name --- class_name", table_name, class_name)
        #print("")
        return -1
            
    if class_name and class_name.isdigit():   # FIND CLASS INSTANCE BY ID
    
        #print("DIGIT: ", class_name)  
        #print("")
        
        id_to_find_by = class_name        
        gt = filter_by_id(id_to_find_by)
        if not gt:
            flash("There is no class with ID {0} In DATABASE. ".format(id_to_find_by) )

        return gt
        
    selected_class = General_txt.query.filter(General_txt.title==class_to_find_by).first()
    
    if not selected_class:
 
        flash("There is no class with STR  {0} In DATABASE. ".format(class_name) )
        return -1
        

    selected_class = specific_gt_type_select2(selected_class.id, selected_class.class_name)
           
    return filter_by_class_name(class_to_find_by)
 


@gt.route('/filter_by_class_name', methods=['GET', 'POST'])
def filter_by_class_name(class_name):

    gt_class = Gt_class.query.filter(Gt_class.title==class_name).first()
    
    #print("IN filter_by_class_name", gt_class)
    #print("")
    
    gt_class = specific_gt_type_select2(gt_class.id, gt_class.class_name)
    
    selected_gts = General_txt.query.filter(General_txt.hide==False).filter(General_txt.class_name.isnot_distinct_from(class_name)).all()
    
    if selected_gts==None or selected_gts==[]:
        flash("There is no data with {0} class name in DATABASE".format(class_name))
        
    return  selected_gts 
    
  																		
																
@gt.route('/filter_by_id', methods=['GET', 'POST'])
def filter_by_id(id):

    #print("IN filter_by_id id {0}   gt {1}".format(id, gt))

    return General_txt.query.filter(General_txt.id==id).all()
 
    
        
@gt.route('/add_child_to_gt<int:gt_id>/<int:child_gt_id>', methods=['GET', 'POST'])
def add_child_to_gt(gt_id, child_gt_id):
        
    form = Search_form()           
    form.table_names.choices = get_class_names()

    gt = General_txt.query.filter(General_txt.id == gt_id).first()

    #print("IN  add_child_to_gt child_gt_id IS : ", child_gt_id)
    #print("")

    if child_gt_id == 0:   ### GET ###
       
        ### POST ### 

        res = gt_filtered_gts(form)   # IN CASE OF SEARH BY ID gt_filtered_gts calls edit_single_gt

        #print("IN add_child_to_gt child_gt_id IS 0 res: ", res)
        #print("")

        if res != -1:   #USER SELECTION        
            if not res:  # USER SEARCHED BY ID THAT Is NOT IN DB
                #print("RES IS NONE -- calling add_or_remove_child WITH res:", res)
                #print("")
                return render_template('add_or_remove_child.html', form=form, gt=gt, gts=get_all_gts())
            
            #print("CALLING add_or_remove_child WITH GTS::", res)
            #print("")            
            return render_template('add_or_remove_child.html', form=form, gt=gt, gts=res)

        gts = General_txt.query.filter(General_txt.hide==False).filter(General_txt.class_name!='Gt_class').order_by(General_txt.title).all()

        return render_template('add_or_remove_child.html', form=form, gt=gt, gts=gts)

        gts = gt_filtered_gts(form)

    ### POST ###
    
    #import pdb; pdb.set_trace()

    child_gt = General_txt.query.filter(General_txt.id == child_gt_id).first()
    child_gt.prnt_id = gt.id
    gt.set_parent(child_gt)
    db.session.commit()
    
    #print("IN GTS add_child_to_gt GT: ", gt)
    #print("IN GTS add_child_to_gt CHILD-GT: ", child_gt)
    #print("")
    #print("")
    
        
    flash ("Child {0} Child {1} added to Parent gt {2} Child {3}  successfully ".format(child_gt.id, child_gt.title,  gt.id, gt.title))
    
    return redirect(url_for('gts.edit_gts'))   

	        
@gt.route('/add_child_to_gt2/<int:gt_id>/<int:child_id>', methods=['GET', 'POST'])
def add_child_to_gt2(gt_id, child_id):

    
    #print("IN add_child_to_gt2 METHOD", gt_id, child_id)  # child_id: 0 for GET ,    selected child_id for PUT
    #print("")
    gt = General_txt.query.filter( General_txt.id==gt_id).first()
    gt = specific_gt_type_select2(gt_id, gt.class_name)    
    return add_child_to_gt(gt.id, child_id)

        
@gt.route('/remove_child_from_gt<int:gt_id>/<int:child_gt_id>', methods=['GET', 'POST'])
def remove_child_from_gt(gt_id, child_id):
        
    form = Search_form()           
    form.table_names.choices = get_class_names()
  
    gt = General_txt.query.filter(General_txt.id == gt_id).first()
    
    ### GET ###
    if child_id==0:
        #gts = General_txt.query.order_by(General_txt.class_name).order_by(General_txt.title).all() 
        gt_children = gt.children
        #print("IN remove_child_from_gt gt_children: ", gt_children)
        #print("")
        return render_template('add_or_remove_child.html', form=form, gt=gt, gts=gt_children)
     
    ### POST ###
    child_gt = General_txt.query.filter(General_txt.id == child_id).first()
    
    #print("IIIIIIIIIIIIIIIIIIIIN remove_child_from_gt", remove_child_from_gt)
    #print("")
    
    child_gt.prnt_id = -1
    gt.unset_parent(child_gt) 
    
    db.session.commit() 
        
    flash ("Child {0} removed from Parent {1} successfully ".format(child_gt.title, gt.title))
    
    return redirect(url_for('gts.edit_gts'))   

	        
@gt.route('/remove_child_from_gt2/<int:gt_id>/<int:child_id>', methods=['GET', 'POST'])
def remove_child_from_gt2(gt_id, child_id):

    #print("IN remove_child_from_gt2", gt_id, child_id)  # child_id: 0 for GET ,    selected child_id for PUT
    #print("")

    gt = General_txt.query.filter( General_txt.id==gt_id).first()
        
    gt = specific_gt_type_select2(gt_id, gt.class_name)    
    return remove_child_from_gt(gt.id, child_id)

        
@gt.route('/gt_add', methods=['GET', 'POST'])
def gt_add(class_name, title, body, from_age, to_age, default, color, image_url, gt_type):

    print("IN gt_add class_name: ", class_name)
    print("")


    new_gt = eval(class_name)("New", "New")
    
    db.session.add(new_gt)
    db.session.commit()
                
    class_family = Family_type.query.filter(Family_type.class_name == class_name).first()
    if class_family == None:    
        new_gt.gt_type = new_gt.class_name
    else:
        new_gt.gt_type = class_family.family_type
    db.session.commit()
    

    gt_already_exist = eval(class_name).query.filter(eval(class_name).title==title).first()
    
    #print("IN gt_add  - gt_already_exist ", gt_already_exist )
    #print("")
    
    if gt_already_exist != None and gt_already_exist != []:
        flash ("This Category with the same title allready exist", gt_already_exist)
        db.session.delete(new_gt)    #NO ADDING DELETE THE NEW GT PREPARED FOR ADDITION
        db.session.commit()
        return None
     
    new_gt.title = title
    new_gt.body =  body

                
    new_gt.color_txt = color
    new_gt.color = get_color(color)

    db.session.commit() 
    
    flash("NEW CLASS {0} Is ADEDD SUCCESSFULLY!".format(new_gt))
    
    return new_gt   

    			        
@gt.route('/gt_add_by_usr', methods=['GET', 'POST'])
def gt_add_by_usr():
			
    class_type = Gt_class.query.filter(Gt_class.selected==True).first()
    
    if class_type==None or class_type==[]:
        flash("Please select a class type from the list below ")
        return edit_gts()
   
    class_name = class_type.title

    new_gt = eval(class_name)("New", "New")

    db.session.add(new_gt)
    db.session.commit()
        
    #print("IN gt_add  CREATED NEW class_type: ",new_gt)
    #print("")
    
    ### GET ###
    if request.method == 'GET':
        return render_template('add_gt.html', new_gt=new_gt)
        
    ### POST ###
    new_gt_title = request.form.get('title')
    new_gt_body = request.form.get('body')
  
    gt_already_exist = eval(class_name).query.filter(eval(class_name).title==new_gt_title).first()
    
    print("IN gt_add  - gt_already_exist ", gt_already_exist )
    print("")
    
    if gt_already_exist != None and gt_already_exist != []:
        flash ("This Category with the same title allready exist", gt_already_exist)
        db.session.delete(new_gt)    #NO ADDING DELETE THE NEW GT PREPARED FOR ADDITION
        db.session.commit()
        return edit_gts()
     
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    
    new_gt.default = request.form.get('default')=='on'
                
    new_gt.color_txt = request.form.get('color_name_txt')
    new_gt.color = get_color(new_gt.color_txt)

    
    db.session.commit() 
    
    flash("NEW CLASS {0} Is ADEDD SUCCESSFULLY!".format(new_gt))
    
    return edit_gts()    


#update selected gt
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@gt.route('/gt_update/<int:selected_gt_id>', methods=['GET', 'POST'])
def gt_update(selected_gt_id):

    gt = General_txt.query.filter(General_txt.id == selected_gt_id).first()
    if gt == None:
        flash("Please select a Category to update first")
        return edit_gts()
			
    if request.method == 'GET':
        ##print("GET render update_gt.html")
        return render_template('update_gt.html', gt=gt)
        
    gt.h_name = request.form.get('h_name')
    gt.e_name = request.form.get('e_name')
   
    gt.class_name = request.form.get('class_name')   
    gt.gt_type =    request.form.get('gt_type')   
      
    gt.color_txt = request.form.get('color_name_txt')
    gt.color = get_color(gt.color_txt)
    
    gt.image_url = url_for( 'static', filename = 'img/' + gt.gt_type + '/' + request.form.get('image_url') ),
    
    #print("IN GTS UPDATE - IMG_URL: ", gt.image_url)
     
    gt.title = request.form.get('title')
    gt.body = request.form.get('body')

    db.session.commit()  
    db.session.refresh(gt)
	
    return redirect(url_for('gts.edit_gts'))


@gt.route('/gt_delete', methods=['GET', 'POST'])
def gt_delete():

    gt = General_txt.query.filter(General_txt.selected==True).first()
    if gt == None:
        flash("Please select a gt to delete first ")
        return redirect(url_for('gts.edit_gts'))

    gt.hide = True

    db.session.commit()
    return redirect(url_for('gts.edit_gts')) 
        
#delete from index gts list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@gt.route('/gt_delete2/<int:selected_gt_id>', methods=['GET', 'POST'])
def gt_delete2(selected_gt_id):

    gt = general_txt_select2(selected_gt_id)

    #print ("SSSSSSSSSSSSSelected for delete gt is", gt )
    #print("")

    return redirect(url_for('gts.gt_delete'))

    ############ START GT CATEGORY (TAG) #############

@gt.route('/get_color', methods=['GET', 'POST'])
def get_color(color):
                       
    if color=='אדום':
        c = '#ff0000'
    elif color=='כחול':
        c = '#0000cc'
    elif color=='צהוב':
        c = '#ffcc00'
    elif color=='כתום':
        c = '#ff981a'            
    elif color=='ירוק':
        c = '#00b300'

    elif color=='lblue':
        c = '#e6ffff'
    elif color=='lyellow':
        c = '#ffffcc'  
    elif color=='lorange':
        c = '#ffe066'
    elif color=='lorange':
        c = '#ffcc66'            
    elif color=='lgreen':
        c = '#ccffcc'
    elif color=='lred':
        c = '#ffcccc'        
    elif color=='lpurple':
        c = '#ffe6ff'        

    elif color=='red':
        c = '#ff0000'
    elif color=='blue':
        c = '#0000cc'
    elif color=='yellow':
        c = '#ffcc00'
    elif color=='orange':
        c = '#ff981a'            
    elif color=='green':
        c = '#00b300'        
    elif color=='purple':
        c = '#cc00cc'        

    else:
        c = '#000000'
        
    return c

														 	
 ###START set selected category		
@gt.route('/set_gt_category/<int:selected_category_title>/<int:selected_gt_id>', methods=['GET', 'POST'])
def set_gt_category(gt_id, Ctg_of_gt_type, selected_category_title, str_msg):

    ##############import pdb; pdb.set_trace()
    #print("IN set_prf_category")
    
   # POST case
    #example: get Tag=='Math'
    selected_category = eval(Ctg_of_gt_type).query.filter(eval(Ctg_of_gt_type).title == selected_category_title).first()   
    if selected_category == None:
        flash(str_msg)
        return(url_for('students.index'))
        
    selected_category = specific_gt_type_select2(selected_category.id, Ctg_of_gt_type)    #Example: selcted Tag='Math'
    
    ###################import pdb; pdb.set_trace()
    
    gt = General_txt.query.filter(General_txt.id==gt_id).first()    #Example: select Subject='אוהב לצייר'
    
    if gt == None:
        flash("Please select a category first")
        return(url_for('gts.edit_gts'))
    
    # For example: get all Tags
    all_ctgs = eval(Ctg_of_gt_type).query.all()   # Example: get all Tags
    ####################import pdb; pdb.set_trace()
    for ctg in all_ctgs:   #delete the prevois category of the updated profile and set the new one
        if gt.is_parent_of(ctg):
            gt.unset_parent(ctg)
            gt.set_parent(selected_category)
           
    gt.set_parent(selected_category)  # Uncase there is no previous category for gt 
    
    ####################import pdb; pdb.set_trace()
    
    db.session.commit() 
    return selected_category
 ###END set selected age_range

    
###get default child gt	
@gt.route('/set_child_by_type', methods=['GET', 'POST'])
def set_child_by_type(gt_id, child_type, new_gt_child):

    print("")
    print("")    
    print("IN set_child_by_type --- gt_id={0}, child_type={1}".format( gt_id, child_type))
    print("")
    
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    print("GT IS:", gt.title)

    prev_gt_child = get_child_by_type(gt_id, child_type)
    
    if prev_gt_child == None:
        gt.set_parent(new_gt_child)
        print("There is no current child for GT {0} of type {1}. Setting GT as parent of {2}".format(gt.title, child_type, new_gt_child.title))
        db.session.commit()
        return new_gt_child 
        
    print("prev_gt_child:", prev_gt_child, prev_gt_child.id)
    print("new_gt_child:",  new_gt_child, new_gt_child.id)
    
    if prev_gt_child != new_gt_child:
        print(" IN set_child_by_type: SETTING new_gt_child {0} to gt {1}".format(new_gt_child.id, gt.id))
        gt.unset_parent(prev_gt_child)
        gt.set_parent(new_gt_child)
        print("IN GTS/set_child_by_type  GT_CHILD: old_chile={0} new_gt={1}".format(prev_gt_child.id, new_gt_child.id)) 
    else:
        print("IN GTS/set_child_by_type  PREV AND NEW CHILD GTS ARE THE SAME".format(prev_gt_child.id, new_gt_child.id))  
    
    print("")
    print("")
    db.session.commit()
    
    return new_gt_child 
     
   
###get selected default option	category	
@gt.route('/get_gt_default', methods=['GET', 'POST'])
def get_gt_default(class_name):
    gt = eval(class_name).query.filter(eval(class_name).default==True).first()    
    return gt 
    
    
###get default child gt	
@gt.route('/get_child_by_type', methods=['GET', 'POST'])
def get_child_by_type(gt_id, child_type):

    print("")
    print("")    
    print("IN get_child_by_type --- gt_id={0}, child_type={1}".format( gt_id, child_type))
    print("")
        
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    print("IN get_child_by_type --- gt=",  gt.body)

    gt_child = None
    gt_children = eval(child_type).query.all()
    for c in gt_children:
        if gt.is_parent_of(c):
            gt_child = c
            print("IN GTS/get_child_by_type  GT_CHILD:", gt_child.title, gt_child.body, gt_child.id)
            print("")
            print("") 
    return gt_child