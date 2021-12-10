
#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py3#from hashlib import md5
from flask import current_app
from app import db
#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py

from datetime import datetime
from sqlalchemy.dialects.postgresql import INET
	
#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask
from sqlalchemy import event
#from common import UTCDateTime

#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
from sqlalchemy.ext.associationproxy import association_proxy

  
############################################ Dst Form for cascade dropdown display     
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
### FROM https://www.tutorialspoint.com/flask/flask_wtf.htm
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, DateField , FieldList, FormField, IntegerField
from wtforms import SelectField, validators, ValidationError
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms.fields.html5 import DateField

from wtforms.fields import StringField
from wtforms.widgets import TextArea
    
 
from datetime import datetime
from flask_login import UserMixin
   
### For Inheritance
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table

#from sqlalchemy_imageattach.entity import Image, image_attachment


#FROM https://hackersandslackers.com/forms-in-flask-wtforms/
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)

########################################## Parent_child_relationship

parent_child_relationship = db.Table('parent_child_relationship',
    db.Column('parent_id', db.Integer, db.ForeignKey('general_txt.id')),
    db.Column('child_id',  db.Integer, db.ForeignKey('general_txt.id'))
) 	
		   
########################################## Parent_child_relationship 
			   

############################################ General_txt 
from sqlalchemy.dialects.postgresql import JSON

class General_txt(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    timestamp = datetime.utcnow()

    prnt_id =  db.Column(db.Integer, nullable=True)
             
    type = db.Column(db.String(50))
    
    h_name = db.Column(db.String(50))   # for example" 'חוזקה'
    e_name = db.Column(db.String(50))   # for example" 'Are of Subject'
    h_plural_name = db.Column(db.String(100))

    gt_type = db.Column(db.String(50))  # for family like 'CBT'
    class_name = db.Column(db.String(50))  # for example" 'Subject'

    title = db.Column(db.String(255), nullable=False)
    body =  db.Column(db.String(1000))
    default = db.Column(db.Boolean)
    
    #json = db.Column(db.JSON)
    
    color_txt = db.Column(db.String(50),   nullable=True)
    color = db.Column(db.String(50),       nullable=True)
    table_color = db.Column(db.String(50), nullable=True)
    title_color = db.Column(db.String(50), nullable=True)
    odd_color = db.Column(db.String(50),   nullable=True)
    even_color = db.Column(db.String(50),  nullable=True)
    
    image_url = db.Column(db.String(1000), nullable=True)
        
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean) 
    used = db.Column(db.Boolean) 
    usr_node = db.Column(db.String(10),   nullable=True)
     
    #from_age = db.Column(db.Integer, nullable=True)   # FOR Age_range
    #to_age = db.Column(db.Integer,   nullable=True)    


   # Anthonies suggestion
    children = db.relationship(
            'General_txt', secondary=parent_child_relationship,
            primaryjoin=(parent_child_relationship.c.parent_id == id),
            secondaryjoin=(parent_child_relationship.c.child_id == id),
            backref=db.backref('parent_child_relationship', lazy=False),
            lazy=False) 
 
    __mapper_args__ = {
        'polymorphic_identity':'general_txt',
        'polymorphic_on':type
    }
    
    def get_parent(self, type):
        parents = [i for i in self.parent_child_relationship if i.type == type]
        #assert len(parents) <= 1
        if len(parents) > 0:
            return parents[0]
        return None
        #all_gts = General_txt.query.all()
        #for parent_gt in all_gts:
        #    if (parent_gt.is_parent_of(self) and parent_gt.type=='tag'):
        #        return parent_gt
        #return None
 
    def set_parent(self, general_txt):
        if not self.is_parent_of(general_txt):
            self.children.append(general_txt)
            
    def unset_parent(self, general_txt):
        if self.is_parent_of(general_txt):
            self.children.remove(general_txt)
    
    #Anthonies suggestion
    def is_parent_of(self, general_txt):
        return general_txt in self.children 
            
    def children_ids(self):
            return General_txt.query.join(
                parnet_child_relationship, (parnet_child_relationship.c.children_id == General_txt.id)).filter(
                    parnet_child_relationship.c.parent_id == self.id).order_by(
                        Generl_txt.title) 
                        
    def get_all_gts_of_type(self):
        return eval(self.gt_type).query.all()
                     
    def get_childrens_of_type(self, type):
        #return eval(type).query.filter(eval(type) in self.children).all()
        return eval(type).query.filter(eval(type) in self.children) # So the caller can deside if he wants forstor all
                      
    def set_json_obj(self):
        json_obj = { 
            "h_name": self.h_name,
            "gt_type": self.gt_type,
            "title": self.title,
            "body": self.body,
            "color": self.color 
        }
        return json_obj
                        
                                        
    def __init__(self ,title, body):
            
        self.prnt_id = -1
        
        self.title = title
        self.body = body
        
        self.timestamp = datetime.utcnow()        

        self.selected = False
        self.hide = False
        self.default = False
        self.used = True
        self.usr_node = "false"   # String an not boolean so it matches gojs template js file
        
        self.image_url = 'default_image.jpg'
        
    def __repr__(self):
        return self.class_name + ' ' + str(self.id) + '  ' + self.title
  
############################################ General_txt

class Gt_class(General_txt):

    __tablename__ = 'Gt_class'
    __mapper_args__ = {'polymorphic_identity': 'gt_class'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)

    def __init__(self ,title, body):
        self.h_name = "סוג רשומה"    # for example" 'סוג רשומה'
        self.e_name = 'Class name'   # for example" 'subect' 
        self.h_plural_name = 'סוגי רשומות '
        
        self.class_name = 'Gt_class'
        self.gt_type = 'Gt_class'

        self.color_txt = 'green'
        self.color = '#006600' 
        self.table_color = 'green_table'
        self.title_color = '#66ff99'
        self.editable = True
                
        super(self.__class__, self).__init__(title, body)       

class Status(General_txt):

    __tablename__ = 'Status'
    __mapper_args__ = {'polymorphic_identity': 'status'}
    
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
        
    def __init__(self, title, body):
           
        self.h_name = 'סטאטוס'   
        self.e_name = 'Status'  
                
        self.class_name = 'Status'
        self.gt_type = 'Status'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body)



#####            
### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
class Search_form(FlaskForm):

    table_names = SelectField("Table Name", choices=[])                                   
    
    submit = SubmitField("שלח לחיפוש")

############################################ Dst Form for cascade dropdown display     

    
class Todo(General_txt):
    __tablename__ = 'Todo'
    __mapper_args__ = {'polymorphic_identity': 'todo'}
    
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    status_id = db.Column(db.ForeignKey(Status.id), primary_key=False)
    
    due_date = db.Column(db.Date)
    
    
    
    def __init__(self ,title, body):
        
        self.h_name = 'משימה'   
        self.e_name = 'Mission'  
        self.h_plural_name = 'משימות'
        
        self.class_name = 'Todo'
        
        self.color_txt = 'orange'
        self.color = '#ffcc00' 
        self.table_color = 'orange_table'
        self.title_color = '#ffff99'
    
        self.due_date = datetime.today()
        self.status_id = Status.query.filter(Status.default==True).first()
        
        self.editable = True
        super(self.__class__, self).__init__(title, body)       
            

############################################ Todo_form
#FROM https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
########################################## Todo     
class Todo_form(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    
    title = TextField("כותרת משימה",[validators.Required("יש להכניס כותרת")])                                   
    body =  TextField("תאור משימה", render_kw={"rows": 70, "cols": 90})
  
    sts = SelectField('סטאטוס ביצוע', choices=[],validators=[validators.Required(message=('יש לבחור סטאטוס ביצוע'))])
  
    due_date =  DateField('תאריך יעד', format='%d-%m-%Y')
         
    submit = SubmitField("שמור")	
    
############################################ Todo_form


############################################ Todo_form
#FROM https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
########################################## Todo     
class Search_by_field_form(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    
    title = TextField("כותרת משימה",[validators.Required("יש להכניס כותרת")])                                   
    body =  TextField("תאור משימה", render_kw={"rows": 70, "cols": 90})
  
    sts = SelectField('סטאטוס ביצוע', choices=[],validators=[validators.Required(message=('יש לבחור סטאטוס ביצוע'))])
  
    due_date =  DateField('תאריך יעד', format='%d-%m-%Y')
    from_date =  DateField('החל מתאריך', format='%d-%m-%Y')
    to_date =  DateField('עד תאריך', format='%d-%m-%Y')
         
    submit = SubmitField("שלח לחיפוש...")	
    
############################################ Todo_form