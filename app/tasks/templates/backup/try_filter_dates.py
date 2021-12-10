{% extends "layout.html" %} 

{% block content %}


<style>

.textareaContainer {	
	align: center;
	text-align:right;
	width: 100%;

}
  
#textarea_id { 
	border: 3px solid #555c;	
	align: center;
	text-align:right;
	width: 100%;
	cols: 130;
}
 
</style>

	<form method="POST" action="{{ url_for('tasks.add_task', 
											from_task_sort_order=from_task_sort_order) }}">
			
		<div class="form-group">
		  <label for="title">כותרת</label>
		  <input type="title" class="form-control" id="title" name="title" 
			     style="font-size:20px; font-family:David">
		</div>
		
		<div class="form-group">
		  <label for="body">תאור</label>
		  <input type="title" class="form-control" id="body" name="body" 
			     style="font-size:20px; font-family:David">
		</div>  
			
		<div class="form-group">
		  <label for="status">סטטוס</label>
			<select class="select" name="selected_status" id="selected_status">	
				{% for sts in statuss %}
					<option value="{{ sts.title }}">{{ sts.title }}</option>
				{% endfor %}
			</select>					
		</div>  
		
		<div class="form-group">
		  <label for="due_date">תאריך יעד</label>
		  <input type="date" class="form-control" id="due_date" name="due_date"> 
				 
		</div>
									
		<button type="submit" class="btn btn-success">שמור</button>
	
	</form>	


<script type="text/javascript" src="{{ url_for('static', filename='js/tree_list_plus.js') }}"></script>
<script>
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].onclick = function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  }
}
</script>
							
{% endblock %}

