// query function for ("Grant", "Google") pair

map = function() { 
 	var i = this._id; 
 	var id = this.object_id; 
 	this.properties.forEach(
 		function(z) { 
 			if (z.name == "Grant") {
 					var check = false; 
 					z.values.forEach(
 						function(y) {
 							if(y.value == "Google") 
 							{
 								check=true;
 							}
 						}
 					); 
 					if(check) {
 						emit(i, id);
 					} 
 			}
 		}
 	);
}



reduce = function(key, value) {
	return value;
}