// --------------------------------------
// Create view for previously declareted property-value pair.

function(doc) {
  
  // check if value is correct
  var checkVal = function(elem, index, array) {
	return (elem.value == "TestValue1");
  };
  
  // check if property is correct
  var checkPro = function(elem, index, array) {
	return (elem.name == "TestPro1" && (elem.values.filter(checkVal)).length > 0);
  };
  
  // emit 
  if ((doc.properties.filter(checkPro)).length > 0) {
   emit(doc._id, doc);
  }
}


//-------------------------------------
// Create view of all property-value pairs,
// so it could be filtered using ?key=[property, value] option

function(doc) {
  for (var p in doc.properties) {
    for (var v in doc.properties[p]['values']) {
      emit([doc.properties[p]['name'], doc.properties[p]['values'][v]['value']], doc);
    }
  }
}