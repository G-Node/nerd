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
