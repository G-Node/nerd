// query function for ("Grant", "Google") pair

map = function() { 
 	var i = this._id; 
 	var id = this.object_id; 
 	this.properties.forEach(
 		function(z) { 
 			if (z.name == "Threshold") {
 					var check = false; 
 					z.values.forEach(
 						function(y) {
 							if(y.value == "0.00999999977648") 
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


// --------------------------------
// map function copied from Couch implementation

map = function() { 
 // check if value is correct
  var checkVal = function(elem, index, array) {
	return (elem.value == \"%s\");
  };
  
  // check if property is correct
  var checkPro = function(elem, index, array) {
	return (elem.name == \"%s\" && (elem.values.filter(checkVal)).length > 0);
  };
  
  // emit 
  if ((doc.properties.filter(checkPro)).length > 0) {
   emit(doc._id, doc);
  }
}
